#!/usr/bin/env node
/**
 * Localized, deterministic arm-proportion resculpt for Mermaid Roshan v4.
 *
 * The repaired v4 mesh has a sound skin, but its bind-pose arm segments were
 * fitted to a strongly asymmetric authored pose.  In a canonical T-frame that
 * leaves the positive-X hand region visibly nearer the torso.  This pass keeps
 * the shoulder roots, hand sculpts, topology, UVs, weights, material, and
 * embedded texture unchanged.  It redistributes only the two upper/forearm
 * lengths around their existing bilateral mean, using a shared 1.2 upper-to-
 * forearm ratio and a small chain offset that compensates for the two distinct
 * hand sculpts.  The result is symmetric hand-centroid reach without erasing
 * Roshan's intentional hand and rest-pose asymmetry.
 *
 * Vertices are resculpted with continuous per-bone axial affine maps.  The
 * upper and forearm maps agree exactly at the elbow, while forearm and hand
 * maps agree at the wrist.  Existing skin weights blend those maps into the
 * torso at each shoulder.  Normals receive the corresponding inverse-
 * transpose map; inverse bind matrices are rebuilt from the new rest joints.
 * The negative-X arm decoration remains its own indexed shell. Two incidental
 * rest-only point contacts with the chest dress are classified by incompatible
 * skin weights instead of being collapsed into false welds.
 *
 * Run from the repository root:
 *
 *   node tools/resculpt_roshan_v4.mjs \
 *     --source audit/roshan_v4_repaired.glb \
 *     --out audit/roshan_v4_resculpted.glb
 *
 * After auditing that candidate, install the exact same deterministic output:
 *
 *   node tools/resculpt_roshan_v4.mjs \
 *     --source audit/roshan_v4_repaired.glb \
 *     --out assets/characters/roshan_v4.glb
 *
 * Passing the same source and output path requires an explicit --in-place.
 */

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const EXPECTED_REPAIRED_SHA256 =
	"b50862c4117c9413d9242b81c9275dc9538733f6c63510cb8473ea208e450dbf";
const EXPECTED_RESCULPTED_SHA256 =
	"9fefb159dc9262404056d97f2e4144754108ae6d5d77b2379e19f09e65d7fedf";
const EXPECTED_IMAGE_SHA256 =
	"487c2409bcc5647b8d8f3cd5980d70e010d690de22c2968d99881490df55167d";
const PRACTICAL_WELD_TOLERANCE = 1e-4;
const EXPECTED_SOURCE_COMPONENTS = [20242, 288, 51, 4];
const EXPECTED_OUTPUT_COMPONENTS = [19996, 288, 248, 51, 4];
const EXPECTED_INCOMPATIBLE_POINT_CONTACTS = ["29202,29203", "30826,30827"];

const TARGET_UPPER_TO_FOREARM_RATIO = 1.2;
// In the canonical T-frame, the positive-X hand centroid projects about
// 0.02535 model units farther past its wrist than the negative-X hand.  Keep
// that deliberate hand-sculpt difference and offset the chain lengths by the
// same amount so the weighted hand centroids have equal lateral reach.
const TARGET_CHAIN_LENGTH_DIFFERENCE = 0.02535;

const COMPONENTS = new Map([
	["SCALAR", 1],
	["VEC2", 2],
	["VEC3", 3],
	["VEC4", 4],
	["MAT4", 16],
]);

const COMPONENT_BYTES = new Map([
	[5120, 1],
	[5121, 1],
	[5122, 2],
	[5123, 2],
	[5125, 4],
	[5126, 4],
]);

function parseArgs(argv) {
	const result = {
		source: "assets/characters/roshan_v4.glb",
		out: "audit/roshan_v4_resculpted.glb",
		inPlace: false,
	};
	for (let index = 2; index < argv.length; index += 1) {
		const argument = argv[index];
		if (argument === "--source" || argument === "--out") {
			if (index + 1 >= argv.length) {
				throw new Error(`${argument} requires a path`);
			}
			result[argument.slice(2)] = argv[index + 1];
			index += 1;
		} else if (argument === "--in-place") {
			result.inPlace = true;
		} else {
			throw new Error(`Unknown argument: ${argument}`);
		}
	}
	return result;
}

function sha256(data) {
	return crypto.createHash("sha256").update(data).digest("hex");
}

function componentRead(view, type, offset) {
	switch (type) {
		case 5120:
			return view.getInt8(offset);
		case 5121:
			return view.getUint8(offset);
		case 5122:
			return view.getInt16(offset, true);
		case 5123:
			return view.getUint16(offset, true);
		case 5125:
			return view.getUint32(offset, true);
		case 5126:
			return view.getFloat32(offset, true);
		default:
			throw new Error(`Unsupported component type ${type}`);
	}
}

function componentWrite(view, type, offset, value) {
	switch (type) {
		case 5120:
			view.setInt8(offset, value);
			break;
		case 5121:
			view.setUint8(offset, value);
			break;
		case 5122:
			view.setInt16(offset, value, true);
			break;
		case 5123:
			view.setUint16(offset, value, true);
			break;
		case 5125:
			view.setUint32(offset, value, true);
			break;
		case 5126:
			view.setFloat32(offset, value, true);
			break;
		default:
			throw new Error(`Unsupported component type ${type}`);
	}
}

