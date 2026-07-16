#!/usr/bin/env node
/**
 * Rebuild the deforming hair layer on the cohesive Mermaid Roshan sculpt.
 *
 * The v5 anatomy repair intentionally shipped with static hair weights while
 * its arm/skin deformation was being isolated. That stopped old hair weights
 * from capturing the face and dress, but it also made all 24 strand bones
 * visually inert. Their generated rest chains were additionally non-monotonic.
 *
 * This deterministic pass changes only:
 *   - the 24 existing hair joint rests and inverse bind matrices; and
 *   - weights on verified, disconnected hair-lock topology components.
 *
 * Positions, indices, normals, UVs, materials, embedded texture bytes, the
 * repaired body weights, and the hidden arm seam underlay remain unchanged.
 * Component ranks below were classified once against the embedded texture and
 * are safe because the exact source GLB hash and topology are pinned.
 *
 * Run from the repository root:
 *
 *   node tools/rebuild_roshan_hair_physics.mjs \
 *     --source assets/characters/roshan_v4.glb \
 *     --out audit/roshan_hair_physics.glb
 *
 * Use --in-place only after auditing the generated candidate.
 */

import fs from "node:fs";
import path from "node:path";

import {
	Glb,
	matrix4Inverse,
	matrixTranslation,
	nodeGlobals,
	sha256,
} from "./resculpt_roshan_v4.mjs";

const EXPECTED_SOURCE_SHA256 =
	"478eaf479d6cda1e08de6f7e27a1f5b7d7b48d158a77e8745c3527aca65fb86e";
const EXPECTED_OUTPUT_SHA256 =
	"9a2ff09680b344625c34523cc6c0f76e82a2c95680610b77a95673c5450b2029";
const EXPECTED_PRIMARY_VERTICES = 27836;
const EXPECTED_COMPONENT_COUNT = 140;
const EXPECTED_IMAGE_SHA256 = [
	"90d40c67c57603d3cab6a8c9a3d88f4fc69322efaf001b2b07c14e5414f259b2",
	"d25ec8e72c8c4bf1cff736b40865d7d1d1e286cc7f9393758882e0d932350ad5",
];

// Topology-component ranks on the pinned source, sorted largest first. These
// are the movable brown/rainbow locks. Central scalp/crown components remain
// head-bound; small front-facing facial components are deliberately excluded.
const HAIR_COMPONENT_RANKS = new Set([
	4, 9, 17, 22, 23, 24, 28, 31, 32, 38, 39, 42, 49, 50, 52, 55, 56,
	57, 58, 60, 65, 67, 69, 70, 71, 72, 75, 76, 77, 78, 80, 88, 89, 90,
	91, 92, 98, 101, 104, 112, 113, 118, 119, 120,
]);

// Global-space joint points. Each chain runs monotonically from a stable scalp
// root to a free lock tip. The fan follows the sculpt: two rainbow locks sweep
// left, four locks trail behind the head, and two frame the right side.
const HAIR_CHAINS = [
	[[-0.20, 0.70, -0.02], [-0.39, 0.56, -0.05], [-0.57, 0.37, -0.09]],
	[[-0.18, 0.65, -0.09], [-0.36, 0.49, -0.12], [-0.53, 0.32, -0.11]],
	[[-0.16, 0.68, 0.11], [-0.25, 0.50, 0.17], [-0.27, 0.29, 0.13]],
	[[-0.09, 0.69, 0.22], [-0.14, 0.50, 0.29], [-0.11, 0.29, 0.29]],
	[[0.00, 0.70, 0.27], [0.00, 0.50, 0.34], [0.00, 0.29, 0.34]],
	[[0.10, 0.69, 0.21], [0.14, 0.50, 0.25], [0.14, 0.29, 0.21]],
	[[0.18, 0.68, 0.08], [0.22, 0.50, 0.08], [0.24, 0.32, 0.11]],
	[[0.18, 0.66, -0.03], [0.20, 0.50, -0.02], [0.16, 0.36, -0.08]],
];

function parseArgs(argv) {
	const args = {
		source: "assets/characters/roshan_v4.glb",
		out: "audit/roshan_hair_physics.glb",
		inPlace: false,
	};
	for (let index = 2; index < argv.length; index += 1) {
		const argument = argv[index];
		if (argument === "--source" || argument === "--out") {
			if (index + 1 >= argv.length) throw new Error(`${argument} requires a path`);
			args[argument.slice(2)] = argv[index + 1];
			index += 1;
		} else if (argument === "--in-place") {
			args.inPlace = true;
		} else {
			throw new Error(`Unknown argument: ${argument}`);
		}
	}
	if (path.resolve(args.source) === path.resolve(args.out) && !args.inPlace) {
		throw new Error("Source and output match; pass --in-place explicitly");
	}
	return args;
}

