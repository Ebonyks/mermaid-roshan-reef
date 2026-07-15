#!/usr/bin/env python3
"""Repair Mermaid Roshan v4's regressed anatomical-left arm binding.

The original shipping v4g mesh still contained the complete left hand.  The
historical v4f/v4g patch changed only arm joint translations, inverse binds,
weights, and the embedded texture; it reassigned most of that hand to torso
bones.  This tool keeps the shipping geometry, topology, UVs, normals, material,
and embedded v4g JPEG byte-for-byte while using the pre-regression v4e skin as a
weight-label donor.  It then anchors only the proximal shoulder back to the
chest, with a smooth 75%-to-0% blend, and installs a conservative arm chain
fitted to the recovered geometry.  It accepts either the audited original v4g
or its own repaired output, making the checked-in result idempotently
reproducible.

By default the donor is read directly from Git revision b0b469c, so no second
3.3 MB character asset needs to be committed.  A full-history clone is required;
``--reference`` can instead name an extracted donor GLB.

Run from the repository root with Blender's bundled Python (NumPy required)::

    python tools/repair_roshan_v4.py \
      --source assets/characters/roshan_v4.glb \
      --out audit/roshan_v4_repaired.glb

The output must be audited before it replaces the shipping GLB.  This script
refuses to overwrite its input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import subprocess
from pathlib import Path
from typing import Any

import numpy as np


REFERENCE_REVISION = "b0b469c"
REFERENCE_PATH = "assets/characters/roshan_v4.glb"
LEFT_BONES = ("armU", "armF", "hand")
EXPECTED_SOURCE_SHA256 = "3537c1fa27f2c048c587fb9062a3e32846c61552fd949931791f9b76e6a5275b"
EXPECTED_REFERENCE_SHA256 = "18ee1c6df47193ca0eaebedfd4240005f7b601315d3a6f67fe312e757ec0f2b0"
EXPECTED_REPAIRED_SHA256 = "b50862c4117c9413d9242b81c9275dc9538733f6c63510cb8473ea208e450dbf"
EXPECTED_IMAGE_SHA256 = "487c2409bcc5647b8d8f3cd5980d70e010d690de22c2968d99881490df55167d"

# Exact local translations obtained by fitting the restored v4e arm labels to
# the unchanged v4g mesh.  Rest rotations, scales, names, and hierarchy stay put.
REPAIRED_LOCAL_TRANSLATIONS = {
	"armU": np.array(
		[0.1552937205319882, 0.15699066077863982, -0.06276322354713888],
		dtype=np.float64,
	),
	"armF": np.array(
		[-0.028527527390962648, 0.17458317750132946, -0.01655686804843512],
		dtype=np.float64,
	),
	"hand": np.array(
		[-1.629814508e-08, 0.17057174444198617, -1.388e-17],
		dtype=np.float64,
	),
}

REPAIRED_GLOBAL_SHOULDER = np.array(
	[0.12, 0.0704244512608305, -0.06086486414895169], dtype=np.float64
)
REPAIRED_GLOBAL_ELBOW = np.array(
	[0.1731409314347682, -0.07151832115716142, -0.1535768048681016],
	dtype=np.float64,
)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--source", default="assets/characters/roshan_v4.glb")
	parser.add_argument("--out", default="audit/roshan_v4_repaired.glb")
	parser.add_argument(
		"--reference",
		help="Optional path to the b0b469c pre-regression donor GLB",
	)
	parser.add_argument("--reference-revision", default=REFERENCE_REVISION)
	return parser.parse_args()


def sha256(data: bytes) -> str:
	return hashlib.sha256(data).hexdigest()


class Glb:
	COMPONENT_DTYPES = {
		5120: np.int8,
		5121: np.uint8,
		5122: np.int16,
		5123: np.uint16,
		5125: np.uint32,
		5126: np.float32,
	}
	COMPONENTS = {
		"SCALAR": 1,
		"VEC2": 2,
		"VEC3": 3,
		"VEC4": 4,
		"MAT4": 16,
	}

	def __init__(self, data: bytes, label: str) -> None:
		if len(data) < 28 or data[:4] != b"glTF":
			raise ValueError(f"{label}: not a GLB 2 file")
		magic, version, declared_length = struct.unpack_from("<4sII", data, 0)
		if magic != b"glTF" or version != 2 or declared_length != len(data):
			raise ValueError(f"{label}: invalid GLB header")
		json_length, json_type = struct.unpack_from("<II", data, 12)
		if json_type != 0x4E4F534A:
			raise ValueError(f"{label}: first chunk is not JSON")
		self.gltf = json.loads(data[20 : 20 + json_length])
		binary_header = 20 + json_length
		binary_length, binary_type = struct.unpack_from("<II", data, binary_header)
		if binary_type != 0x004E4942:
			raise ValueError(f"{label}: second chunk is not BIN")
		self.binary = bytearray(
			data[binary_header + 8 : binary_header + 8 + binary_length]
		)
		self.label = label

	def accessor(self, accessor_index: int, normalized: bool = True) -> np.ndarray:
		accessor = self.gltf["accessors"][accessor_index]
		view = self.gltf["bufferViews"][accessor["bufferView"]]
		dtype = self.COMPONENT_DTYPES[int(accessor["componentType"])]
		components = self.COMPONENTS[accessor["type"]]
		count = int(accessor["count"])
		start = int(view.get("byteOffset", 0)) + int(accessor.get("byteOffset", 0))
		element_bytes = np.dtype(dtype).itemsize * components
		stride = int(view.get("byteStride", element_bytes))
		if stride == element_bytes:
			array = np.frombuffer(
				self.binary,
				dtype=dtype,
				count=count * components,
				offset=start,
			).reshape((count, components))
		else:
			array = np.ndarray(
				shape=(count, components),
				dtype=dtype,
				buffer=self.binary,
				offset=start,
				strides=(stride, np.dtype(dtype).itemsize),
			)
		array = array.copy()
		if normalized and accessor.get("normalized", False) and not np.issubdtype(
			dtype, np.floating
		):
			array = array.astype(np.float64)
			if np.issubdtype(dtype, np.unsignedinteger):
				array /= float(np.iinfo(dtype).max)
			else:
				array = np.maximum(array / float(np.iinfo(dtype).max), -1.0)
		return array[:, 0] if components == 1 else array

	def write_accessor(self, accessor_index: int, values: np.ndarray) -> None:
		accessor = self.gltf["accessors"][accessor_index]
		view = self.gltf["bufferViews"][accessor["bufferView"]]
		dtype = self.COMPONENT_DTYPES[int(accessor["componentType"])]
		components = self.COMPONENTS[accessor["type"]]
		count = int(accessor["count"])
		array = np.asarray(values)
		if array.shape != (count, components):
			raise ValueError(
				f"{self.label}: accessor {accessor_index} shape {array.shape} != "
				f"{(count, components)}"
			)
		if accessor.get("normalized", False) and not np.issubdtype(dtype, np.floating):
			if np.issubdtype(dtype, np.unsignedinteger):
				array = np.rint(np.clip(array, 0.0, 1.0) * np.iinfo(dtype).max)
			else:
				array = np.rint(np.clip(array, -1.0, 1.0) * np.iinfo(dtype).max)
		array = array.astype(dtype)
		start = int(view.get("byteOffset", 0)) + int(accessor.get("byteOffset", 0))
		element_bytes = np.dtype(dtype).itemsize * components
		stride = int(view.get("byteStride", element_bytes))
		if stride == element_bytes:
			payload = array.reshape(-1).tobytes()
			self.binary[start : start + len(payload)] = payload
		else:
			for row in range(count):
				payload = array[row].tobytes()
				row_start = start + row * stride
				self.binary[row_start : row_start + element_bytes] = payload

	def image_payloads(self) -> list[bytes]:
		payloads = []
		for image in self.gltf.get("images", []):
			if "bufferView" not in image:
				continue
			view = self.gltf["bufferViews"][int(image["bufferView"])]
			start = int(view.get("byteOffset", 0))
			payloads.append(bytes(self.binary[start : start + int(view["byteLength"])]))
		return payloads

	def to_bytes(self) -> bytes:
		json_bytes = json.dumps(
			self.gltf, separators=(",", ":"), ensure_ascii=False
		).encode("utf-8")
		while len(json_bytes) % 4:
			json_bytes += b" "
		while len(self.binary) % 4:
			self.binary.append(0)
		total = 12 + 8 + len(json_bytes) + 8 + len(self.binary)
		return b"".join(
			[
				struct.pack("<4sII", b"glTF", 2, total),
				struct.pack("<II", len(json_bytes), 0x4E4F534A),
				json_bytes,
				struct.pack("<II", len(self.binary), 0x004E4942),
				bytes(self.binary),
			]
		)


def load_reference(args: argparse.Namespace) -> bytes:
	if args.reference:
		return Path(args.reference).resolve().read_bytes()
	result = subprocess.run(
		["git", "show", f"{args.reference_revision}:{REFERENCE_PATH}"],
		check=False,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
	)
	if result.returncode != 0:
		detail = result.stderr.decode("utf-8", errors="replace").strip()
		raise RuntimeError(
			"Unable to read the pre-regression donor from Git history. Pass "
			f"--reference explicitly. git show said: {detail}"
		)
	return result.stdout


def quat_matrix(quaternion: np.ndarray) -> np.ndarray:
	x, y, z, w = quaternion
	return np.array(
		[
			[1.0 - 2.0 * (y * y + z * z), 2.0 * (x * y - z * w), 2.0 * (x * z + y * w)],
			[2.0 * (x * y + z * w), 1.0 - 2.0 * (x * x + z * z), 2.0 * (y * z - x * w)],
			[2.0 * (x * z - y * w), 2.0 * (y * z + x * w), 1.0 - 2.0 * (x * x + y * y)],
		],
		dtype=np.float64,
	)


def node_local(node: dict[str, Any]) -> np.ndarray:
	if "matrix" in node:
		return np.asarray(node["matrix"], dtype=np.float64).reshape(4, 4).T
	translation = np.asarray(node.get("translation", [0.0, 0.0, 0.0]), dtype=np.float64)
	rotation = np.asarray(node.get("rotation", [0.0, 0.0, 0.0, 1.0]), dtype=np.float64)
	scale = np.asarray(node.get("scale", [1.0, 1.0, 1.0]), dtype=np.float64)
	matrix = np.eye(4, dtype=np.float64)
	matrix[:3, :3] = quat_matrix(rotation) @ np.diag(scale)
	matrix[:3, 3] = translation
	return matrix


def node_globals(gltf: dict[str, Any]) -> dict[int, np.ndarray]:
	nodes = gltf["nodes"]
	parent: dict[int, int] = {}
	for parent_index, node in enumerate(nodes):
		for child_index in node.get("children", []):
			parent[int(child_index)] = parent_index
	globals_by_node: dict[int, np.ndarray] = {}

	def visit(index: int) -> None:
		local = node_local(nodes[index])
		globals_by_node[index] = (
			globals_by_node[parent[index]] @ local if index in parent else local
		)
		for child in nodes[index].get("children", []):
			visit(int(child))

	for index in range(len(nodes)):
		if index not in parent:
			visit(index)
	return globals_by_node


def dense_weights(
	joints: np.ndarray, weights: np.ndarray, joint_count: int
) -> np.ndarray:
	dense = np.zeros((len(joints), joint_count), dtype=np.float64)
	rows = np.arange(len(joints))
	for influence in range(joints.shape[1]):
		np.add.at(dense, (rows, joints[:, influence].astype(np.int64)), weights[:, influence])
	dense /= np.maximum(dense.sum(axis=1, keepdims=True), 1.0e-12)
	return dense


def compact_weights(dense: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
	# Stable descending order makes rebuilds deterministic when weights tie.
	indices = np.argsort(-dense, axis=1, kind="stable")[:, :4]
	weights = np.take_along_axis(dense, indices, axis=1)
	weights /= np.maximum(weights.sum(axis=1, keepdims=True), 1.0e-12)
	return indices, weights


def main() -> None:
	args = parse_args()
	source_path = Path(args.source).resolve()
	out_path = Path(args.out).resolve()
	if source_path == out_path:
		raise ValueError("Refusing to overwrite --source; write and audit a candidate first")
	source_bytes = source_path.read_bytes()
	reference_bytes = load_reference(args)
	source_hash = sha256(source_bytes)
	if source_hash not in (EXPECTED_SOURCE_SHA256, EXPECTED_REPAIRED_SHA256):
		raise ValueError(
			"The shipping source no longer matches the audited v4g input. "
			"Re-audit it and update this repair deliberately instead of applying "
			"historical weights to a different rig."
		)
	if sha256(reference_bytes) != EXPECTED_REFERENCE_SHA256:
		raise ValueError(
			"The reference does not match the audited b0b469c v4e donor"
		)
	source = Glb(source_bytes, "shipping source")
	reference = Glb(reference_bytes, "pre-regression reference")

	if len(source.gltf.get("meshes", [])) != 1 or len(source.gltf.get("skins", [])) != 1:
		raise ValueError("Expected Roshan's one-mesh/one-skin GLB contract")
	source_primitive = source.gltf["meshes"][0]["primitives"][0]
	reference_primitive = reference.gltf["meshes"][0]["primitives"][0]
	for attribute in ("POSITION", "NORMAL", "TEXCOORD_0"):
		a = source.accessor(int(source_primitive["attributes"][attribute]))
		b = reference.accessor(int(reference_primitive["attributes"][attribute]))
		if a.shape != b.shape or not np.array_equal(a, b):
			raise ValueError(f"Donor mismatch: {attribute} is not byte-identical numerically")
	source_indices = source.accessor(int(source_primitive["indices"])).astype(
		np.int64
	)
	if not np.array_equal(
		source_indices,
		reference.accessor(int(reference_primitive["indices"])),
	):
		raise ValueError("Donor mismatch: triangle indices differ")

	source_skin = source.gltf["skins"][0]
	reference_skin = reference.gltf["skins"][0]
	source_joint_names = [
		source.gltf["nodes"][int(index)].get("name", "")
		for index in source_skin["joints"]
	]
	reference_joint_names = [
		reference.gltf["nodes"][int(index)].get("name", "")
		for index in reference_skin["joints"]
	]
	if source_joint_names != reference_joint_names:
		raise ValueError("Donor mismatch: skin joint order/names differ")
	joint_name_to_skin = {name: index for index, name in enumerate(source_joint_names)}
	joint_name_to_node = {
		node.get("name", ""): index
		for index, node in enumerate(source.gltf["nodes"])
		if node.get("name")
	}
	for name in (*LEFT_BONES, "chest", "handHold"):
		if name not in joint_name_to_skin or name not in joint_name_to_node:
			raise ValueError(f"Required joint is missing: {name}")

	position = source.accessor(int(source_primitive["attributes"]["POSITION"])).astype(
		np.float64
	)
	reference_joints = reference.accessor(
		int(reference_primitive["attributes"]["JOINTS_0"]), normalized=False
	).astype(np.int64)
	reference_weights = reference.accessor(
		int(reference_primitive["attributes"]["WEIGHTS_0"])
	).astype(np.float64)
	dense = dense_weights(reference_joints, reference_weights, len(source_joint_names))
	left_indices = np.array(
		[joint_name_to_skin[name] for name in LEFT_BONES], dtype=np.int64
	)
	chest_index = joint_name_to_skin["chest"]
	left_total = dense[:, left_indices].sum(axis=1)

	upper_axis = REPAIRED_GLOBAL_ELBOW - REPAIRED_GLOBAL_SHOULDER
	upper_length_sq = float(upper_axis @ upper_axis)
	t = ((position - REPAIRED_GLOBAL_SHOULDER) @ upper_axis) / max(
		upper_length_sq, 1.0e-12
	)
	closest = REPAIRED_GLOBAL_SHOULDER + np.clip(t, 0.0, 1.0)[:, None] * upper_axis
	radial = np.linalg.norm(position - closest, axis=1)
	# The shoulder blend must cover the complete geometric seam. A narrower 20%
	# blend left an 80%-arm vertex directly beside a 100%-chest vertex and opened
	# that 0.0053-unit edge to 0.0606 in a T-pose. This audited envelope selects
	# no hand vertices and leaves every point at/after 35% of the upper arm
	# untouched, while removing every >3x shoulder edge stretch.
	shoulder_selection = (left_total > 0.5) & (t < 0.35) & (radial < 0.105)
	s = np.clip(t / 0.35, 0.0, 1.0)
	smooth = s * s * (3.0 - 2.0 * s)
	blend = 0.75 * (1.0 - smooth) * shoulder_selection.astype(np.float64)
	dense[:, left_indices] *= 1.0 - blend[:, None]
	dense[:, chest_index] += blend
	dense /= np.maximum(dense.sum(axis=1, keepdims=True), 1.0e-12)
	new_joints, new_weights = compact_weights(dense)

	for bone_name, translation in REPAIRED_LOCAL_TRANSLATIONS.items():
		node = source.gltf["nodes"][joint_name_to_node[bone_name]]
		if "matrix" in node:
			raise ValueError(f"{bone_name} unexpectedly uses a matrix node")
		node["translation"] = [float(value) for value in translation]

	globals_by_node = node_globals(source.gltf)
	inverse_binds = np.stack(
		[
			np.linalg.inv(globals_by_node[int(node_index)])
			for node_index in source_skin["joints"]
		],
		axis=0,
	).astype(np.float32)
	source.write_accessor(
		int(source_primitive["attributes"]["JOINTS_0"]), new_joints
	)
	source.write_accessor(
		int(source_primitive["attributes"]["WEIGHTS_0"]), new_weights
	)
	# glTF MAT4 accessor storage is column-major.
	source.write_accessor(
		int(source_skin["inverseBindMatrices"]),
		inverse_binds.transpose((0, 2, 1)).reshape((-1, 16)),
	)

	before_images = source.image_payloads()
	if len(before_images) != 1 or sha256(before_images[0]) != EXPECTED_IMAGE_SHA256:
		raise ValueError("Shipping embedded v4g JPEG is missing or has an unexpected hash")
	out_bytes = source.to_bytes()
	if sha256(out_bytes) != EXPECTED_REPAIRED_SHA256:
		raise RuntimeError(
			"Repair output differs from the audited deterministic result"
		)
	verification = Glb(out_bytes, "repaired output")
	after_images = verification.image_payloads()
	if [sha256(payload) for payload in after_images] != [
		sha256(payload) for payload in before_images
	]:
		raise RuntimeError("Embedded texture bytes changed during the rig-only repair")

	out_path.parent.mkdir(parents=True, exist_ok=True)
	out_path.write_bytes(out_bytes)
	left_hand_index = joint_name_to_skin["hand"]
	hand_nonzero = int(np.count_nonzero(dense[:, left_hand_index] > 1.0e-8))
	hand_probe = int(np.count_nonzero(dense[:, left_hand_index] > 0.12))
	referenced = np.zeros(len(dense), dtype=bool)
	referenced[np.unique(source_indices)] = True
	shoulder_referenced = int(np.count_nonzero(shoulder_selection & referenced))
	hand_nonzero_referenced = int(
		np.count_nonzero((dense[:, left_hand_index] > 1.0e-8) & referenced)
	)
	hand_probe_referenced = int(
		np.count_nonzero((dense[:, left_hand_index] > 0.12) & referenced)
	)
	print(f"ROSHAN_REPAIR|SOURCE_SHA256|{source_hash}")
	print(f"ROSHAN_REPAIR|REFERENCE_SHA256|{sha256(reference_bytes)}")
	print(f"ROSHAN_REPAIR|OUTPUT_SHA256|{sha256(out_bytes)}")
	print(f"ROSHAN_REPAIR|TEXTURE_SHA256|{sha256(after_images[0])}")
	print(
		"ROSHAN_REPAIR|SHOULDER_BLEND_SOURCE_ENTRIES|"
		f"{int(shoulder_selection.sum())}"
	)
	print(f"ROSHAN_REPAIR|SHOULDER_BLEND_REFERENCED_VERTICES|{shoulder_referenced}")
	print(f"ROSHAN_REPAIR|LEFT_HAND_SOURCE_ENTRIES|{hand_nonzero}")
	print(f"ROSHAN_REPAIR|LEFT_HAND_REFERENCED_VERTICES|{hand_nonzero_referenced}")
	print(f"ROSHAN_REPAIR|LEFT_HAND_PROBE_SOURCE_ENTRIES|{hand_probe}")
	print(
		"ROSHAN_REPAIR|LEFT_HAND_PROBE_REFERENCED_VERTICES|"
		f"{hand_probe_referenced}"
	)
	print(f"ROSHAN_REPAIR|OUTPUT|{out_path}")


if __name__ == "__main__":
	main()