function integerRange(type) {
	switch (type) {
		case 5120:
			return [-128, 127];
		case 5121:
			return [0, 255];
		case 5122:
			return [-32768, 32767];
		case 5123:
			return [0, 65535];
		case 5125:
			return [0, 4294967295];
		default:
			return null;
	}
}

class Glb {
	constructor(bytes, label) {
		if (bytes.length < 28 || bytes.toString("ascii", 0, 4) !== "glTF") {
			throw new Error(`${label}: not a GLB 2 file`);
		}
		if (bytes.readUInt32LE(4) !== 2 || bytes.readUInt32LE(8) !== bytes.length) {
			throw new Error(`${label}: invalid GLB header`);
		}
		const jsonLength = bytes.readUInt32LE(12);
		if (bytes.readUInt32LE(16) !== 0x4e4f534a) {
			throw new Error(`${label}: first chunk is not JSON`);
		}
		this.gltf = JSON.parse(bytes.subarray(20, 20 + jsonLength).toString("utf8"));
		const binaryHeader = 20 + jsonLength;
		const binaryLength = bytes.readUInt32LE(binaryHeader);
		if (bytes.readUInt32LE(binaryHeader + 4) !== 0x004e4942) {
			throw new Error(`${label}: second chunk is not BIN`);
		}
		this.binary = Buffer.from(
			bytes.subarray(binaryHeader + 8, binaryHeader + 8 + binaryLength),
		);
		this.label = label;
	}

	accessorInfo(index) {
		const accessor = this.gltf.accessors[index];
		if (accessor.sparse) {
			throw new Error(`${this.label}: sparse accessor ${index} is unsupported`);
		}
		const bufferView = this.gltf.bufferViews[accessor.bufferView];
		const components = COMPONENTS.get(accessor.type);
		const componentBytes = COMPONENT_BYTES.get(accessor.componentType);
		if (!components || !componentBytes) {
			throw new Error(`${this.label}: unsupported accessor ${index}`);
		}
		const elementBytes = components * componentBytes;
		return {
			accessor,
			bufferView,
			components,
			componentBytes,
			count: accessor.count,
			start: (bufferView.byteOffset || 0) + (accessor.byteOffset || 0),
			stride: bufferView.byteStride || elementBytes,
		};
	}

	readAccessor(index, normalize = true) {
		const info = this.accessorInfo(index);
		const values = new Float64Array(info.count * info.components);
		const view = new DataView(
			this.binary.buffer,
			this.binary.byteOffset,
			this.binary.byteLength,
		);
		const range = integerRange(info.accessor.componentType);
		for (let row = 0; row < info.count; row += 1) {
			for (let column = 0; column < info.components; column += 1) {
				const byteOffset =
					info.start + row * info.stride + column * info.componentBytes;
				let value = componentRead(view, info.accessor.componentType, byteOffset);
				if (normalize && info.accessor.normalized && range) {
					value = range[0] === 0
						? value / range[1]
						: Math.max(value / range[1], -1);
				}
				values[row * info.components + column] = value;
			}
		}
		return { values, ...info };
	}

	writeAccessor(index, values) {
		const info = this.accessorInfo(index);
		if (values.length !== info.count * info.components) {
			throw new Error(`${this.label}: wrong value count for accessor ${index}`);
		}
		const view = new DataView(
			this.binary.buffer,
			this.binary.byteOffset,
			this.binary.byteLength,
		);
		const range = integerRange(info.accessor.componentType);
		for (let row = 0; row < info.count; row += 1) {
			for (let column = 0; column < info.components; column += 1) {
				const byteOffset =
					info.start + row * info.stride + column * info.componentBytes;
				let value = values[row * info.components + column];
				if (info.accessor.normalized && range) {
					value = Math.round(Math.max(-1, Math.min(1, value)) * range[1]);
				}
				componentWrite(view, info.accessor.componentType, byteOffset, value);
			}
		}
	}

	imagePayloads() {
		const payloads = [];
		for (const image of this.gltf.images || []) {
			if (image.bufferView === undefined) {
				continue;
			}
			const bufferView = this.gltf.bufferViews[image.bufferView];
			const start = bufferView.byteOffset || 0;
			payloads.push(this.binary.subarray(start, start + bufferView.byteLength));
		}
		return payloads;
	}

	toBuffer() {
		let json = Buffer.from(JSON.stringify(this.gltf), "utf8");
		while (json.length % 4 !== 0) {
			json = Buffer.concat([json, Buffer.from(" ")]);
		}
		let binary = this.binary;
		while (binary.length % 4 !== 0) {
			binary = Buffer.concat([binary, Buffer.from([0])]);
		}
		const total = 12 + 8 + json.length + 8 + binary.length;
		const result = Buffer.alloc(total);
		result.write("glTF", 0, "ascii");
		result.writeUInt32LE(2, 4);
		result.writeUInt32LE(total, 8);
		result.writeUInt32LE(json.length, 12);
		result.writeUInt32LE(0x4e4f534a, 16);
		json.copy(result, 20);
		const binaryHeader = 20 + json.length;
		result.writeUInt32LE(binary.length, binaryHeader);
		result.writeUInt32LE(0x004e4942, binaryHeader + 4);
		binary.copy(result, binaryHeader + 8);
		return result;
	}
}