function vectorSub(a, b) {
	return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
}

function vectorAdd(a, b) {
	return [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
}

function vectorScale(a, scale) {
	return [a[0] * scale, a[1] * scale, a[2] * scale];
}

function dot(a, b) {
	return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

function lengthSquared(a) {
	return dot(a, a);
}

function distanceSquared(a, b) {
	return lengthSquared(vectorSub(a, b));
}

function transformPoint(matrix, point) {
	return [
		matrix[0] * point[0] + matrix[1] * point[1] + matrix[2] * point[2] + matrix[3],
		matrix[4] * point[0] + matrix[5] * point[1] + matrix[6] * point[2] + matrix[7],
		matrix[8] * point[0] + matrix[9] * point[1] + matrix[10] * point[2] + matrix[11],
	];
}

function nearestOnChain(point, chain) {
	const segmentLengths = [
		Math.sqrt(distanceSquared(chain[0], chain[1])),
		Math.sqrt(distanceSquared(chain[1], chain[2])),
	];
	const totalLength = segmentLengths[0] + segmentLengths[1];
	let best = { distanceSquared: Infinity, progress: 0 };
	let preceding = 0;
	for (let segment = 0; segment < 2; segment += 1) {
		const start = chain[segment];
		const span = vectorSub(chain[segment + 1], start);
		const alpha = Math.max(0, Math.min(1,
			dot(vectorSub(point, start), span) / Math.max(lengthSquared(span), 1e-12),
		));
		const closest = vectorAdd(start, vectorScale(span, alpha));
		const candidate = {
			distanceSquared: distanceSquared(point, closest),
			progress: (preceding + alpha * segmentLengths[segment]) / totalLength,
		};
		if (candidate.distanceSquared < best.distanceSquared) best = candidate;
		preceding += segmentLengths[segment];
	}
	return best;
}

function smoothstep(edge0, edge1, value) {
	const t = Math.max(0, Math.min(1, (value - edge0) / (edge1 - edge0)));
	return t * t * (3 - 2 * t);
}

function topologyComponents(vertexCount, indices) {
	const parent = Array.from({ length: vertexCount }, (_, index) => index);
	function find(index) {
		while (parent[index] !== index) {
			parent[index] = parent[parent[index]];
			index = parent[index];
		}
		return index;
	}
	function union(a, b) {
		const left = find(a);
		const right = find(b);
		if (left !== right) parent[right] = left;
	}
	for (let offset = 0; offset < indices.length; offset += 3) {
		union(Math.round(indices[offset]), Math.round(indices[offset + 1]));
		union(Math.round(indices[offset + 1]), Math.round(indices[offset + 2]));
	}
	const groups = new Map();
	for (let vertex = 0; vertex < vertexCount; vertex += 1) {
		const root = find(vertex);
		if (!groups.has(root)) groups.set(root, []);
		groups.get(root).push(vertex);
	}
	return [...groups.values()].sort((a, b) => b.length - a.length);
}

function componentCentroid(vertices, positions) {
	const result = [0, 0, 0];
	for (const vertex of vertices) {
		for (let axis = 0; axis < 3; axis += 1) {
			result[axis] += positions.values[vertex * 3 + axis];
		}
	}
	return result.map((value) => value / vertices.length);
}

function writeAtomic(filePath, bytes) {
	fs.mkdirSync(path.dirname(filePath), { recursive: true });
	const temporary = `${filePath}.tmp-${process.pid}`;
	fs.writeFileSync(temporary, bytes);
	fs.renameSync(temporary, filePath);
}

function main() {
	const args = parseArgs(process.argv);
	const sourceBytes = fs.readFileSync(args.source);
	const sourceHash = sha256(sourceBytes);
	if (sourceHash !== EXPECTED_SOURCE_SHA256) {
		throw new Error(`Source SHA-256 ${sourceHash} is not the audited cohesive sculpt`);
	}
	const glb = new Glb(sourceBytes, args.source);
	const images = glb.imagePayloads();
	const imageHashes = images.map((payload) => sha256(payload));
	if (JSON.stringify(imageHashes) !== JSON.stringify(EXPECTED_IMAGE_SHA256)) {
		throw new Error(`Embedded textures changed: ${imageHashes.join(",")}`);
	}

	const primitive = glb.gltf.meshes[0].primitives[0];
	const positions = glb.readAccessor(primitive.attributes.POSITION);
	const joints = glb.readAccessor(primitive.attributes.JOINTS_0, false);
	const weights = glb.readAccessor(primitive.attributes.WEIGHTS_0);
	const indices = glb.readAccessor(primitive.indices, false);
	if (positions.count !== EXPECTED_PRIMARY_VERTICES) {
		throw new Error(`Unexpected primary vertex count: ${positions.count}`);
	}
	const components = topologyComponents(positions.count, indices.values);
	if (components.length !== EXPECTED_COMPONENT_COUNT) {
		throw new Error(`Unexpected topology component count: ${components.length}`);
	}
	for (const rank of HAIR_COMPONENT_RANKS) {
		if (rank >= components.length) throw new Error(`Missing hair component rank ${rank}`);
	}

	const skin = glb.gltf.skins[0];
	const skinNames = skin.joints.map((node) => glb.gltf.nodes[node].name || "");
	const skinIndexByName = new Map(skinNames.map((name, index) => [name, index]));
	const nodeIndexByName = new Map(glb.gltf.nodes.map((node, index) => [node.name, index]));
	const headSkinIndex = skinIndexByName.get("head");
	if (headSkinIndex === undefined) throw new Error("Missing head joint");
	for (let strand = 0; strand < HAIR_CHAINS.length; strand += 1) {
		for (let segment = 0; segment < 3; segment += 1) {
			const name = `hair_${String(strand).padStart(2, "0")}_${segment}`;
			if (!skinIndexByName.has(name) || !nodeIndexByName.has(name)) {
				throw new Error(`Missing strand joint ${name}`);
			}
		}
	}

	// The source is expected to be the deliberately static-hair v5 bind.
	let oldStrandWeight = 0;
	for (let vertex = 0; vertex < joints.count; vertex += 1) {
		for (let slot = 0; slot < 4; slot += 1) {
			const skinIndex = Math.round(joints.values[vertex * 4 + slot]);
			if (/^hair_\d\d_\d$/.test(skinNames[skinIndex] || "")) {
				oldStrandWeight += weights.values[vertex * 4 + slot];
			}
		}
	}
	if (oldStrandWeight > 1e-6) {
		throw new Error(`Source already has ${oldStrandWeight} total strand weight`);
	}

	// Re-key each existing chain as a clean monotonic fan. Identity local rests
	// inherit the head basis, eliminating the arbitrary generated local axes.
	for (let strand = 0; strand < HAIR_CHAINS.length; strand += 1) {
		for (let segment = 0; segment < 3; segment += 1) {
			const name = `hair_${String(strand).padStart(2, "0")}_${segment}`;
			const nodeIndex = nodeIndexByName.get(name);
			const parents = new Map();
			for (let parent = 0; parent < glb.gltf.nodes.length; parent += 1) {
				for (const child of glb.gltf.nodes[parent].children || []) parents.set(child, parent);
			}
			const parentIndex = parents.get(nodeIndex);
			if (parentIndex === undefined) throw new Error(`${name} has no parent`);
			const globals = nodeGlobals(glb.gltf);
			const parentInverse = matrix4Inverse(globals[parentIndex]);
			const node = glb.gltf.nodes[nodeIndex];
			delete node.matrix;
			delete node.scale;
			node.translation = transformPoint(parentInverse, HAIR_CHAINS[strand][segment]);
			node.rotation = [0, 0, 0, 1];
		}
	}
	const cleanGlobals = nodeGlobals(glb.gltf);
	let maximumJointError = 0;
	for (let strand = 0; strand < HAIR_CHAINS.length; strand += 1) {
		for (let segment = 0; segment < 3; segment += 1) {
			const name = `hair_${String(strand).padStart(2, "0")}_${segment}`;
			const actual = matrixTranslation(cleanGlobals[nodeIndexByName.get(name)]);
			maximumJointError = Math.max(
				maximumJointError,
				Math.sqrt(distanceSquared(actual, HAIR_CHAINS[strand][segment])),
			);
		}
	}
	if (maximumJointError > 2e-6) {
		throw new Error(`Rebuilt chain missed target by ${maximumJointError}`);
	}

	// Assign every disconnected lock to one chain by its centroid, then grade
	// its vertices from stable head/root weighting to free tip weighting.
	const newJoints = new Float64Array(joints.values);
	const newWeights = new Float64Array(weights.values);
	const chainVertexCounts = new Uint32Array(HAIR_CHAINS.length);
	let selectedVertices = 0;
	for (const rank of [...HAIR_COMPONENT_RANKS].sort((a, b) => a - b)) {
		const vertices = components[rank];
		const centroid = componentCentroid(vertices, positions);
		let strand = 0;
		let bestDistance = Infinity;
		for (let candidate = 0; candidate < HAIR_CHAINS.length; candidate += 1) {
			const hit = nearestOnChain(centroid, HAIR_CHAINS[candidate]);
			if (hit.distanceSquared < bestDistance) {
				bestDistance = hit.distanceSquared;
				strand = candidate;
			}
		}
		const hairSkinIndices = [0, 1, 2].map((segment) =>
			skinIndexByName.get(`hair_${String(strand).padStart(2, "0")}_${segment}`),
		);
		for (const vertex of vertices) {
			const point = [
				positions.values[vertex * 3],
				positions.values[vertex * 3 + 1],
				positions.values[vertex * 3 + 2],
			];
			const progress = nearestOnChain(point, HAIR_CHAINS[strand]).progress;
			const headWeight = 0.08 + 0.72 * (1 - smoothstep(0.0, 0.88, progress));
			const hairWeight = 1 - headWeight;
			const scaled = progress * 2;
			const lower = Math.min(1, Math.floor(scaled));
			const blend = Math.min(1, scaled - lower);
			const upper = lower + 1;
			const assignments = [
				[headSkinIndex, headWeight],
				[hairSkinIndices[lower], hairWeight * (1 - blend)],
				[hairSkinIndices[upper], hairWeight * blend],
				[headSkinIndex, 0],
			].sort((a, b) => b[1] - a[1]);
			for (let slot = 0; slot < 4; slot += 1) {
				newJoints[vertex * 4 + slot] = assignments[slot][0];
				newWeights[vertex * 4 + slot] = assignments[slot][1];
			}
			selectedVertices += 1;
			chainVertexCounts[strand] += 1;
		}
	}
	if (selectedVertices < 7000 || selectedVertices > 9000) {
		throw new Error(`Unexpected selected hair vertex count: ${selectedVertices}`);
	}
	if ([...chainVertexCounts].some((count) => count < 100)) {
		throw new Error(`A strand chain is underused: ${[...chainVertexCounts].join(",")}`);
	}
	glb.writeAccessor(primitive.attributes.JOINTS_0, newJoints);
	glb.writeAccessor(primitive.attributes.WEIGHTS_0, newWeights);

	// Rebuild every inverse bind from the updated rest hierarchy. Writing all
	// joints avoids assumptions about matrix accessor packing and keeps the skin
	// internally self-consistent.
	const globalsAfter = nodeGlobals(glb.gltf);
	const inverseBinds = new Float64Array(skin.joints.length * 16);
	for (let joint = 0; joint < skin.joints.length; joint += 1) {
		const inverse = matrix4Inverse(globalsAfter[skin.joints[joint]]);
		for (let row = 0; row < 4; row += 1) {
			for (let column = 0; column < 4; column += 1) {
				// glTF MAT4 accessor storage is column-major.
				inverseBinds[joint * 16 + column * 4 + row] = inverse[row * 4 + column];
			}
		}
	}
	glb.writeAccessor(skin.inverseBindMatrices, inverseBinds);

	const outputBytes = glb.toBuffer();
	const outputHash = sha256(outputBytes);
	if (EXPECTED_OUTPUT_SHA256 && outputHash !== EXPECTED_OUTPUT_SHA256) {
		throw new Error(`Output ${outputHash} differs from audited ${EXPECTED_OUTPUT_SHA256}`);
	}
	writeAtomic(args.out, outputBytes);
	console.log(`ROSHAN_HAIR|SOURCE_SHA256|${sourceHash}`);
	console.log(`ROSHAN_HAIR|OUTPUT_SHA256|${outputHash}`);
	console.log(`ROSHAN_HAIR|SELECTED_VERTICES|${selectedVertices}`);
	console.log(`ROSHAN_HAIR|CHAIN_VERTICES|${[...chainVertexCounts].join(",")}`);
	console.log(`ROSHAN_HAIR|MAXIMUM_JOINT_ERROR|${maximumJointError.toExponential(3)}`);
	console.log(`ROSHAN_HAIR|TEXTURES_SHA256|${imageHashes.join(",")}`);
	console.log(`ROSHAN_HAIR|OUTPUT|${args.out}`);
}

try {
	main();
} catch (error) {
	console.error(`ROSHAN_HAIR|ERROR|${error.stack || error.message}`);
	process.exitCode = 1;
}
