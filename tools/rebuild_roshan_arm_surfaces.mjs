#!/usr/bin/env node
/**
 * Add continuous anatomical arm surfaces beneath Roshan v4's damaged arm
 * shells.  The Meshy remesh contains a usable positive-X hand/arm sculpt and
 * a decorated negative-X forearm/hand shell, but neither side has a dependable
 * shoulder-to-wrist skin surface under animation.  This deterministic pass
 * builds one low-cost, skinned tube per arm.  Each tube begins inside the
 * torso, blends across shoulder/elbow/wrist joints, and ends inside the hand.
 * The authored hands, sleeve/scale overlays, texture, and original topology
 * remain intact above the new anatomical underlay.
 *
 * Run from the repository root:
 *
 *   node tools/rebuild_roshan_arm_surfaces.mjs \
 *     --source assets/characters/roshan_v4.glb \
 *     --out audit/roshan_v4_cohesive_arms.glb
 */

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

import {
	Glb,
	matrixTranslation,
	nodeGlobals,
	vectorAdd,
	vectorLength,
	vectorNormalize,
	vectorScale,
	vectorSub,
} from "./resculpt_roshan_v4.mjs";

const EXPECTED_SOURCE_SHA256 =
	"9fefb159dc9262404056d97f2e4144754108ae6d5d77b2379e19f09e65d7fedf";
const EXPECTED_OUTPUT_SHA256 =
	"6e9db85f9388e8bacee1d423a6adca6d0fd1e9e14ddb76bc26593d1f931b82e9";
const EXPECTED_TEXTURE_SHA256 =
	"487c2409bcc5647b8d8f3cd5980d70e010d690de22c2968d99881490df55167d";
const SIDES = 14;
const SKIN_COLOUR = [0.79, 0.67, 0.61, 1.0];