function vectorAdd(a, b) {
	return [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
}

function vectorSub(a, b) {
	return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
}

function vectorScale(a, scale) {
	return [a[0] * scale, a[1] * scale, a[2] * scale];
}

function vectorLength(a) {
	return Math.hypot(a[0], a[1], a[2]);
}

function vectorNormalize(a) {
	const length = vectorLength(a);
	if (length < 1e-12) {
		throw new Error("Cannot normalize a zero-length vector");
	}
	return vectorScale(a, 1 / length);
}

function matrix3Identity() {
	return [1, 0, 0, 0, 1, 0, 0, 0, 1];
}

function matrix3Axial(axis, scale) {
	const result = matrix3Identity();
	for (let row = 0; row < 3; row += 1) {
		for (let column = 0; column < 3; column += 1) {
			result[row * 3 + column] +=
				(scale - 1) * axis[row] * axis[column];
		}
	}
	return result;
}

function matrix3Vector(matrix, vector) {
	return [
		matrix[0] * vector[0] + matrix[1] * vector[1] + matrix[2] * vector[2],
		matrix[3] * vector[0] + matrix[4] * vector[1] + matrix[5] * vector[2],
		matrix[6] * vector[0] + matrix[7] * vector[1] + matrix[8] * vector[2],
	];
}

function matrix3Inverse(matrix) {
	const [a, b, c, d, e, f, g, h, i] = matrix;
	const determinant =
		a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g);
	if (Math.abs(determinant) < 1e-12) {
		throw new Error("Singular deformation gradient");
	}
	const reciprocal = 1 / determinant;
	return [
		(e * i - f * h) * reciprocal,
		(c * h - b * i) * reciprocal,
		(b * f - c * e) * reciprocal,
		(f * g - d * i) * reciprocal,
		(a * i - c * g) * reciprocal,
		(c * d - a * f) * reciprocal,
		(d * h - e * g) * reciprocal,
		(b * g - a * h) * reciprocal,
		(a * e - b * d) * reciprocal,
	];
}

function matrix3Transpose(matrix) {
	return [
		matrix[0], matrix[3], matrix[6],
		matrix[1], matrix[4], matrix[7],
		matrix[2], matrix[5], matrix[8],
	];
}

function matrix4Identity() {
	return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
}

function matrix4Multiply(a, b) {
	const result = new Array(16).fill(0);
	for (let row = 0; row < 4; row += 1) {
		for (let column = 0; column < 4; column += 1) {
			for (let inner = 0; inner < 4; inner += 1) {
				result[row * 4 + column] +=
					a[row * 4 + inner] * b[inner * 4 + column];
			}
		}
	}
	return result;
}

function matrix4Inverse(matrix) {
	const augmented = Array.from({ length: 4 }, (_, row) => [
		...matrix.slice(row * 4, row * 4 + 4),
		...matrix4Identity().slice(row * 4, row * 4 + 4),
	]);
	for (let column = 0; column < 4; column += 1) {
		let pivot = column;
		for (let row = column + 1; row < 4; row += 1) {
			if (Math.abs(augmented[row][column]) > Math.abs(augmented[pivot][column])) {
				pivot = row;
			}
		}
		if (Math.abs(augmented[pivot][column]) < 1e-12) {
			throw new Error("Singular 4x4 matrix");
		}
		[augmented[column], augmented[pivot]] = [augmented[pivot], augmented[column]];
		const divisor = augmented[column][column];
		for (let item = 0; item < 8; item += 1) {
			augmented[column][item] /= divisor;
		}
		for (let row = 0; row < 4; row += 1) {
			if (row === column) {
				continue;
			}
			const factor = augmented[row][column];
			for (let item = 0; item < 8; item += 1) {
				augmented[row][item] -= factor * augmented[column][item];
			}
		}
	}
	return augmented.flatMap((row) => row.slice(4));
}

function quaternionMatrix(quaternion) {
	const [x, y, z, w] = quaternion;
	return [
		1 - 2 * (y * y + z * z),
		2 * (x * y - z * w),
		2 * (x * z + y * w),
		2 * (x * y + z * w),
		1 - 2 * (x * x + z * z),
		2 * (y * z - x * w),
		2 * (x * z - y * w),
		2 * (y * z + x * w),
		1 - 2 * (x * x + y * y),
	];
}

function nodeLocal(node) {
	if (node.matrix) {
		// glTF stores matrix arrays column-major.
		return Array.from({ length: 16 }, (_, index) => {
			const row = Math.floor(index / 4);
			const column = index % 4;
			return node.matrix[column * 4 + row];
		});
	}
	const translation = node.translation || [0, 0, 0];
	const rotation = quaternionMatrix(node.rotation || [0, 0, 0, 1]);
	const scale = node.scale || [1, 1, 1];
	const result = matrix4Identity();
	for (let row = 0; row < 3; row += 1) {
		for (let column = 0; column < 3; column += 1) {
			result[row * 4 + column] = rotation[row * 3 + column] * scale[column];
		}
	}
	result[3] = translation[0];
	result[7] = translation[1];
	result[11] = translation[2];
	return result;
}

function nodeGlobals(gltf) {
	const parents = new Map();
	for (let parent = 0; parent < gltf.nodes.length; parent += 1) {
		for (const child of gltf.nodes[parent].children || []) {
			parents.set(child, parent);
		}
	}
	const globals = new Array(gltf.nodes.length);
	function visit(index) {
		if (globals[index]) {
			return globals[index];
		}
		const local = nodeLocal(gltf.nodes[index]);
		globals[index] = parents.has(index)
			? matrix4Multiply(visit(parents.get(index)), local)
			: local;
		return globals[index];
	}
	for (let index = 0; index < gltf.nodes.length; index += 1) {
		visit(index);
	}
	return globals;
}

function matrixTranslation(matrix) {
	return [matrix[3], matrix[7], matrix[11]];
}

function affinePoint(transform, point) {
	return vectorAdd(
		transform.newAnchor,
		matrix3Vector(transform.linear, vectorSub(point, transform.oldAnchor)),
	);
}

function accessorDigest(glb, index) {
	const info = glb.accessorInfo(index);
	const chunks = [];
	for (let row = 0; row < info.count; row += 1) {
		const start = info.start + row * info.stride;
		chunks.push(glb.binary.subarray(start, start + info.components * info.componentBytes));
	}
	return sha256(Buffer.concat(chunks));
}

function selectedAccessorDigest(glb, index, selected) {
	const info = glb.accessorInfo(index);
	const digest = crypto.createHash("sha256");
	for (let row = 0; row < info.count; row += 1) {
		if (!selected(row)) {
			continue;
		}
		const start = info.start + row * info.stride;
		digest.update(
			glb.binary.subarray(start, start + info.components * info.componentBytes),
		);
	}
	return digest.digest("hex");
}

function practicalWeldTopology(positionValues, indexValues) {
	const vertexCount = positionValues.length / 3;
	const groupByVertex = new Int32Array(vertexCount);
	groupByVertex.fill(-1);
	const groups = [];
	const lookup = new Map();
	for (const rawIndex of indexValues) {
		const vertex = Math.round(rawIndex);
		if (groupByVertex[vertex] >= 0) {
			continue;
		}
		const key = [0, 1, 2]
			.map((axis) => Math.round(
				positionValues[vertex * 3 + axis] / PRACTICAL_WELD_TOLERANCE,
			))
			.join(",");
		let group = lookup.get(key);
		if (group === undefined) {
			group = groups.length;
			lookup.set(key, group);
			groups.push([]);
		}
		groupByVertex[vertex] = group;
		groups[group].push(vertex);
	}

	const parent = Int32Array.from({ length: groups.length }, (_, index) => index);
	function find(index) {
		let current = index;
		while (parent[current] !== current) {
			parent[current] = parent[parent[current]];
			current = parent[current];
		}
		return current;
	}
	function unite(a, b) {
		const rootA = find(a);
		const rootB = find(b);
		if (rootA !== rootB) {
			parent[rootB] = rootA;
		}
	}
	for (let offset = 0; offset < indexValues.length; offset += 3) {
		const a = groupByVertex[Math.round(indexValues[offset])];
		const b = groupByVertex[Math.round(indexValues[offset + 1])];
		const c = groupByVertex[Math.round(indexValues[offset + 2])];
		unite(a, b);
		unite(b, c);
		unite(c, a);
	}
	const sizes = new Map();
	for (let group = 0; group < groups.length; group += 1) {
		const root = find(group);
		sizes.set(root, (sizes.get(root) || 0) + 1);
	}
	return {
		componentSizes: [...sizes.values()].sort((a, b) => b - a),
		groupByVertex,
		groups,
	};
}

function canonicalPath(filePath) {
	let cursor = path.resolve(filePath);
	const suffix = [];
	while (!fs.existsSync(cursor)) {
		const parent = path.dirname(cursor);
		if (parent === cursor) {
			throw new Error(`Cannot resolve path identity for ${filePath}`);
		}
		suffix.unshift(path.basename(cursor));
		cursor = parent;
	}
	return path.join(fs.realpathSync.native(cursor), ...suffix);
}

function pathIdentityKey(filePath) {
	const canonical = canonicalPath(filePath);
	return process.platform === "win32" ? canonical.toLowerCase() : canonical;
}

function pathsReferToSameFile(a, b) {
	if (fs.existsSync(a) && fs.existsSync(b)) {
		const statA = fs.statSync(a);
		const statB = fs.statSync(b);
		if (statA.dev === statB.dev && statA.ino !== 0 && statA.ino === statB.ino) {
			return true;
		}
	}
	return pathIdentityKey(a) === pathIdentityKey(b);
}

function writeVerifiedAtomic(outPath, bytes, expectedHash) {
	const directory = path.dirname(outPath);
	fs.mkdirSync(directory, { recursive: true });
	const existingMode = fs.existsSync(outPath)
		? fs.statSync(outPath).mode & 0o777
		: undefined;
	let temporaryPath = "";
	for (let attempt = 0; attempt < 20; attempt += 1) {
		const suffix = crypto.randomBytes(8).toString("hex");
		const candidate = path.join(
			directory,
			`.${path.basename(outPath)}.${process.pid}.${suffix}.tmp`,
		);
		try {
			const descriptor = fs.openSync(candidate, "wx", existingMode ?? 0o666);
			try {
				fs.writeFileSync(descriptor, bytes);
				fs.fsyncSync(descriptor);
			} finally {
				fs.closeSync(descriptor);
			}
			temporaryPath = candidate;
			break;
		} catch (error) {
			if (error?.code !== "EEXIST") {
				throw error;
			}
		}
	}
	if (!temporaryPath) {
		throw new Error(`Unable to allocate a sibling temporary file for ${outPath}`);
	}
	try {
		const temporaryHash = sha256(fs.readFileSync(temporaryPath));
		if (temporaryHash !== expectedHash) {
			throw new Error(
				`Temporary output hash ${temporaryHash} differs from ${expectedHash}`,
			);
		}
		fs.renameSync(temporaryPath, outPath);
		temporaryPath = "";
		const installedHash = sha256(fs.readFileSync(outPath));
		if (installedHash !== expectedHash) {
			throw new Error(
				`Installed output hash ${installedHash} differs from ${expectedHash}`,
			);
		}
	} finally {
		if (temporaryPath && fs.existsSync(temporaryPath)) {
			fs.unlinkSync(temporaryPath);
		}
	}
}