function parseArgs(argv) {
	const result = {
		source: "assets/characters/roshan_v4.glb",
		out: "audit/roshan_v4_cohesive_arms.glb",
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

function dot(a, b) {
	return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function cross(a, b) {
	return [
		a[1] * b[2] - a[2] * b[1],
		a[2] * b[0] - a[0] * b[2],
		a[0] * b[1] - a[1] * b[0],
	];
}

function mix(a, b, t) {
	return vectorAdd(vectorScale(a, 1 - t), vectorScale(b, t));
}

function samePath(a, b) {
	return path.resolve(a).toLowerCase() === path.resolve(b).toLowerCase();
}

function alignedBuffer(buffer) {
	const padding = (4 - (buffer.length % 4)) % 4;
	return padding ? Buffer.concat([buffer, Buffer.alloc(padding)]) : buffer;
}

function bufferFromFloat32(values) {
	const buffer = Buffer.alloc(values.length * 4);
	for (let index = 0; index < values.length; index += 1) {
		buffer.writeFloatLE(Math.fround(values[index]), index * 4);
	}
	return buffer;
}

function bufferFromUint16(values) {
	const buffer = Buffer.alloc(values.length * 2);
	for (let index = 0; index < values.length; index += 1) {
		buffer.writeUInt16LE(values[index], index * 2);
	}
	return buffer;
}

function bufferFromUint8(values) {
	return Buffer.from(values);
}

function appendAccessor(glb, bytes, descriptor) {
	glb.binary = alignedBuffer(glb.binary);
	const byteOffset = glb.binary.length;
	glb.binary = Buffer.concat([glb.binary, bytes]);
	const bufferView = glb.gltf.bufferViews.length;
	glb.gltf.bufferViews.push({
		buffer: 0,
		byteOffset,
		byteLength: bytes.length,
		...(descriptor.target ? { target: descriptor.target } : {}),
	});
	const accessor = glb.gltf.accessors.length;
	glb.gltf.accessors.push({
		bufferView,
		byteOffset: 0,
		componentType: descriptor.componentType,
		count: descriptor.count,
		type: descriptor.type,
		...(descriptor.normalized ? { normalized: true } : {}),
		...(descriptor.min ? { min: descriptor.min } : {}),
		...(descriptor.max ? { max: descriptor.max } : {}),
	});
	glb.gltf.buffers[0].byteLength = glb.binary.length;
	return accessor;
}

function ringFrame(tangent) {
	let reference = [0, 0, 1];
	if (Math.abs(dot(tangent, reference)) > 0.92) {
		reference = [0, 1, 0];
	}
	const normal = vectorNormalize(cross(tangent, reference));
	const binormal = vectorNormalize(cross(tangent, normal));
	return { normal, binormal };
}

function chainRings(shoulder, elbow, wrist, names) {
	const upper = vectorSub(elbow, shoulder);
	const forearm = vectorSub(wrist, elbow);
	const upperLength = vectorLength(upper);
	const forearmLength = vectorLength(forearm);
	const upperDirection = vectorNormalize(upper);
	const forearmDirection = vectorNormalize(forearm);
	const elbowTangent = vectorNormalize(vectorAdd(upperDirection, forearmDirection));
	const start = vectorAdd(shoulder, vectorScale(upperDirection, -0.050));
	const end = vectorAdd(wrist, vectorScale(forearmDirection, 0.038));
	const rings = [
		{ center: start, radius: 0.061, tangent: upperDirection, weights: [["chest", 0.72], [names.upper, 0.28]] },
		{ center: vectorAdd(shoulder, vectorScale(upperDirection, -0.018)), radius: 0.058, tangent: upperDirection, weights: [["chest", 0.38], [names.upper, 0.62]] },
		{ center: vectorAdd(shoulder, vectorScale(upperDirection, 0.035)), radius: 0.052, tangent: upperDirection, weights: [[names.upper, 1.0]] },
		{ center: vectorAdd(shoulder, vectorScale(upperDirection, upperLength * 0.34)), radius: 0.047, tangent: upperDirection, weights: [[names.upper, 1.0]] },
		{ center: vectorAdd(shoulder, vectorScale(upperDirection, upperLength * 0.70)), radius: 0.043, tangent: upperDirection, weights: [[names.upper, 1.0]] },
		{ center: vectorAdd(shoulder, vectorScale(upperDirection, upperLength * 0.90)), radius: 0.042, tangent: mix(upperDirection, elbowTangent, 0.45), weights: [[names.upper, 0.82], [names.forearm, 0.18]] },
		{ center: elbow, radius: 0.043, tangent: elbowTangent, weights: [[names.upper, 0.50], [names.forearm, 0.50]] },
		{ center: vectorAdd(elbow, vectorScale(forearmDirection, forearmLength * 0.10)), radius: 0.042, tangent: mix(elbowTangent, forearmDirection, 0.55), weights: [[names.upper, 0.18], [names.forearm, 0.82]] },
		{ center: vectorAdd(elbow, vectorScale(forearmDirection, forearmLength * 0.40)), radius: 0.039, tangent: forearmDirection, weights: [[names.forearm, 1.0]] },
		{ center: vectorAdd(elbow, vectorScale(forearmDirection, forearmLength * 0.72)), radius: 0.036, tangent: forearmDirection, weights: [[names.forearm, 1.0]] },
		{ center: vectorAdd(elbow, vectorScale(forearmDirection, forearmLength * 0.92)), radius: 0.033, tangent: forearmDirection, weights: [[names.forearm, 0.82], [names.hand, 0.18]] },
		{ center: wrist, radius: 0.034, tangent: forearmDirection, weights: [[names.forearm, 0.50], [names.hand, 0.50]] },
		{ center: end, radius: 0.036, tangent: forearmDirection, weights: [[names.hand, 1.0]] },
	];
	return { rings, upperLength, forearmLength };
}

function buildArmSurface(chains, skinIndexByName) {
	const positions = [];
	const normals = [];
	const texcoords = [];
	const joints = [];
	const weights = [];
	const indices = [];
	const chainStats = [];

	function appendWeights(profile) {
		const jointRow = [0, 0, 0, 0];
		const weightRow = [0, 0, 0, 0];
		for (let slot = 0; slot < profile.length; slot += 1) {
			jointRow[slot] = skinIndexByName.get(profile[slot][0]);
			weightRow[slot] = profile[slot][1];
		}
		joints.push(...jointRow);
		weights.push(...weightRow);
	}

	for (const chain of chains) {
		const base = positions.length / 3;
		const generated = chainRings(chain.shoulder, chain.elbow, chain.wrist, chain);
		const rings = generated.rings;
		for (let ringIndex = 0; ringIndex < rings.length; ringIndex += 1) {
			const ring = rings[ringIndex];
			const frame = ringFrame(vectorNormalize(ring.tangent));
			for (let side = 0; side < SIDES; side += 1) {
				const angle = side / SIDES * Math.PI * 2;
				const radial = vectorAdd(
					vectorScale(frame.normal, Math.cos(angle)),
					vectorScale(frame.binormal, Math.sin(angle)),
				);
				positions.push(...vectorAdd(ring.center, vectorScale(radial, ring.radius)));
				normals.push(...radial);
				texcoords.push(side / SIDES, ringIndex / (rings.length - 1));
				appendWeights(ring.weights);
			}
		}
		for (let ring = 0; ring < rings.length - 1; ring += 1) {
			for (let side = 0; side < SIDES; side += 1) {
				const next = (side + 1) % SIDES;
				const a = base + ring * SIDES + side;
				const b = base + ring * SIDES + next;
				const c = base + (ring + 1) * SIDES + side;
				const d = base + (ring + 1) * SIDES + next;
				indices.push(a, c, b, b, c, d);
			}
		}
		for (const [ringIndex, direction] of [[0, -1], [rings.length - 1, 1]]) {
			const centerIndex = positions.length / 3;
			const ring = rings[ringIndex];
			positions.push(...ring.center);
			normals.push(...vectorScale(vectorNormalize(ring.tangent), direction));
			texcoords.push(0.5, ringIndex === 0 ? 0 : 1);
			appendWeights(ring.weights);
			for (let side = 0; side < SIDES; side += 1) {
				const next = (side + 1) % SIDES;
				const a = base + ringIndex * SIDES + side;
				const b = base + ringIndex * SIDES + next;
				if (direction < 0) {
					indices.push(centerIndex, b, a);
				} else {
					indices.push(centerIndex, a, b);
				}
			}
		}
		chainStats.push({
			label: chain.label,
			upperLength: generated.upperLength,
			forearmLength: generated.forearmLength,
			rings: rings.length,
		});
	}

	return { positions, normals, texcoords, joints, weights, indices, chainStats };
}

function bounds(values, components) {
	const min = new Array(components).fill(Infinity);
	const max = new Array(components).fill(-Infinity);
	for (let offset = 0; offset < values.length; offset += components) {
		for (let axis = 0; axis < components; axis += 1) {
			min[axis] = Math.min(min[axis], values[offset + axis]);
			max[axis] = Math.max(max[axis], values[offset + axis]);
		}
	}
	return { min, max };
}

function writeAtomic(outPath, bytes) {
	fs.mkdirSync(path.dirname(outPath), { recursive: true });
	const temporary = `${outPath}.${process.pid}.tmp`;
	fs.writeFileSync(temporary, bytes);
	fs.renameSync(temporary, outPath);
}

function removeDamagedArmTriangles(glb, primitive, jointNames, positiveWrist) {
	const position = glb.readAccessor(primitive.attributes.POSITION);
	const joints = glb.readAccessor(primitive.attributes.JOINTS_0, false);
	const weights = glb.readAccessor(primitive.attributes.WEIGHTS_0);
	const indexAccessor = glb.readAccessor(primitive.indices, false);
	const indexValues = indexAccessor.values;
	const skinIndexByName = new Map(jointNames.map((name, index) => [name, index]));
	const targetIndices = Object.fromEntries(
		["armU", "armF", "hand", "armU2", "armF2", "hand2"].map(
			(name) => [name, skinIndexByName.get(name)],
		),
	);

	function vertexWeight(vertex, skinIndex) {
		let result = 0;
		for (let slot = 0; slot < 4; slot += 1) {
			const offset = vertex * 4 + slot;
			if (Math.round(joints.values[offset]) === skinIndex) {
				result += weights.values[offset];
			}
		}
		return result;
	}

	const kept = [];
	let removedPositive = 0;
	let removedNegative = 0;
	for (let offset = 0; offset < indexValues.length; offset += 3) {
		const triangle = [0, 1, 2].map((corner) => Math.round(indexValues[offset + corner]));
		const average = {};
		for (const [name, skinIndex] of Object.entries(targetIndices)) {
			average[name] = triangle.reduce(
				(sum, vertex) => sum + vertexWeight(vertex, skinIndex), 0,
			) / 3;
		}
		const positiveSegments = average.armU + average.armF;
		const negativeChain = average.armU2 + average.armF2 + average.hand2;
		const centroid = [0, 1, 2].map((axis) => triangle.reduce(
			(sum, vertex) => sum + position.values[vertex * 3 + axis], 0,
		) / 3);
		const nearPositivePalm = vectorLength(vectorSub(centroid, positiveWrist)) < 0.085;
		const dropPositive =
			positiveSegments > 0.35 && average.hand < 0.08 && !nearPositivePalm;
		// The independent negative-X upper-arm decoration is overwhelmingly
		// armU2-weighted.  Remove it along with the torn upper-arm skin while
		// retaining the authored forearm-scale sleeve and hand shell.
		const dropNegative =
			negativeChain > 0.72 && average.armU2 > 0.05 && average.hand2 < 0.35;
		if (dropPositive || dropNegative) {
			if (dropPositive) removedPositive += 1;
			if (dropNegative) removedNegative += 1;
			continue;
		}
		kept.push(...triangle);
	}
	if (removedPositive < 300 || removedNegative < 150) {
		throw new Error(
			`Arm cleanup selected too little geometry: ${removedPositive}/${removedNegative}`,
		);
	}
	const info = glb.accessorInfo(primitive.indices);
	if (info.accessor.componentType !== 5123 || kept.length > info.count) {
		throw new Error("Unexpected source index accessor contract");
	}
	const encoded = bufferFromUint16(kept);
	encoded.copy(glb.binary, info.start);
	info.accessor.count = kept.length;
	info.accessor.min = [0];
	info.accessor.max = [position.count - 1];
	return {
		keptTriangles: kept.length / 3,
		removedPositive,
		removedNegative,
	};
}

function main() {
	const args = parseArgs(process.argv);
	const sourcePath = path.resolve(args.source);
	const outPath = path.resolve(args.out);
	if (samePath(sourcePath, outPath) && !args.inPlace) {
		throw new Error("Refusing to overwrite --source without --in-place");
	}
	const sourceBytes = fs.readFileSync(sourcePath);
	const sourceHash = sha256(sourceBytes);
	if (sourceHash === EXPECTED_OUTPUT_SHA256) {
		if (!samePath(sourcePath, outPath)) {
			writeAtomic(outPath, sourceBytes);
		}
		console.log(`ROSHAN_ARM_SURFACE|SOURCE_ALREADY_FINAL|${sourceHash}`);
		console.log(`ROSHAN_ARM_SURFACE|OUTPUT|${outPath}`);
		return;
	}
	if (sourceHash !== EXPECTED_SOURCE_SHA256) {
		throw new Error(`Unexpected source SHA-256 ${sourceHash}`);
	}
	const glb = new Glb(sourceBytes, "Roshan v4 cohesive-arm source");
	if (glb.gltf.meshes?.length !== 1 || glb.gltf.skins?.length !== 1) {
		throw new Error("Expected Roshan's one-mesh/one-skin GLB contract");
	}
	const images = glb.imagePayloads();
	if (images.length !== 1 || sha256(images[0]) !== EXPECTED_TEXTURE_SHA256) {
		throw new Error("Embedded Roshan texture changed or is missing");
	}
	const skin = glb.gltf.skins[0];
	const jointNames = skin.joints.map((node) => glb.gltf.nodes[node].name || "");
	const skinIndexByName = new Map(jointNames.map((name, index) => [name, index]));
	const nodeIndexByName = new Map(
		glb.gltf.nodes.map((node, index) => [node.name, index]).filter(([name]) => Boolean(name)),
	);
	for (const name of ["chest", "armU", "armF", "hand", "armU2", "armF2", "hand2"]) {
		if (!skinIndexByName.has(name) || !nodeIndexByName.has(name)) {
			throw new Error(`Required joint is missing: ${name}`);
		}
	}
	const globals = nodeGlobals(glb.gltf);
	const jointPoint = (name) => matrixTranslation(globals[nodeIndexByName.get(name)]);
	const chains = [
		{ label: "positive_x", upper: "armU", forearm: "armF", hand: "hand" },
		{ label: "negative_x", upper: "armU2", forearm: "armF2", hand: "hand2" },
	].map((chain) => ({
		...chain,
		shoulder: jointPoint(chain.upper),
		elbow: jointPoint(chain.forearm),
		wrist: jointPoint(chain.hand),
	}));
	const sourcePrimitive = glb.gltf.meshes[0].primitives[0];
	const cleanup = removeDamagedArmTriangles(
		glb, sourcePrimitive, jointNames, chains[0].wrist,
	);
	const surface = buildArmSurface(chains, skinIndexByName);
	const vertexCount = surface.positions.length / 3;
	if (vertexCount >= 65536) {
		throw new Error("Generated arm surface exceeded uint16 index range");
	}
	const positionBounds = bounds(surface.positions, 3);
	const positionAccessor = appendAccessor(glb, bufferFromFloat32(surface.positions), {
		componentType: 5126, count: vertexCount, type: "VEC3", target: 34962,
		min: positionBounds.min, max: positionBounds.max,
	});
	const normalAccessor = appendAccessor(glb, bufferFromFloat32(surface.normals), {
		componentType: 5126, count: vertexCount, type: "VEC3", target: 34962,
	});
	const texcoordAccessor = appendAccessor(glb, bufferFromFloat32(surface.texcoords), {
		componentType: 5126, count: vertexCount, type: "VEC2", target: 34962,
	});
	const jointAccessor = appendAccessor(glb, bufferFromUint8(surface.joints), {
		componentType: 5121, count: vertexCount, type: "VEC4", target: 34962,
	});
	const weightAccessor = appendAccessor(glb, bufferFromFloat32(surface.weights), {
		componentType: 5126, count: vertexCount, type: "VEC4", target: 34962,
	});
	const indexAccessor = appendAccessor(glb, bufferFromUint16(surface.indices), {
		componentType: 5123, count: surface.indices.length, type: "SCALAR", target: 34963,
		min: [0], max: [vertexCount - 1],
	});
	const materialIndex = glb.gltf.materials.length;
	glb.gltf.materials.push({
		name: "Roshan_Cohesive_Arm_Skin",
		doubleSided: false,
		pbrMetallicRoughness: {
			baseColorFactor: SKIN_COLOUR,
			metallicFactor: 0,
			roughnessFactor: 0.72,
		},
	});
	glb.gltf.meshes[0].primitives.push({
		attributes: {
			POSITION: positionAccessor,
			NORMAL: normalAccessor,
			TEXCOORD_0: texcoordAccessor,
			JOINTS_0: jointAccessor,
			WEIGHTS_0: weightAccessor,
		},
		indices: indexAccessor,
		material: materialIndex,
		extras: { purpose: "continuous shoulder-elbow-wrist anatomical underlay" },
	});
	glb.gltf.asset.extras = {
		...(glb.gltf.asset.extras || {}),
		roshanCohesiveArmSurface: {
			version: 1,
			sides: SIDES,
			vertexCount,
			triangleCount: surface.indices.length / 3,
		},
	};
	const outputBytes = glb.toBuffer();
	const outputHash = sha256(outputBytes);
	if (outputHash !== EXPECTED_OUTPUT_SHA256) {
		throw new Error(
			`Cohesive-arm output ${outputHash} differs from audited ${EXPECTED_OUTPUT_SHA256}`,
		);
	}
	writeAtomic(outPath, outputBytes);
	console.log(`ROSHAN_ARM_SURFACE|SOURCE_SHA256|${sourceHash}`);
	console.log(`ROSHAN_ARM_SURFACE|OUTPUT_SHA256|${outputHash}`);
	console.log(`ROSHAN_ARM_SURFACE|TEXTURE_SHA256|${sha256(glb.imagePayloads()[0])}`);
	console.log(`ROSHAN_ARM_SURFACE|VERTICES|${vertexCount}`);
	console.log(`ROSHAN_ARM_SURFACE|TRIANGLES|${surface.indices.length / 3}`);
	console.log(
		`ROSHAN_ARM_SURFACE|REMOVED_DAMAGED_TRIANGLES|` +
		`positive=${cleanup.removedPositive}|negative=${cleanup.removedNegative}|` +
		`kept=${cleanup.keptTriangles}`,
	);
	for (const stat of surface.chainStats) {
		console.log(
			`ROSHAN_ARM_SURFACE|${stat.label.toUpperCase()}|` +
			`upper=${stat.upperLength.toFixed(9)}|forearm=${stat.forearmLength.toFixed(9)}|rings=${stat.rings}`,
		);
	}
	console.log(`ROSHAN_ARM_SURFACE|OUTPUT|${outPath}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
	main();
}