function main() {
	const args = parseArgs(process.argv);
	const sourcePath = path.resolve(args.source);
	const outPath = path.resolve(args.out);
	const sameFile = pathsReferToSameFile(sourcePath, outPath);
	if (sameFile && !args.inPlace) {
		throw new Error(
			"Refusing to overwrite --source without --in-place; write and audit a candidate first",
		);
	}
	const sourceBytes = fs.readFileSync(sourcePath);
	const sourceHash = sha256(sourceBytes);
	if (EXPECTED_RESCULPTED_SHA256 && sourceHash === EXPECTED_RESCULPTED_SHA256) {
		if (!sameFile) {
			writeVerifiedAtomic(outPath, sourceBytes, sourceHash);
		}
		console.log(`ROSHAN_RESCULPT|SOURCE_ALREADY_FINAL|${sourceHash}`);
		console.log(`ROSHAN_RESCULPT|OUTPUT|${outPath}`);
		return;
	}
	if (sourceHash !== EXPECTED_REPAIRED_SHA256) {
		throw new Error(
			"Source is not the audited repaired Roshan v4 GLB; run the binding repair first",
		);
	}
	const glb = new Glb(sourceBytes, "repaired Roshan v4");
	if (glb.gltf.meshes?.length !== 1 || glb.gltf.skins?.length !== 1) {
		throw new Error("Expected Roshan's one-mesh/one-skin GLB contract");
	}
	const primitive = glb.gltf.meshes[0].primitives[0];
	const positionIndex = primitive.attributes.POSITION;
	const normalIndex = primitive.attributes.NORMAL;
	const jointsIndex = primitive.attributes.JOINTS_0;
	const weightsIndex = primitive.attributes.WEIGHTS_0;
	const immutableDigests = new Map();
	for (const index of [
		primitive.attributes.TEXCOORD_0,
		primitive.indices,
		jointsIndex,
		weightsIndex,
	]) {
		immutableDigests.set(index, accessorDigest(glb, index));
	}

	const skin = glb.gltf.skins[0];
	const jointNames = skin.joints.map((nodeIndex) => glb.gltf.nodes[nodeIndex].name || "");
	const skinIndexByName = new Map(jointNames.map((name, index) => [name, index]));
	const nodeIndexByName = new Map(
		glb.gltf.nodes
			.map((node, index) => [node.name, index])
			.filter(([name]) => Boolean(name)),
	);
	for (const name of ["armU", "armF", "hand", "armU2", "armF2", "hand2"]) {
		if (!skinIndexByName.has(name) || !nodeIndexByName.has(name)) {
			throw new Error(`Required arm joint is missing: ${name}`);
		}
	}

	const globalsBefore = nodeGlobals(glb.gltf);
	const chains = [
		{ label: "positive_x", upper: "armU", forearm: "armF", hand: "hand" },
		{ label: "negative_x", upper: "armU2", forearm: "armF2", hand: "hand2" },
	];
	for (const chain of chains) {
		chain.shoulder = matrixTranslation(globalsBefore[nodeIndexByName.get(chain.upper)]);
		chain.elbow = matrixTranslation(globalsBefore[nodeIndexByName.get(chain.forearm)]);
		chain.wrist = matrixTranslation(globalsBefore[nodeIndexByName.get(chain.hand)]);
		chain.upperVector = vectorSub(chain.elbow, chain.shoulder);
		chain.forearmVector = vectorSub(chain.wrist, chain.elbow);
		chain.oldUpperLength = vectorLength(chain.upperVector);
		chain.oldForearmLength = vectorLength(chain.forearmVector);
		chain.oldTotalLength = chain.oldUpperLength + chain.oldForearmLength;
	}
	const meanTotal = (chains[0].oldTotalLength + chains[1].oldTotalLength) / 2;
	chains[0].targetTotalLength = meanTotal - TARGET_CHAIN_LENGTH_DIFFERENCE / 2;
	chains[1].targetTotalLength = meanTotal + TARGET_CHAIN_LENGTH_DIFFERENCE / 2;
	for (const chain of chains) {
		chain.targetForearmLength =
			chain.targetTotalLength / (TARGET_UPPER_TO_FOREARM_RATIO + 1);
		chain.targetUpperLength =
			chain.targetTotalLength - chain.targetForearmLength;
		chain.upperScale = chain.targetUpperLength / chain.oldUpperLength;
		chain.forearmScale = chain.targetForearmLength / chain.oldForearmLength;
		chain.newElbow = vectorAdd(
			chain.shoulder,
			vectorScale(chain.upperVector, chain.upperScale),
		);
		chain.newWrist = vectorAdd(
			chain.newElbow,
			vectorScale(chain.forearmVector, chain.forearmScale),
		);
		chain.transforms = [
			{
				name: chain.upper,
				oldAnchor: chain.shoulder,
				newAnchor: chain.shoulder,
				linear: matrix3Axial(vectorNormalize(chain.upperVector), chain.upperScale),
			},
			{
				name: chain.forearm,
				oldAnchor: chain.elbow,
				newAnchor: chain.newElbow,
				linear: matrix3Axial(
					vectorNormalize(chain.forearmVector),
					chain.forearmScale,
				),
			},
			{
				name: chain.hand,
				oldAnchor: chain.wrist,
				newAnchor: chain.newWrist,
				linear: matrix3Identity(),
			},
		];
	}

	const transformBySkinIndex = new Map();
	for (const chain of chains) {
		for (const transform of chain.transforms) {
			transformBySkinIndex.set(skinIndexByName.get(transform.name), transform);
		}
	}

	const position = glb.readAccessor(positionIndex);
	const normal = glb.readAccessor(normalIndex);
	const joints = glb.readAccessor(jointsIndex, false);
	const weights = glb.readAccessor(weightsIndex);
	const indices = glb.readAccessor(primitive.indices, false);
	if (
		position.count !== normal.count ||
		position.count !== joints.count ||
		position.count !== weights.count
	) {
		throw new Error("Position/normal/joint/weight accessor counts differ");
	}
	const newPosition = new Float64Array(position.values.length);
	const newNormal = new Float64Array(normal.values.length);
	const gradientByVertex = new Float64Array(position.count * 9);
	const directlyAffected = new Uint8Array(position.count);
	const sourceWeld = practicalWeldTopology(position.values, indices.values);
	if (
		JSON.stringify(sourceWeld.componentSizes) !==
		JSON.stringify(EXPECTED_SOURCE_COMPONENTS)
	) {
		throw new Error(
			`Unexpected repaired-source topology: ${sourceWeld.componentSizes.join(",")}`,
		);
	}
	for (let vertex = 0; vertex < position.count; vertex += 1) {
		const point = Array.from(position.values.subarray(vertex * 3, vertex * 3 + 3));
		const result = [...point];
		const gradient = matrix3Identity();
		let affectedWeight = 0;
		for (let influence = 0; influence < 4; influence += 1) {
			const offset = vertex * 4 + influence;
			const transform = transformBySkinIndex.get(Math.round(joints.values[offset]));
			const weight = weights.values[offset];
			if (!transform || weight <= 0) {
				continue;
			}
			affectedWeight += weight;
			const mapped = affinePoint(transform, point);
			for (let axis = 0; axis < 3; axis += 1) {
				result[axis] += weight * (mapped[axis] - point[axis]);
			}
			for (let item = 0; item < 9; item += 1) {
				gradient[item] += weight * (
					transform.linear[item] - (item % 4 === 0 ? 1 : 0)
				);
			}
		}
		directlyAffected[vertex] = affectedWeight > 1e-8 ? 1 : 0;
		for (let axis = 0; axis < 3; axis += 1) {
			newPosition[vertex * 3 + axis] = result[axis];
		}
		for (let item = 0; item < 9; item += 1) {
			gradientByVertex[vertex * 9 + item] = gradient[item];
		}
	}

	// The negative-X arm decoration is an independent indexed shell.  In the
	// repaired rest mesh it merely touches the chest-only dress shell at two
	// coincident points; it shares no edge or face with that shell.  Those point
	// pairs have mutually exclusive skin influences, so forcing their positions
	// to remain welded would collapse one surface whenever the arm changes
	// length.  Classify and allow exactly those two contacts to open.
	const incompatiblePointContacts = [];
	let maximumCompatibleRawWeldSpread = 0;
	let maximumRawWeldSpread = 0;
	for (const group of sourceWeld.groups) {
		if (group.length < 2 || !group.some((vertex) => directlyAffected[vertex])) {
			continue;
		}
		let sourceSpread = 0;
		let rawSpread = 0;
		for (let a = 0; a < group.length; a += 1) {
			for (let b = a + 1; b < group.length; b += 1) {
				const sourceA = [0, 1, 2].map(
					(axis) => position.values[group[a] * 3 + axis],
				);
				const sourceB = [0, 1, 2].map(
					(axis) => position.values[group[b] * 3 + axis],
				);
				const mappedA = [0, 1, 2].map(
					(axis) => newPosition[group[a] * 3 + axis],
				);
				const mappedB = [0, 1, 2].map(
					(axis) => newPosition[group[b] * 3 + axis],
				);
				sourceSpread = Math.max(
					sourceSpread,
					vectorLength(vectorSub(sourceA, sourceB)),
				);
				rawSpread = Math.max(rawSpread, vectorLength(vectorSub(mappedA, mappedB)));
			}
		}
		if (sourceSpread > PRACTICAL_WELD_TOLERANCE * 0.1) {
			throw new Error(
				`Practical-weld source group spans ${sourceSpread}; refusing to collapse it`,
			);
		}
		maximumRawWeldSpread = Math.max(maximumRawWeldSpread, rawSpread);
		if (rawSpread <= PRACTICAL_WELD_TOLERANCE * 0.1) {
			maximumCompatibleRawWeldSpread = Math.max(
				maximumCompatibleRawWeldSpread,
				rawSpread,
			);
			continue;
		}
		if (group.length !== 2) {
			throw new Error("A multi-entry practical weld opened unexpectedly");
		}
		const [first, second] = group;
		let sharesIndexedEdge = false;
		for (let offset = 0; offset < indices.values.length; offset += 3) {
			const triangle = [0, 1, 2].map(
				(item) => Math.round(indices.values[offset + item]),
			);
			if (triangle.includes(first) && triangle.includes(second)) {
				sharesIndexedEdge = true;
				break;
			}
		}
		if (sharesIndexedEdge) {
			throw new Error("An opening practical weld shares an indexed edge");
		}
		const profiles = group.map((vertex) => {
			const profile = new Map();
			for (let influence = 0; influence < 4; influence += 1) {
				const offset = vertex * 4 + influence;
				const weight = weights.values[offset];
				if (weight > 1e-6) {
					const name = jointNames[Math.round(joints.values[offset])];
					profile.set(name, (profile.get(name) || 0) + weight);
				}
			}
			return profile;
		});
		const isChest = (profile) =>
			profile.size === 1 && Math.abs((profile.get("chest") || 0) - 1) < 1e-5;
		const negativeArmNames = new Set(["armU2", "armF2", "hand2"]);
		const isNegativeArm = (profile) =>
			profile.size > 0 &&
			[...profile.keys()].every((name) => negativeArmNames.has(name)) &&
			Math.abs([...profile.values()].reduce((sum, value) => sum + value, 0) - 1) < 1e-5;
		if (
			!((isChest(profiles[0]) && isNegativeArm(profiles[1])) ||
			(isChest(profiles[1]) && isNegativeArm(profiles[0])))
		) {
			throw new Error("Opening point contact is not chest-to-negative-arm decoration");
		}
		let sharedInfluence = 0;
		for (const [name, weight] of profiles[0]) {
			sharedInfluence += Math.min(weight, profiles[1].get(name) || 0);
		}
		if (sharedInfluence > 1e-6) {
			throw new Error("Opening point contact has deformation-compatible weights");
		}
		incompatiblePointContacts.push({
			key: [...group].sort((a, b) => a - b).join(","),
			spread: rawSpread,
		});
	}
	const pointContactKeys = incompatiblePointContacts
		.map((contact) => contact.key)
		.sort();
	if (
		JSON.stringify(pointContactKeys) !==
		JSON.stringify(EXPECTED_INCOMPATIBLE_POINT_CONTACTS)
	) {
		throw new Error(
			`Unexpected incompatible point contacts: ${pointContactKeys.join(";")}`,
		);
	}
	const unaffectedNormalDigest = selectedAccessorDigest(
		glb,
		normalIndex,
		(vertex) => !directlyAffected[vertex],
	);

	let affectedVertices = 0;
	let maximumDisplacement = 0;
	for (let vertex = 0; vertex < position.count; vertex += 1) {
		const sourcePoint = [0, 1, 2].map(
			(axis) => position.values[vertex * 3 + axis],
		);
		for (let axis = 0; axis < 3; axis += 1) {
			newPosition[vertex * 3 + axis] = Math.fround(
				newPosition[vertex * 3 + axis],
			);
		}
		const mappedPoint = [0, 1, 2].map(
			(axis) => newPosition[vertex * 3 + axis],
		);
		const displacement = vectorLength(vectorSub(mappedPoint, sourcePoint));
		if (displacement > 1e-8) {
			affectedVertices += 1;
		}
		maximumDisplacement = Math.max(maximumDisplacement, displacement);

		const sourceNormal = Array.from(
			normal.values.subarray(vertex * 3, vertex * 3 + 3),
		);
		let mappedNormal = sourceNormal;
		if (directlyAffected[vertex]) {
			const gradient = Array.from(
				gradientByVertex.subarray(vertex * 9, vertex * 9 + 9),
			);
			const normalMatrix = matrix3Transpose(matrix3Inverse(gradient));
			mappedNormal = vectorNormalize(matrix3Vector(normalMatrix, sourceNormal));
		}
		for (let axis = 0; axis < 3; axis += 1) {
			newNormal[vertex * 3 + axis] = Math.fround(mappedNormal[axis]);
		}
	}

	const outputWeld = practicalWeldTopology(newPosition, indices.values);
	if (
		JSON.stringify(outputWeld.componentSizes) !==
		JSON.stringify(EXPECTED_OUTPUT_COMPONENTS)
	) {
		throw new Error(
			`Unexpected resculpted topology: ${outputWeld.componentSizes.join(",")}`,
		);
	}

	for (const chain of chains) {
		const forearmNode = glb.gltf.nodes[nodeIndexByName.get(chain.forearm)];
		const handNode = glb.gltf.nodes[nodeIndexByName.get(chain.hand)];
		if (!forearmNode.translation || !handNode.translation) {
			throw new Error(`${chain.label}: arm nodes unexpectedly lack translations`);
		}
		forearmNode.translation = forearmNode.translation.map(
			(value) => value * chain.upperScale,
		);
		handNode.translation = handNode.translation.map(
			(value) => value * chain.forearmScale,
		);
	}

	glb.writeAccessor(positionIndex, newPosition);
	glb.writeAccessor(normalIndex, newNormal);
	if (
		selectedAccessorDigest(
			glb,
			normalIndex,
			(vertex) => !directlyAffected[vertex],
		) !== unaffectedNormalDigest
	) {
		throw new Error("Normals outside the resculpted arm influences changed");
	}
	const boundsMin = [Infinity, Infinity, Infinity];
	const boundsMax = [-Infinity, -Infinity, -Infinity];
	for (let vertex = 0; vertex < position.count; vertex += 1) {
		for (let axis = 0; axis < 3; axis += 1) {
			const value = newPosition[vertex * 3 + axis];
			boundsMin[axis] = Math.min(boundsMin[axis], value);
			boundsMax[axis] = Math.max(boundsMax[axis], value);
		}
	}
	glb.gltf.accessors[positionIndex].min = boundsMin;
	glb.gltf.accessors[positionIndex].max = boundsMax;

	const globalsAfter = nodeGlobals(glb.gltf);
	const inverseBinds = new Float64Array(skin.joints.length * 16);
	for (let joint = 0; joint < skin.joints.length; joint += 1) {
		const inverse = matrix4Inverse(globalsAfter[skin.joints[joint]]);
		for (let row = 0; row < 4; row += 1) {
			for (let column = 0; column < 4; column += 1) {
				inverseBinds[joint * 16 + column * 4 + row] = inverse[row * 4 + column];
			}
		}
	}
	glb.writeAccessor(skin.inverseBindMatrices, inverseBinds);

	for (const [index, digest] of immutableDigests) {
		if (accessorDigest(glb, index) !== digest) {
			throw new Error(`Immutable accessor ${index} changed during resculpt`);
		}
	}
	const images = glb.imagePayloads();
	if (images.length !== 1 || sha256(images[0]) !== EXPECTED_IMAGE_SHA256) {
		throw new Error("Embedded v4g texture changed or is missing");
	}
	for (const chain of chains) {
		const shoulder = matrixTranslation(globalsAfter[nodeIndexByName.get(chain.upper)]);
		const elbow = matrixTranslation(globalsAfter[nodeIndexByName.get(chain.forearm)]);
		const wrist = matrixTranslation(globalsAfter[nodeIndexByName.get(chain.hand)]);
		const upperLength = vectorLength(vectorSub(elbow, shoulder));
		const forearmLength = vectorLength(vectorSub(wrist, elbow));
		if (
			Math.abs(upperLength - chain.targetUpperLength) > 2e-6 ||
			Math.abs(forearmLength - chain.targetForearmLength) > 2e-6
		) {
			throw new Error(`${chain.label}: rebuilt joint lengths missed their targets`);
		}
		chain.newUpperLength = upperLength;
		chain.newForearmLength = forearmLength;
	}

	const outputBytes = glb.toBuffer();
	const outputHash = sha256(outputBytes);
	if (EXPECTED_RESCULPTED_SHA256 && outputHash !== EXPECTED_RESCULPTED_SHA256) {
		throw new Error(
			`Resculpt output ${outputHash} differs from audited result ${EXPECTED_RESCULPTED_SHA256}`,
		);
	}
	writeVerifiedAtomic(outPath, outputBytes, outputHash);
	console.log(`ROSHAN_RESCULPT|SOURCE_SHA256|${sourceHash}`);
	console.log(`ROSHAN_RESCULPT|OUTPUT_SHA256|${outputHash}`);
	console.log(`ROSHAN_RESCULPT|TEXTURE_SHA256|${sha256(images[0])}`);
	for (const chain of chains) {
		console.log(
			`ROSHAN_RESCULPT|${chain.label.toUpperCase()}|` +
				`upper=${chain.oldUpperLength.toFixed(9)}->${chain.newUpperLength.toFixed(9)}|` +
				`forearm=${chain.oldForearmLength.toFixed(9)}->${chain.newForearmLength.toFixed(9)}|` +
				`total=${chain.oldTotalLength.toFixed(9)}->${(
					chain.newUpperLength + chain.newForearmLength
				).toFixed(9)}`,
		);
	}
	console.log(`ROSHAN_RESCULPT|AFFECTED_VERTICES|${affectedVertices}`);
	console.log(`ROSHAN_RESCULPT|MAXIMUM_REST_DISPLACEMENT|${maximumDisplacement.toFixed(9)}`);
	console.log(
		`ROSHAN_RESCULPT|INCOMPATIBLE_POINT_CONTACTS|${pointContactKeys.join(";")}`,
	);
	console.log(
		`ROSHAN_RESCULPT|MAXIMUM_RAW_WELD_SPREAD|${maximumRawWeldSpread.toFixed(9)}`,
	);
	console.log(
		`ROSHAN_RESCULPT|MAXIMUM_COMPATIBLE_RAW_WELD_SPREAD|${
			maximumCompatibleRawWeldSpread.toFixed(9)
		}`,
	);
	console.log(
		`ROSHAN_RESCULPT|UNAFFECTED_NORMALS_SHA256|${unaffectedNormalDigest}`,
	);
	console.log(
		`ROSHAN_RESCULPT|SOURCE_PRACTICAL_COMPONENTS|${sourceWeld.componentSizes.join(",")}`,
	);
	console.log(
		`ROSHAN_RESCULPT|PRACTICAL_COMPONENTS|${outputWeld.componentSizes.join(",")}`,
	);
	console.log(`ROSHAN_RESCULPT|OUTPUT|${outPath}`);
}

export {
	Glb,
	matrix3Vector,
	matrix4Identity,
	matrix4Inverse,
	matrix4Multiply,
	matrixTranslation,
	nodeGlobals,
	nodeLocal,
	quaternionMatrix,
	sha256,
	vectorAdd,
	vectorLength,
	vectorNormalize,
	vectorScale,
	vectorSub,
};

if (
	process.argv[1] &&
	import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
	main();
}
