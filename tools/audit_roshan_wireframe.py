#!/usr/bin/env python3
"""Non-destructive wireframe and deformation audit for Mermaid Roshan v4.

Run from the repository root with Blender 4.4+::

    blender --background --factory-startup \
      --python tools/audit_roshan_wireframe.py -- \
      --glb assets/characters/roshan_v4.glb \
      --out audit/roshan_wireframe

The source GLB is imported read-only.  This script deliberately contains no
save/export operation and writes only PNG, JSON, and TXT diagnostics beneath
``--out``.  It poses the imported rig in memory, using the same rest-aware
model-axis conversion used by ``scripts/player.gd`` for all game-authored
poses.  The T-pose is deliberately a true lateral alignment rather than a
guess at game angles, so it is useful as a neutral rigging stress test.

Outputs:

* ``renders/<pose>_<view>.png``: topology plus on-body and offset skeletons
* ``roshan_rig_contact_sheet.png``: all five poses in three views
* ``audit_report.json``: topology, weights, asymmetry, hand gaps, and strain
* ``audit_summary.txt``: concise human-readable findings

No output is an animation/export asset.  Nothing here should be shipped in
place of the irreplaceable character GLB.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector
from mathutils.kdtree import KDTree


ARM_PRIMARY = ("armU", "armF", "hand")
ARM_SECONDARY = ("armU2", "armF2", "hand2")
ARM_BONES = set(ARM_PRIMARY + ARM_SECONDARY)
MIDLINE_BONES = ("root", "spine1", "chest", "neck", "head")

# Godot model axes converted to Blender's axes after a glTF round trip:
# Godot (X right, Y up, Z back) -> Blender (X right, Y forward, Z up).
GD_RIGHT = Vector((1.0, 0.0, 0.0))
GD_BACK = Vector((0.0, -1.0, 0.0))

def parse_args() -> argparse.Namespace:
	argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--glb", default="assets/characters/roshan_v4.glb")
	parser.add_argument("--out", default="audit/roshan_wireframe")
	parser.add_argument(
		"--resolution",
		type=int,
		default=720,
		help="Height of each diagnostic render (default: 720)",
	)
	parser.add_argument(
		"--no-render",
		action="store_true",
		help="Collect numerical metrics only; useful for a quick rig check",
	)
	return parser.parse_args(argv)


def vec(value: Vector | Iterable[float], digits: int = 6) -> list[float]:
	v = Vector(value)
	return [round(float(component), digits) for component in v]


def finite(value: float, digits: int = 6) -> float | None:
	value = float(value)
	return round(value, digits) if math.isfinite(value) else None


class GltfRuntimeRig:
	"""Authoritative glTF joint math matching ``tools/audit_motions.py``.

	Blender converts glTF joint axes into edit-bone roll, so assigning a local
	``PoseBone.rotation_quaternion`` is not equivalent to Godot's imported
	Skeleton3D pose. Instead, compute joint-global deformation and linear blend
	skinning in the source glTF frame, then write those vertices directly into
	the imported mesh. Blender bones are retained only as rest-shape input for
	the source-matrix skeleton diagram.
	"""

	GLTF_TO_BLENDER = np.array(
		[
			[1.0, 0.0, 0.0, 0.0],
			[0.0, 0.0, -1.0, 0.0],
			[0.0, 1.0, 0.0, 0.0],
			[0.0, 0.0, 0.0, 1.0],
		],
		dtype=np.float64,
	)

	def __init__(self, glb_path: Path) -> None:
		data = glb_path.read_bytes()
		json_length, json_type = struct.unpack_from("<II", data, 12)
		if json_type != 0x4E4F534A:
			raise ValueError("First GLB chunk is not JSON")
		self.gltf = json.loads(data[20 : 20 + json_length])
		binary_header = 20 + json_length
		binary_length, binary_type = struct.unpack_from("<II", data, binary_header)
		if binary_type != 0x004E4942:
			raise ValueError("Second GLB chunk is not BIN")
		self.binary = data[binary_header + 8 : binary_header + 8 + binary_length]
		self.nodes = self.gltf["nodes"]
		self.parent: dict[int, int] = {}
		for parent_index, node in enumerate(self.nodes):
			for child_index in node.get("children", []):
				self.parent[int(child_index)] = parent_index
		self.order: list[int] = []

		def visit(node_index: int) -> None:
			self.order.append(node_index)
			for child_index in self.nodes[node_index].get("children", []):
				visit(int(child_index))

		for root_index in range(len(self.nodes)):
			if root_index not in self.parent:
				visit(root_index)
		self.name_to_node = {
			node.get("name", ""): index
			for index, node in enumerate(self.nodes)
			if node.get("name")
		}
		self.rest_translation = {
			index: np.asarray(node.get("translation", [0.0, 0.0, 0.0]), dtype=np.float64)
			for index, node in enumerate(self.nodes)
		}
		self.rest_rotation = {
			index: np.asarray(node.get("rotation", [0.0, 0.0, 0.0, 1.0]), dtype=np.float64)
			for index, node in enumerate(self.nodes)
		}
		self.rest_scale = {
			index: np.asarray(node.get("scale", [1.0, 1.0, 1.0]), dtype=np.float64)
			for index, node in enumerate(self.nodes)
		}
		for name in ARM_BONES | set(MIDLINE_BONES):
			index = self.name_to_node.get(name)
			if index is None:
				raise ValueError(f"Required glTF joint node is missing: {name}")
			if "matrix" in self.nodes[index]:
				raise ValueError(f"Joint {name} uses a matrix node; TRS is required")
		self.rest_globals = self.global_matrices({})
		self.skin = self.gltf["skins"][0]
		self.skin_joints = [int(index) for index in self.skin["joints"]]
		self.inverse_bind = self.accessor(int(self.skin["inverseBindMatrices"])).reshape(
			(-1, 4, 4)
		).transpose((0, 2, 1))
		# Blender combines a glTF mesh's skinned primitives into one deform mesh.
		# Preserve that same primitive order here so direct authoritative LBS also
		# covers repair underlays/material splits instead of auditing primitive 0
		# while leaving later surfaces frozen in the bind pose.
		position_parts: list[np.ndarray] = []
		joint_parts: list[np.ndarray] = []
		weight_parts: list[np.ndarray] = []
		index_parts: list[np.ndarray] = []
		vertex_offset = 0
		for primitive in self.gltf["meshes"][0]["primitives"]:
			attributes = primitive["attributes"]
			for required in ("POSITION", "JOINTS_0", "WEIGHTS_0"):
				if required not in attributes:
					raise ValueError(f"Skinned mesh primitive is missing {required}")
			positions = self.accessor(int(attributes["POSITION"])).astype(np.float64)
			position_parts.append(positions)
			joint_parts.append(
				self.accessor(int(attributes["JOINTS_0"])).astype(np.int64)
			)
			weight_parts.append(
				self.accessor(int(attributes["WEIGHTS_0"])).astype(np.float64)
			)
			indices = self.accessor(int(primitive["indices"])).astype(np.int64).reshape(-1)
			index_parts.append(indices + vertex_offset)
			vertex_offset += len(positions)
		self.positions = np.concatenate(position_parts, axis=0)
		self.vertex_joints = np.concatenate(joint_parts, axis=0)
		self.vertex_weights = np.concatenate(weight_parts, axis=0)
		self.source_weight_sum_error = float(
			np.max(np.abs(self.vertex_weights.sum(axis=1) - 1.0))
		)
		self.vertex_weights /= np.maximum(
			self.vertex_weights.sum(axis=1, keepdims=True), 1.0e-12
		)
		self.indices = np.concatenate(index_parts)
		self.referenced_mask = np.zeros(len(self.positions), dtype=bool)
		self.referenced_mask[self.indices] = True
		self.referenced_indices = np.flatnonzero(self.referenced_mask)
		self._configured_mesh: bpy.types.Object | None = None
		self._mesh_rest_mapping_residual: float | None = None

	def validation_metrics(self) -> dict[str, Any]:
		inverse_bind_residual = max(
			float(
				np.max(
					np.abs(
						self.rest_globals[node_index] @ self.inverse_bind[joint_index]
						- np.eye(4)
					)
				)
			)
			for joint_index, node_index in enumerate(self.skin_joints)
		)
		quaternion_norm_error = max(
			abs(float(np.linalg.norm(self.rest_rotation[node_index])) - 1.0)
			for node_index in self.skin_joints
		)
		return {
			"maximum_inverse_bind_identity_residual": finite(inverse_bind_residual, 10),
			"maximum_rest_quaternion_norm_error": finite(quaternion_norm_error, 10),
			"maximum_source_weight_sum_error": finite(self.source_weight_sum_error, 10),
			"joint_indices_in_range": bool(
				self.vertex_joints.min() >= 0
				and self.vertex_joints.max() < len(self.skin_joints)
			),
			"all_positions_weights_and_bind_matrices_finite": bool(
				np.isfinite(self.positions).all()
				and np.isfinite(self.vertex_weights).all()
				and np.isfinite(self.inverse_bind).all()
			),
		}

	def accessor(self, accessor_index: int) -> np.ndarray:
		accessor = self.gltf["accessors"][accessor_index]
		buffer_view = self.gltf["bufferViews"][accessor["bufferView"]]
		component_type = int(accessor["componentType"])
		dtype = {
			5120: np.int8,
			5121: np.uint8,
			5122: np.int16,
			5123: np.uint16,
			5125: np.uint32,
			5126: np.float32,
		}[component_type]
		components = {
			"SCALAR": 1,
			"VEC2": 2,
			"VEC3": 3,
			"VEC4": 4,
			"MAT4": 16,
		}[accessor["type"]]
		start = int(buffer_view.get("byteOffset", 0)) + int(accessor.get("byteOffset", 0))
		element_bytes = np.dtype(dtype).itemsize * components
		stride = int(buffer_view.get("byteStride", element_bytes))
		if stride == element_bytes:
			array = np.frombuffer(
				self.binary,
				dtype=dtype,
				count=int(accessor["count"]) * components,
				offset=start,
			).reshape((int(accessor["count"]), components))
		else:
			array = np.ndarray(
				shape=(int(accessor["count"]), components),
				dtype=dtype,
				buffer=self.binary,
				offset=start,
				strides=(stride, np.dtype(dtype).itemsize),
			).copy()
		if accessor.get("normalized", False) and not np.issubdtype(dtype, np.floating):
			array = array.astype(np.float64)
			if np.issubdtype(dtype, np.unsignedinteger):
				array /= float(np.iinfo(dtype).max)
			else:
				array = np.maximum(array / float(np.iinfo(dtype).max), -1.0)
		return array[:, 0] if components == 1 else array

	@staticmethod
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

	@staticmethod
	def axis_angle_quaternion(axis: np.ndarray, angle: float) -> np.ndarray:
		axis = np.asarray(axis, dtype=np.float64)
		axis /= max(float(np.linalg.norm(axis)), 1.0e-12)
		sine = math.sin(angle * 0.5)
		return np.array(
			[axis[0] * sine, axis[1] * sine, axis[2] * sine, math.cos(angle * 0.5)],
			dtype=np.float64,
		)

	@staticmethod
	def quaternion_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
		ax, ay, az, aw = a
		bx, by, bz, bw = b
		return np.array(
			[
				aw * bx + ax * bw + ay * bz - az * by,
				aw * by - ax * bz + ay * bw + az * bx,
				aw * bz + ax * by - ay * bx + az * bw,
				aw * bw - ax * bx - ay * by - az * bz,
			],
			dtype=np.float64,
		)

	@staticmethod
	def quaternion_between(a: np.ndarray, b: np.ndarray) -> np.ndarray:
		"""Shortest unit quaternion rotating vector ``a`` onto vector ``b``."""
		a = np.array(a, dtype=np.float64, copy=True)
		b = np.array(b, dtype=np.float64, copy=True)
		a /= max(float(np.linalg.norm(a)), 1.0e-12)
		b /= max(float(np.linalg.norm(b)), 1.0e-12)
		dot = float(np.clip(a @ b, -1.0, 1.0))
		if dot > 1.0 - 1.0e-12:
			return np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float64)
		if dot < -1.0 + 1.0e-9:
			basis = np.array([1.0, 0.0, 0.0], dtype=np.float64)
			if abs(float(a @ basis)) > 0.9:
				basis = np.array([0.0, 1.0, 0.0], dtype=np.float64)
			axis = np.cross(a, basis)
			axis /= max(float(np.linalg.norm(axis)), 1.0e-12)
			return np.array([axis[0], axis[1], axis[2], 0.0], dtype=np.float64)
		cross = np.cross(a, b)
		quaternion = np.array([cross[0], cross[1], cross[2], 1.0 + dot])
		return quaternion / np.linalg.norm(quaternion)

	def model_axis_delta(self, bone_name: str, axis_gltf: Vector, angle: float) -> np.ndarray:
		index = self.name_to_node[bone_name]
		global_rest = self.rest_globals[index][:3, :3]
		u, _, vh = np.linalg.svd(global_rest)
		global_rest_rotation = u @ vh
		local_axis = global_rest_rotation.T @ np.asarray(axis_gltf, dtype=np.float64)
		return self.axis_angle_quaternion(local_axis, angle)

	def lateral_alignment_delta(
		self,
		bone_name: str,
		child_name: str,
		target_gltf: np.ndarray,
		deltas: dict[str, np.ndarray],
	) -> np.ndarray:
		"""Solve a joint-local delta that points its child exactly at ``target``."""
		bone_index = self.name_to_node[bone_name]
		child_index = self.name_to_node[child_name]
		parent_global = (
			self.global_matrices(deltas)[self.parent[bone_index]][:3, :3]
			if bone_index in self.parent
			else np.eye(3, dtype=np.float64)
		)
		# Remove any inherited scale before transforming a direction.
		parent_rotation, _, parent_rotation_v = np.linalg.svd(parent_global)
		parent_rotation = parent_rotation @ parent_rotation_v
		base_rotation = parent_rotation @ self.quat_matrix(self.rest_rotation[bone_index])
		target_local = base_rotation.T @ np.asarray(target_gltf, dtype=np.float64)
		child_translation = self.rest_translation[child_index]
		return self.quaternion_between(child_translation, target_local)

	def global_matrices(self, deltas: dict[str, np.ndarray]) -> dict[int, np.ndarray]:
		globals_by_node: dict[int, np.ndarray] = {}
		for index in self.order:
			node = self.nodes[index]
			if "matrix" in node:
				local = np.asarray(node["matrix"], dtype=np.float64).reshape(4, 4).T
			else:
				rotation = self.rest_rotation[index]
				name = node.get("name", "")
				if name in deltas:
					rotation = self.quaternion_multiply(rotation, deltas[name])
				local = np.eye(4, dtype=np.float64)
				local[:3, :3] = self.quat_matrix(rotation) @ np.diag(self.rest_scale[index])
				local[:3, 3] = self.rest_translation[index]
			globals_by_node[index] = (
				globals_by_node[self.parent[index]] @ local
				if index in self.parent
				else local
			)
		return globals_by_node

	def apply_to_blender(
		self, armature: bpy.types.Object, deltas: dict[str, np.ndarray]
	) -> None:
		pose_globals = self.global_matrices(deltas)
		conversion = self.GLTF_TO_BLENDER
		conversion_inverse = conversion.T
		for node_index in self.order:
			name = self.nodes[node_index].get("name", "")
			pose_bone = armature.pose.bones.get(name)
			if pose_bone is None:
				continue
			deformation_gltf = pose_globals[node_index] @ np.linalg.inv(
				self.rest_globals[node_index]
			)
			deformation_blender = conversion @ deformation_gltf @ conversion_inverse
			pose_bone.matrix = Matrix(deformation_blender.tolist()) @ pose_bone.bone.matrix_local
		bpy.context.view_layer.update()

	def bone_point_blender(
		self,
		armature: bpy.types.Object,
		bone_name: str,
		tail: bool,
		deltas: dict[str, np.ndarray],
	) -> Vector:
		"""Transform an imported rest-bone point with its source-joint matrix."""
		node_index = self.name_to_node[bone_name]
		pose_globals = self.global_matrices(deltas)
		deformation_gltf = pose_globals[node_index] @ np.linalg.inv(
			self.rest_globals[node_index]
		)
		deformation_blender = (
			self.GLTF_TO_BLENDER @ deformation_gltf @ self.GLTF_TO_BLENDER.T
		)
		bone = armature.data.bones[bone_name]
		point = bone.tail_local if tail else bone.head_local
		homogeneous = np.array([point.x, point.y, point.z, 1.0], dtype=np.float64)
		return Vector((deformation_blender @ homogeneous)[:3])

	def joint_head_blender(self, bone_name: str, deltas: dict[str, np.ndarray]) -> Vector:
		point_gltf = self.global_matrices(deltas)[self.name_to_node[bone_name]][:3, 3]
		return Vector(self.GLTF_TO_BLENDER[:3, :3] @ point_gltf)

	def skin_positions(self, deltas: dict[str, np.ndarray]) -> np.ndarray:
		"""Return authoritative linear-blend-skinned positions in glTF space."""
		pose_globals = self.global_matrices(deltas)
		joint_matrices = np.stack(
			[
				pose_globals[node_index] @ self.inverse_bind[joint_index]
				for joint_index, node_index in enumerate(self.skin_joints)
			],
			axis=0,
		)
		homogeneous = np.ones((len(self.positions), 4), dtype=np.float64)
		homogeneous[:, :3] = self.positions
		deformed = np.zeros((len(self.positions), 3), dtype=np.float64)
		for influence in range(4):
			matrices = joint_matrices[self.vertex_joints[:, influence]]
			transformed = np.einsum("nij,nj->ni", matrices, homogeneous)[:, :3]
			deformed += self.vertex_weights[:, influence, None] * transformed
		return deformed

	def positions_blender(self, deltas: dict[str, np.ndarray]) -> np.ndarray:
		positions_gltf = self.skin_positions(deltas)
		return positions_gltf @ self.GLTF_TO_BLENDER[:3, :3].T

	def configure_direct_mesh(self, obj: bpy.types.Object) -> float:
		"""Map imported vertices to source accessors and disable Blender skinning.

		Blender's armature evaluator differs slightly from Godot/glTF LBS for this
		asset.  The audit therefore writes source-LBS positions directly to the
		imported mesh.  The rest-position residual proves that Blender retained the
		source referenced-vertex order before this path is enabled.
		"""
		if self._configured_mesh is not None:
			raise RuntimeError("Direct glTF deformation supports exactly one mesh")
		if len(obj.data.vertices) != len(self.referenced_indices):
			raise RuntimeError(
				"Imported/source vertex-count mismatch: "
				f"{len(obj.data.vertices)} != {len(self.referenced_indices)}"
			)
		source_world = self.positions_blender({})[self.referenced_indices]
		world_inverse = np.asarray(obj.matrix_world.inverted(), dtype=np.float64)
		homogeneous = np.ones((len(source_world), 4), dtype=np.float64)
		homogeneous[:, :3] = source_world
		source_local = (homogeneous @ world_inverse.T)[:, :3]
		imported_local = np.empty(len(obj.data.vertices) * 3, dtype=np.float64)
		obj.data.vertices.foreach_get("co", imported_local)
		imported_local = imported_local.reshape((-1, 3))
		residual = float(np.max(np.linalg.norm(imported_local - source_local, axis=1)))
		if residual > 1.0e-5:
			raise RuntimeError(
				"Blender changed source vertex order/coordinates; direct skin mapping "
				f"is unsafe (max rest residual {residual:.9g})"
			)
		for modifier in obj.modifiers:
			if modifier.type == "ARMATURE":
				modifier.show_viewport = False
				modifier.show_render = False
		self._configured_mesh = obj
		self._mesh_rest_mapping_residual = residual
		self.write_direct_mesh({})
		return residual

	def write_direct_mesh(self, deltas: dict[str, np.ndarray]) -> None:
		if self._configured_mesh is None:
			raise RuntimeError("Direct mesh has not been configured")
		obj = self._configured_mesh
		source_world = self.positions_blender(deltas)[self.referenced_indices]
		world_inverse = np.asarray(obj.matrix_world.inverted(), dtype=np.float64)
		homogeneous = np.ones((len(source_world), 4), dtype=np.float64)
		homogeneous[:, :3] = source_world
		local = (homogeneous @ world_inverse.T)[:, :3]
		obj.data.vertices.foreach_set("co", local.reshape(-1))
		obj.data.update()
		bpy.context.view_layer.update()

	def hand_probe(self, bone_name: str, deltas: dict[str, np.ndarray]) -> tuple[np.ndarray, int]:
		joint_index = self.skin_joints.index(self.name_to_node[bone_name])
		selection = self.referenced_mask & np.any(
			(self.vertex_joints == joint_index) & (self.vertex_weights > 0.12), axis=1
		)
		positions = self.skin_positions(deltas)[selection]
		return positions.mean(axis=0), int(np.count_nonzero(selection))

	def practical_weld_topology(self, tolerance: float = 1.0e-4) -> dict[str, Any]:
		"""Measure geometric seams after welding exporter/UV splits by position."""
		quantized = np.rint(self.positions / tolerance).astype(np.int64)
		_, inverse = np.unique(quantized, axis=0, return_inverse=True)
		triangles = inverse[self.indices.reshape((-1, 3))]
		edges = np.vstack(
			[
				triangles[:, (0, 1)],
				triangles[:, (1, 2)],
				triangles[:, (2, 0)],
			]
		)
		edges.sort(axis=1)
		edges = edges[edges[:, 0] != edges[:, 1]]
		unique_edges, counts = np.unique(edges, axis=0, return_counts=True)
		used_vertices = np.unique(triangles.reshape(-1))
		compact = {int(value): index for index, value in enumerate(used_vertices)}
		compact_edges = np.asarray(
			[[compact[int(a)], compact[int(b)]] for a, b in unique_edges],
			dtype=np.int64,
		)
		parent = np.arange(len(used_vertices), dtype=np.int64)

		def find(index: int) -> int:
			while parent[index] != index:
				parent[index] = parent[parent[index]]
				index = int(parent[index])
			return index

		for a, b in compact_edges:
			ra, rb = find(int(a)), find(int(b))
			if ra != rb:
				parent[rb] = ra
		component_sizes: dict[int, int] = {}
		for index in range(len(used_vertices)):
			root = find(index)
			component_sizes[root] = component_sizes.get(root, 0) + 1
		return {
			"position_weld_tolerance": tolerance,
			"source_position_entries": len(self.positions),
			"referenced_source_positions": int(np.count_nonzero(self.referenced_mask)),
			"welded_referenced_vertices": len(used_vertices),
			"welded_edges": len(unique_edges),
			"boundary_edges_one_face": int(np.count_nonzero(counts == 1)),
			"nonmanifold_edges_more_than_two_faces": int(np.count_nonzero(counts > 2)),
			"geometric_shells": len(component_sizes),
			"shell_vertex_counts_descending": sorted(component_sizes.values(), reverse=True),
		}

	def rest_head_residual(self, armature: bpy.types.Object) -> float:
		worst = 0.0
		for name, node_index in self.name_to_node.items():
			bone = armature.data.bones.get(name)
			if bone is None:
				continue
			point_gltf = self.rest_globals[node_index][:3, 3]
			point_blender = self.GLTF_TO_BLENDER[:3, :3] @ point_gltf
			worst = max(worst, float(np.linalg.norm(point_blender - np.asarray(bone.head_local))))
		return worst


_RUNTIME_RIG: GltfRuntimeRig | None = None
_POSE_DELTAS: dict[str, np.ndarray] = {}


def percentile(values: np.ndarray, q: float) -> float | None:
	return finite(np.percentile(values, q)) if values.size else None


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as source:
		for block in iter(lambda: source.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def blender_to_godot(value: Vector) -> Vector:
	"""Blender (X, Y, Z-up) to Godot model (X, Y-up, Z-back)."""
	return Vector((value.x, value.z, -value.y))


def angle_degrees(a: Vector, b: Vector) -> float:
	if a.length < 1.0e-9 or b.length < 1.0e-9:
		return 0.0
	return math.degrees(a.angle(b))


def reset_pose(armature: bpy.types.Object) -> None:
	global _POSE_DELTAS
	_POSE_DELTAS = {}
	armature.data.pose_position = "POSE"
	for pose_bone in armature.pose.bones:
		pose_bone.rotation_mode = "QUATERNION"
		pose_bone.location = Vector((0.0, 0.0, 0.0))
		pose_bone.rotation_quaternion = Quaternion()
		pose_bone.scale = Vector((1.0, 1.0, 1.0))
	bpy.context.view_layer.update()
	if _RUNTIME_RIG is not None:
		_RUNTIME_RIG.apply_to_blender(armature, _POSE_DELTAS)


def rotate_model_axis(
	armature: bpy.types.Object,
	bone_name: str,
	model_axis_blender: Vector,
	angle_radians: float,
) -> None:
	"""Apply ``player.gd::_model_axis_quat`` semantics to the imported rig.

	The authoritative path computes global glTF deformation matrices and maps
	them onto Blender's imported rest bones.  This avoids confusing glTF joint
	axes with Blender's edit-bone roll.  The axis conversion matches
	``player.gd`` and ``tools/audit_motions.py``::

	    local_axis = global_rest_rotation.inverse() * model_axis
	    posed_local_rotation = rest_rotation * Quaternion(local_axis, angle)
	"""
	pose_bone = armature.pose.bones.get(bone_name)
	if pose_bone is None:
		return
	if _RUNTIME_RIG is not None:
		axis_gltf = blender_to_godot(model_axis_blender)
		_POSE_DELTAS[bone_name] = _RUNTIME_RIG.model_axis_delta(
			bone_name, axis_gltf, float(angle_radians)
		)
		_RUNTIME_RIG.apply_to_blender(armature, _POSE_DELTAS)
		return
	rest_rotation = pose_bone.bone.matrix_local.to_quaternion()
	local_axis = (rest_rotation.inverted() @ model_axis_blender).normalized()
	pose_bone.rotation_mode = "QUATERNION"
	pose_bone.rotation_quaternion = Quaternion(local_axis, float(angle_radians))


def apply_t_pose(armature: bpy.types.Object, midline_x: float) -> None:
	del midline_x
	global _POSE_DELTAS
	reset_pose(armature)
	if _RUNTIME_RIG is None:
		raise RuntimeError("Source glTF rig is required for diagnostic T-pose")
	for bone_name, child_name, target in (
		("armU", "armF", np.array([1.0, 0.0, 0.0])),
		("armF", "hand", np.array([1.0, 0.0, 0.0])),
		("armU2", "armF2", np.array([-1.0, 0.0, 0.0])),
		("armF2", "hand2", np.array([-1.0, 0.0, 0.0])),
	):
		_POSE_DELTAS[bone_name] = _RUNTIME_RIG.lateral_alignment_delta(
			bone_name, child_name, target, _POSE_DELTAS
		)
	_RUNTIME_RIG.apply_to_blender(armature, _POSE_DELTAS)
	bpy.context.view_layer.update()


@dataclass(frozen=True)
class PoseSpec:
	name: str
	description: str
	game_source: str
	apply: Callable[[bpy.types.Object, float], None]


def build_pose_specs() -> list[PoseSpec]:
	def rest(armature: bpy.types.Object, _midline_x: float) -> None:
		reset_pose(armature)

	def t_pose(armature: bpy.types.Object, midline_x: float) -> None:
		apply_t_pose(armature, midline_x)

	def cheer(armature: bpy.types.Object, _midline_x: float) -> None:
		reset_pose(armature)
		# player.gd VERB_LIB.cheer, held peak (t=0.5..1.7).
		rotate_model_axis(armature, "armU", GD_RIGHT + GD_BACK * 3.0, 2.4)
		rotate_model_axis(armature, "armU2", GD_RIGHT - GD_BACK * 3.0, 2.4)
		rotate_model_axis(armature, "armF", GD_RIGHT - GD_BACK * 0.5, 0.8)
		rotate_model_axis(armature, "armF2", GD_RIGHT + GD_BACK * 0.5, 0.8)
		rotate_model_axis(armature, "head", GD_RIGHT, 0.08)
		rotate_model_axis(armature, "chest", GD_RIGHT, -0.08)
		bpy.context.view_layer.update()

	def clap_open(armature: bpy.types.Object, _midline_x: float) -> None:
		reset_pose(armature)
		# player.gd VERB_LIB.clap at t=0.65: the open/rebound key.
		rotate_model_axis(armature, "armU", GD_RIGHT - GD_BACK * 1.5, 0.8)
		rotate_model_axis(armature, "armU2", GD_RIGHT + GD_BACK * 1.5, 0.8)
		bpy.context.view_layer.update()

	def clap_contact(armature: bpy.types.Object, _midline_x: float) -> None:
		reset_pose(armature)
		# player.gd VERB_LIB.clap at t=0.50: the authored contact key.
		rotate_model_axis(armature, "armU", GD_RIGHT - GD_BACK * 1.5, 2.4)
		rotate_model_axis(armature, "armU2", GD_RIGHT + GD_BACK * 1.5, 2.4)
		rotate_model_axis(armature, "armF", GD_BACK, -0.5)
		rotate_model_axis(armature, "armF2", GD_BACK, 0.5)
		bpy.context.view_layer.update()

	return [
		PoseSpec("rest", "Imported bind/rest pose", "roshan_v4.glb bind pose", rest),
		PoseSpec(
			"t_pose",
			"True lateral T-pose: shoulder-to-wrist segments aligned to +/- model X",
			"diagnostic alignment (not a game verb)",
			t_pose,
		),
		PoseSpec(
			"cheer_peak",
			"Both arms overhead at the current cheer hold angles",
			"scripts/player.gd VERB_LIB.cheer",
			cheer,
		),
		PoseSpec(
			"clap_open",
			"Open/rebound frame of the current clap",
			"scripts/player.gd VERB_LIB.clap at t=0.65",
			clap_open,
		),
		PoseSpec(
			"clap_contact",
			"Authored hand-contact frame of the current clap",
			"scripts/player.gd VERB_LIB.clap at t=0.50",
			clap_contact,
		),
	]


def imported_deform_meshes(armature: bpy.types.Object) -> list[bpy.types.Object]:
	meshes = []
	for obj in bpy.context.scene.objects:
		if obj.type != "MESH":
			continue
		if any(
			modifier.type == "ARMATURE" and modifier.object == armature
			for modifier in obj.modifiers
		):
			meshes.append(obj)
	return meshes


def hide_import_helpers(armature: bpy.types.Object, deform_meshes: list[bpy.types.Object]) -> list[str]:
	"""Hide imported staging objects, especially the Icosphere custom shape."""
	deform_set = set(deform_meshes)
	custom_shapes = {
		pose_bone.custom_shape
		for pose_bone in armature.pose.bones
		if pose_bone.custom_shape is not None
	}
	hidden = []
	for obj in list(bpy.context.scene.objects):
		is_helper = obj in custom_shapes or obj.name.lower().startswith("icosphere")
		is_stage = obj.type in {"CAMERA", "LIGHT"} or (
			obj.type == "MESH" and obj not in deform_set
		)
		if is_helper or is_stage:
			obj.hide_render = True
			obj.hide_set(True)
			hidden.append(obj.name)
	armature.hide_render = True
	return sorted(set(hidden))


def world_vertices(obj: bpy.types.Object) -> np.ndarray:
	depsgraph = bpy.context.evaluated_depsgraph_get()
	evaluated = obj.evaluated_get(depsgraph)
	evaluated_mesh = evaluated.to_mesh()
	try:
		count = len(evaluated_mesh.vertices)
		coordinates = np.empty(count * 3, dtype=np.float64)
		evaluated_mesh.vertices.foreach_get("co", coordinates)
		coordinates = coordinates.reshape((-1, 3))
		matrix = np.asarray(evaluated.matrix_world, dtype=np.float64)
		homogeneous = np.ones((count, 4), dtype=np.float64)
		homogeneous[:, :3] = coordinates
		return (homogeneous @ matrix.T)[:, :3]
	finally:
		evaluated.to_mesh_clear()


def connected_components(vertex_count: int, edges: np.ndarray) -> int:
	parent = np.arange(vertex_count, dtype=np.int64)

	def find(index: int) -> int:
		while parent[index] != index:
			parent[index] = parent[parent[index]]
			index = int(parent[index])
		return index

	for a, b in edges:
		ra, rb = find(int(a)), find(int(b))
		if ra != rb:
			parent[rb] = ra
	return len({find(index) for index in range(vertex_count)})


def mesh_topology(obj: bpy.types.Object, rest_coordinates: np.ndarray) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
	mesh = obj.data
	mesh.calc_loop_triangles()
	edges = np.asarray([edge.vertices[:] for edge in mesh.edges], dtype=np.int64)
	triangles = np.asarray(
		[triangle.vertices[:] for triangle in mesh.loop_triangles], dtype=np.int64
	)
	face_use = np.zeros(len(mesh.edges), dtype=np.int64)
	for polygon in mesh.polygons:
		for edge_index in polygon.edge_keys:
			# ``edge_keys`` stores vertex pairs, so map them once through Mesh.edge_keys.
			pass
	edge_lookup = {tuple(sorted(edge.vertices[:])): edge.index for edge in mesh.edges}
	for polygon in mesh.polygons:
		for key in polygon.edge_keys:
			index = edge_lookup.get(tuple(sorted(key)))
			if index is not None:
				face_use[index] += 1
	used_vertices = np.zeros(len(mesh.vertices), dtype=bool)
	if edges.size:
		used_vertices[edges.reshape(-1)] = True
	tri_points = rest_coordinates[triangles]
	rest_areas = 0.5 * np.linalg.norm(
		np.cross(tri_points[:, 1] - tri_points[:, 0], tri_points[:, 2] - tri_points[:, 0]),
		axis=1,
	)
	rest_edge_lengths = np.linalg.norm(
		rest_coordinates[edges[:, 0]] - rest_coordinates[edges[:, 1]], axis=1
	)
	polygon_sizes = np.asarray([len(poly.vertices) for poly in mesh.polygons])
	bounds_min = rest_coordinates.min(axis=0)
	bounds_max = rest_coordinates.max(axis=0)
	report = {
		"vertices": len(mesh.vertices),
		"edges": len(mesh.edges),
		"polygons": len(mesh.polygons),
		"triangles_after_triangulation": len(mesh.loop_triangles),
		"tri_faces": int(np.count_nonzero(polygon_sizes == 3)),
		"quad_faces": int(np.count_nonzero(polygon_sizes == 4)),
		"ngons": int(np.count_nonzero(polygon_sizes > 4)),
		"boundary_edges": int(np.count_nonzero(face_use == 1)),
		"non_manifold_edges_total": int(np.count_nonzero(face_use != 2)),
		"edges_with_more_than_two_faces": int(np.count_nonzero(face_use > 2)),
		"loose_edges": int(np.count_nonzero(face_use == 0)),
		"loose_vertices": int(np.count_nonzero(~used_vertices)),
		"connected_components_including_loose_vertices": connected_components(
			len(mesh.vertices), edges
		),
		"degenerate_triangles_area_lt_1e-10": int(np.count_nonzero(rest_areas < 1.0e-10)),
		"zero_length_edges_lt_1e-8": int(np.count_nonzero(rest_edge_lengths < 1.0e-8)),
		"materials": len(mesh.materials),
		"uv_layers": len(mesh.uv_layers),
		"bounds_blender": {"min": vec(bounds_min), "max": vec(bounds_max)},
		"height": finite(bounds_max[2] - bounds_min[2]),
		"euler_characteristic_v_minus_e_plus_f": int(
			len(mesh.vertices) - len(mesh.edges) + len(mesh.polygons)
		),
	}
	arrays = {
		"edges": edges,
		"triangles": triangles,
		"rest_edge_lengths": rest_edge_lengths,
		"rest_triangle_areas": rest_areas,
	}
	return report, arrays


def cohesive_arm_surface_report(rig: GltfRuntimeRig) -> dict[str, Any]:
	"""Validate continuous shoulder-to-palm topology in repaired or native meshes."""
	purpose = "continuous shoulder-elbow-wrist anatomical underlay"
	matches = [
		primitive
		for mesh in rig.gltf.get("meshes", [])
		for primitive in mesh.get("primitives", [])
		if primitive.get("extras", {}).get("purpose") == purpose
	]
	if len(matches) != 1:
		# Newer Roshan sculpts carry each anatomical arm in the native character
		# surface instead of adding a closed tube underneath it. Validate that a
		# single connected weighted region spans upper arm, forearm, and hand and
		# blends into the torso at the shoulder on each side.
		joint_names = [rig.nodes[node].get("name", "") for node in rig.skin_joints]
		name_to_skin = {name: index for index, name in enumerate(joint_names)}
		chains = {
			"positive_x": ("armU", "armF", "hand"),
			"negative_x": ("armU2", "armF2", "hand2"),
		}
		torso_names = tuple(
			name for name in ("spine1", "chest") if name in name_to_skin
		)
		native_primitives = [
			primitive
			for mesh in rig.gltf.get("meshes", [])
			for primitive in mesh.get("primitives", [])
			if primitive.get("indices") is not None
			and all(
				name in primitive.get("attributes", {})
				for name in ("POSITION", "JOINTS_0", "WEIGHTS_0")
			)
		]
		component_reports = []
		for label, names in chains.items():
			best: dict[str, Any] | None = None
			for primitive_index, primitive in enumerate(native_primitives):
				attributes = primitive["attributes"]
				positions = rig.accessor(int(attributes["POSITION"])).astype(np.float64)
				joints = rig.accessor(int(attributes["JOINTS_0"])).astype(np.int64)
				weights = rig.accessor(int(attributes["WEIGHTS_0"])).astype(np.float64)
				weights /= np.maximum(weights.sum(axis=1, keepdims=True), 1.0e-12)
				triangles = rig.accessor(int(primitive["indices"])).astype(np.int64).reshape((-1, 3))
				bone_weights = {
					name: np.where(joints == name_to_skin[name], weights, 0.0).sum(axis=1)
					for name in names
				}
				chain_weights = sum(bone_weights.values(), np.zeros(len(positions)))
				torso_weights = sum(
					(
						np.where(joints == name_to_skin[name], weights, 0.0).sum(axis=1)
						for name in torso_names
					),
					np.zeros(len(positions)),
				)
				selected = chain_weights > 0.03
				parent = np.arange(len(positions), dtype=np.int64)

				def find(index: int) -> int:
					while parent[index] != index:
						parent[index] = parent[parent[index]]
						index = int(parent[index])
					return index

				edges = np.vstack(
					[
						triangles[:, (0, 1)],
						triangles[:, (1, 2)],
						triangles[:, (2, 0)],
					]
				)
				for a, b in edges[selected[edges[:, 0]] & selected[edges[:, 1]]]:
					ra, rb = find(int(a)), find(int(b))
					if ra != rb:
						parent[rb] = ra
				components: dict[int, list[int]] = {}
				for vertex in np.flatnonzero(selected):
					components.setdefault(find(int(vertex)), []).append(int(vertex))
				if not components:
					continue
				dominant = max(
					components.values(),
					key=lambda vertices: float(chain_weights[vertices].sum()),
				)
				selection = np.asarray(dominant, dtype=np.int64)
				bone_totals = {
					name: finite(float(values[selection].sum()))
					for name, values in bone_weights.items()
				}
				total_weight = max(float(chain_weights.sum()), 1.0e-12)
				candidate = {
					"label": label,
					"primitive_index": primitive_index,
					"vertices": len(dominant),
					"weighted_components": len(components),
					"dominant_component_fraction_of_chain_weight": finite(
						float(chain_weights[selection].sum()) / total_weight
					),
					"shoulder_torso_bridge_vertices": int(
						np.count_nonzero(torso_weights[selection] > 0.03)
					),
					"coverage": {
						"bone_weight_totals": bone_totals,
						"all_chain_bones_present": all(
							(bone_totals[name] or 0.0) > 0.1 for name in names
						),
					},
				}
				if best is None or (
					candidate["dominant_component_fraction_of_chain_weight"] or 0.0
				) > (best["dominant_component_fraction_of_chain_weight"] or 0.0):
					best = candidate
			if best is not None:
				component_reports.append(best)
		present = (
			len(component_reports) == len(chains)
			and all(
				component["coverage"]["all_chain_bones_present"]
				and (component["dominant_component_fraction_of_chain_weight"] or 0.0) > 0.80
				and component["shoulder_torso_bridge_vertices"] > 0
				for component in component_reports
			)
		)
		return {
			"present": present,
			"mode": "native_continuous_mesh",
			"matching_primitives": len(matches),
			"skinned_primitives": len(native_primitives),
			"expected_purpose": purpose,
			"component_reports": component_reports,
		}
	primitive = matches[0]
	attributes = primitive["attributes"]
	positions = rig.accessor(int(attributes["POSITION"])).astype(np.float64)
	joints = rig.accessor(int(attributes["JOINTS_0"])).astype(np.int64)
	weights = rig.accessor(int(attributes["WEIGHTS_0"])).astype(np.float64)
	weights /= np.maximum(weights.sum(axis=1, keepdims=True), 1.0e-12)
	triangles = rig.accessor(int(primitive["indices"])).astype(np.int64).reshape((-1, 3))
	if triangles.min() < 0 or triangles.max() >= len(positions):
		raise ValueError("Cohesive arm surface indices are out of range")
	edges = np.vstack(
		[
			triangles[:, (0, 1)],
			triangles[:, (1, 2)],
			triangles[:, (2, 0)],
		]
	)
	edges.sort(axis=1)
	unique_edges, edge_counts = np.unique(edges, axis=0, return_counts=True)
	parent = np.arange(len(positions), dtype=np.int64)

	def find(index: int) -> int:
		while parent[index] != index:
			parent[index] = parent[parent[index]]
			index = int(parent[index])
		return index

	for a, b in unique_edges:
		ra, rb = find(int(a)), find(int(b))
		if ra != rb:
			parent[rb] = ra
	used = np.unique(triangles.reshape(-1))
	components: dict[int, list[int]] = {}
	for vertex in used:
		components.setdefault(find(int(vertex)), []).append(int(vertex))
	joint_names = [rig.nodes[node].get("name", "") for node in rig.skin_joints]
	name_to_skin = {name: index for index, name in enumerate(joint_names)}
	chains = {
		"positive_x": ("armU", "armF", "hand"),
		"negative_x": ("armU2", "armF2", "hand2"),
	}
	component_reports = []
	for vertices in sorted(components.values(), key=len, reverse=True):
		selection = np.asarray(vertices, dtype=np.int64)
		coverage = {}
		for label, names in chains.items():
			total = 0.0
			bone_totals = {}
			for name in names:
				skin_index = name_to_skin[name]
				bone_total = float(np.where(joints[selection] == skin_index, weights[selection], 0.0).sum())
				bone_totals[name] = finite(bone_total)
				total += bone_total
			coverage[label] = {
				"total_weight": finite(total),
				"bone_weight_totals": bone_totals,
				"all_chain_bones_present": all((bone_totals[name] or 0.0) > 0.1 for name in names),
			}
		label = max(coverage, key=lambda key: coverage[key]["total_weight"] or 0.0)
		component_reports.append(
			{
				"label": label,
				"vertices": len(vertices),
				"coverage": coverage[label],
			}
		)
	points = positions[triangles]
	areas = 0.5 * np.linalg.norm(
		np.cross(points[:, 1] - points[:, 0], points[:, 2] - points[:, 0]), axis=1
	)
	return {
		"present": True,
		"mode": "dedicated_closed_underlay",
		"matching_primitives": 1,
		"purpose": purpose,
		"vertices": len(positions),
		"triangles": len(triangles),
		"connected_components": len(components),
		"component_reports": component_reports,
		"boundary_edges": int(np.count_nonzero(edge_counts == 1)),
		"edges_with_more_than_two_faces": int(np.count_nonzero(edge_counts > 2)),
		"degenerate_triangles_area_lt_1e-10": int(np.count_nonzero(areas < 1.0e-10)),
	}


def mesh_weights(
	obj: bpy.types.Object,
	armature: bpy.types.Object,
	coordinates: np.ndarray,
	height: float,
	midline_x: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
	bone_names = {bone.name for bone in armature.data.bones}
	group_names = {group.index: group.name for group in obj.vertex_groups}
	vertex_count = len(obj.data.vertices)
	sums = np.zeros(vertex_count, dtype=np.float64)
	influences = np.zeros(vertex_count, dtype=np.int64)
	primary = np.zeros(vertex_count, dtype=np.float64)
	secondary = np.zeros(vertex_count, dtype=np.float64)
	hand = np.zeros(vertex_count, dtype=np.float64)
	hand2 = np.zeros(vertex_count, dtype=np.float64)
	torso = np.zeros(vertex_count, dtype=np.float64)
	arm_group_weights = {
		name: np.zeros(vertex_count, dtype=np.float64) for name in ARM_BONES
	}
	unknown_weight = np.zeros(vertex_count, dtype=np.float64)
	per_group_vertices = {name: 0 for name in group_names.values()}
	per_group_weight = {name: 0.0 for name in group_names.values()}
	for vertex in obj.data.vertices:
		for assignment in vertex.groups:
			weight = float(assignment.weight)
			if weight <= 1.0e-8:
				continue
			name = group_names.get(assignment.group, f"<group:{assignment.group}>")
			sums[vertex.index] += weight
			influences[vertex.index] += 1
			per_group_vertices[name] = per_group_vertices.get(name, 0) + 1
			per_group_weight[name] = per_group_weight.get(name, 0.0) + weight
			if name in ARM_PRIMARY:
				primary[vertex.index] += weight
			if name in ARM_SECONDARY:
				secondary[vertex.index] += weight
			if name == "hand":
				hand[vertex.index] += weight
			if name == "hand2":
				hand2[vertex.index] += weight
			if name in {"root", "spine1", "chest"}:
				torso[vertex.index] += weight
			if name in arm_group_weights:
				arm_group_weights[name][vertex.index] += weight
			if name not in bone_names:
				unknown_weight[vertex.index] += weight
	weighted = sums > 1.0e-8
	normalized_error = np.abs(sums[weighted] - 1.0)

	def spatial_arm_audit(
		label: str,
		names: tuple[str, ...],
		weights: np.ndarray,
		expected_positive_x: bool,
	) -> dict[str, Any]:
		"""Measure arm influence that lies implausibly far from its bone chain."""
		distance = np.full(vertex_count, np.inf, dtype=np.float64)
		for bone_name in names:
			a = np.asarray(bone_point_world(armature, bone_name), dtype=np.float64)
			b = np.asarray(bone_point_world(armature, bone_name, True), dtype=np.float64)
			ab = b - a
			ab2 = max(float(ab @ ab), 1.0e-12)
			t = np.clip(((coordinates - a) @ ab) / ab2, 0.0, 1.0)
			distance = np.minimum(
				distance, np.linalg.norm(coordinates - a - t[:, None] * ab, axis=1)
			)
		selected = weights > 0.05
		strong = weights > 0.25
		far_threshold = height * 0.08
		far = selected & (distance > far_threshold)
		wrong_side = (
			coordinates[:, 0] < midline_x - height * 0.02
			if expected_positive_x
			else coordinates[:, 0] > midline_x + height * 0.02
		)
		weight_total = max(float(weights.sum()), 1.0e-12)
		selected_distance = distance[selected]
		strong_coordinates = coordinates[strong]
		return {
			"label": label,
			"bones": list(names),
			"expected_side": "+X" if expected_positive_x else "-X",
			"vertices_weight_gt_0_05": int(np.count_nonzero(selected)),
			"vertices_weight_gt_0_25": int(np.count_nonzero(strong)),
			"capsule_distance_threshold_8pct_height": finite(far_threshold),
			"far_vertices_weight_gt_0_05": int(np.count_nonzero(far)),
			"far_weight_fraction": finite(float(weights[far].sum()) / weight_total),
			"wrong_side_vertices_weight_gt_0_05": int(
				np.count_nonzero(selected & wrong_side)
			),
			"wrong_side_weight_fraction": finite(
				float(weights[wrong_side].sum()) / weight_total
			),
			"distance_from_chain_for_weighted_vertices": {
				"mean": finite(selected_distance.mean()) if selected_distance.size else None,
				"p90": percentile(selected_distance, 90),
				"p99": percentile(selected_distance, 99),
				"maximum": finite(selected_distance.max()) if selected_distance.size else None,
			},
			"strong_weight_vertex_bounds_blender": (
				{
					"min": vec(strong_coordinates.min(axis=0)),
					"max": vec(strong_coordinates.max(axis=0)),
				}
				if strong_coordinates.size
				else None
			),
		}

	spatial_audit = {
		"armU_armF_hand_positive_x": spatial_arm_audit(
			"positive-X full arm chain", ARM_PRIMARY, primary, True
		),
		"armU2_armF2_hand2_negative_x": spatial_arm_audit(
			"negative-X full arm chain", ARM_SECONDARY, secondary, False
		),
		"armU_positive_x_only": spatial_arm_audit(
			"positive-X upper arm only", ("armU",), arm_group_weights["armU"], True
		),
		"armU2_negative_x_only": spatial_arm_audit(
			"negative-X upper arm only", ("armU2",), arm_group_weights["armU2"], False
		),
	}

	def torso_contamination(label: str, arm_weights: np.ndarray) -> dict[str, Any]:
		selected = arm_weights > 1.0e-8
		values = torso[selected]
		return {
			"label": label,
			"arm_influenced_vertices": int(np.count_nonzero(selected)),
			"vertices_with_torso_weight_gt_0_05": int(np.count_nonzero(values > 0.05)),
			"vertices_with_torso_weight_gt_0_25": int(np.count_nonzero(values > 0.25)),
			"vertices_with_torso_weight_gt_0_40": int(np.count_nonzero(values > 0.40)),
			"median_torso_weight": finite(np.median(values)) if values.size else None,
			"maximum_torso_weight": finite(values.max()) if values.size else None,
		}

	torso_audit = {
		"torso_definition": ["root", "spine1", "chest"],
		"positive_x_full_arm": torso_contamination("armU + armF + hand", primary),
		"negative_x_full_arm": torso_contamination("armU2 + armF2 + hand2", secondary),
		"positive_x_forearm": torso_contamination("armF", arm_group_weights["armF"]),
		"negative_x_forearm": torso_contamination("armF2", arm_group_weights["armF2"]),
	}

	def weighted_region(weights: np.ndarray, threshold: float = 1.0e-8) -> dict[str, Any]:
		selection = weights > threshold
		points = coordinates[selection]
		return {
			"threshold": threshold,
			"vertices": int(np.count_nonzero(selection)),
			"weight_sum": finite(weights[selection].sum()) if points.size else 0.0,
			"bounds_blender": {
				"min": vec(points.min(axis=0)),
				"max": vec(points.max(axis=0)),
				"extent": vec(points.max(axis=0) - points.min(axis=0)),
			}
			if points.size
			else None,
		}

	report = {
		"vertex_groups": len(obj.vertex_groups),
		"groups_without_matching_bone": sorted(set(group_names.values()) - bone_names),
		"bones_without_vertex_group": sorted(bone_names - set(group_names.values())),
		"zero_weight_vertex_groups": sorted(
			name for name, count in per_group_vertices.items() if count == 0
		),
		"unweighted_vertices": int(np.count_nonzero(~weighted)),
		"underweighted_vertices_sum_lt_0_99": int(np.count_nonzero((sums < 0.99) & weighted)),
		"overweighted_vertices_sum_gt_1_01": int(np.count_nonzero(sums > 1.01)),
		"max_weight_sum_error": finite(normalized_error.max() if normalized_error.size else 0.0),
		"mean_weight_sum_error": finite(normalized_error.mean() if normalized_error.size else 0.0),
		"max_influences_per_vertex": int(influences.max()) if influences.size else 0,
		"vertices_over_four_influences": int(np.count_nonzero(influences > 4)),
		"influence_histogram": {
			str(count): int(np.count_nonzero(influences == count))
			for count in range(int(influences.max()) + 1)
		},
		"vertices_weighted_to_both_arm_chains_gt_0_05_each": int(
			np.count_nonzero((primary > 0.05) & (secondary > 0.05))
		),
		"vertices_with_unknown_group_weight": int(np.count_nonzero(unknown_weight > 1.0e-6)),
		"arm_chain_vertex_counts_weight_gt_0_25": {
			"armU_armF_hand": int(np.count_nonzero(primary > 0.25)),
			"armU2_armF2_hand2": int(np.count_nonzero(secondary > 0.25)),
			"hand": int(np.count_nonzero(hand > 0.25)),
			"hand2": int(np.count_nonzero(hand2 > 0.25)),
		},
		"spatial_arm_weight_audit": spatial_audit,
		"arm_to_torso_weight_contamination": torso_audit,
		"hand_weighted_regions": {
			"positive_x_anatomical_left_hand": weighted_region(hand),
			"negative_x_anatomical_right_hand": weighted_region(hand2),
			"interpretation": (
				"A nonzero region proves that hand geometry/binding exists; a large bilateral "
				"count or weight-sum mismatch indicates incomplete or asymmetric binding."
			),
		},
		"per_group": {
			name: {
				"vertices": int(per_group_vertices[name]),
				"weight_sum": finite(per_group_weight[name]),
			}
			for name in sorted(per_group_vertices)
		},
	}
	arrays = {
		"sum": sums,
		"influences": influences,
		"primary_arm": primary,
		"secondary_arm": secondary,
		"arm": primary + secondary,
		"hand": hand,
		"hand2": hand2,
		"torso": torso,
		**arm_group_weights,
	}
	return report, arrays


def bone_point_world(armature: bpy.types.Object, bone_name: str, tail: bool = False) -> Vector:
	if _RUNTIME_RIG is not None:
		point = _RUNTIME_RIG.bone_point_blender(
			armature, bone_name, tail, _POSE_DELTAS
		)
	else:
		pose_bone = armature.pose.bones[bone_name]
		point = pose_bone.tail if tail else pose_bone.head
	return armature.matrix_world @ point


def arm_chain_points(armature: bpy.types.Object, chain: tuple[str, str, str]) -> list[Vector]:
	if _RUNTIME_RIG is not None:
		return [
			armature.matrix_world @ _RUNTIME_RIG.joint_head_blender(name, _POSE_DELTAS)
			for name in chain
		]
	return [bone_point_world(armature, name) for name in chain]


def arm_asymmetry(armature: bpy.types.Object, midline_x: float, height: float) -> dict[str, Any]:
	primary_points = arm_chain_points(armature, ARM_PRIMARY)
	secondary_points = arm_chain_points(armature, ARM_SECONDARY)
	primary_lengths = [
		(primary_points[index + 1] - primary_points[index]).length
		for index in range(len(primary_points) - 1)
	]
	secondary_lengths = [
		(secondary_points[index + 1] - secondary_points[index]).length
		for index in range(len(secondary_points) - 1)
	]
	reflected = [Vector((2.0 * midline_x - p.x, p.y, p.z)) for p in primary_points]
	errors = [(a - b).length for a, b in zip(reflected, secondary_points)]
	primary_total = sum(primary_lengths)
	secondary_total = sum(secondary_lengths)
	mean_total = max((primary_total + secondary_total) * 0.5, 1.0e-9)
	shorter_total = max(min(primary_total, secondary_total), 1.0e-9)
	return {
		"naming_note": (
			"armU/armF/hand is the positive-X chain in this file; armU2/armF2/hand2 "
			"is the negative-X chain. Anatomical left/right labels are intentionally avoided."
		),
		"midline_x": finite(midline_x),
		"character_height": finite(height),
		"primary_chain_points_blender": [vec(point) for point in primary_points],
		"secondary_chain_points_blender": [vec(point) for point in secondary_points],
		"primary_segment_lengths": [finite(value) for value in primary_lengths],
		"secondary_segment_lengths": [finite(value) for value in secondary_lengths],
		"primary_total_length": finite(primary_total),
		"secondary_total_length": finite(secondary_total),
		"longer_chain_excess_fraction_of_shorter": finite(
			abs(primary_total - secondary_total) / shorter_total
		),
		"total_length_difference_fraction_of_mean": finite(
			abs(primary_total - secondary_total) / mean_total
		),
		"mirrored_joint_error_each": [finite(value) for value in errors],
		"mirrored_joint_rms": finite(math.sqrt(sum(e * e for e in errors) / len(errors))),
		"mirrored_joint_rms_fraction_of_height": finite(
			math.sqrt(sum(e * e for e in errors) / len(errors)) / max(height, 1.0e-9)
		),
		"shoulder_height_difference": finite(abs(primary_points[0].z - secondary_points[0].z)),
		"shoulder_depth_difference": finite(abs(primary_points[0].y - secondary_points[0].y)),
		"mirror_metric_interpretation": (
			"Raw reflected rest-joint position error, retained as a descriptor of the "
			"native shoulder pose/depth offset. It is not a measure of arm-segment "
			"proportion parity and does not gate that finding."
		),
		"chain_scope": "Shoulder, elbow, and wrist joint heads; terminal display-bone tails excluded.",
	}


def strain_stats(
	current: np.ndarray,
	rest: np.ndarray,
	topology: dict[str, np.ndarray],
	arm_weights: np.ndarray,
	height: float,
) -> dict[str, Any]:
	edges = topology["edges"]
	triangles = topology["triangles"]
	rest_edge_lengths = topology["rest_edge_lengths"]
	rest_triangle_areas = topology["rest_triangle_areas"]
	current_edge_lengths = np.linalg.norm(current[edges[:, 0]] - current[edges[:, 1]], axis=1)
	tri_points = current[triangles]
	current_triangle_areas = 0.5 * np.linalg.norm(
		np.cross(tri_points[:, 1] - tri_points[:, 0], tri_points[:, 2] - tri_points[:, 0]),
		axis=1,
	)
	edge_cutoff = max(height * 0.001, 1.0e-5)
	area_cutoff = edge_cutoff * edge_cutoff * 0.25
	valid_edges = rest_edge_lengths >= edge_cutoff
	valid_triangles = rest_triangle_areas >= area_cutoff
	arm_edges = valid_edges & (arm_weights[edges[:, 0]] + arm_weights[edges[:, 1]] >= 0.5)
	arm_triangles = valid_triangles & (
		arm_weights[triangles[:, 0]]
		+ arm_weights[triangles[:, 1]]
		+ arm_weights[triangles[:, 2]]
		>= 0.75
	)

	def ratio_report(current_values: np.ndarray, rest_values: np.ndarray, mask: np.ndarray) -> dict[str, Any]:
		ratio = current_values[mask] / np.maximum(rest_values[mask], 1.0e-12)
		absolute_strain = np.abs(ratio - 1.0)
		absolute_measure_change = np.abs(current_values[mask] - rest_values[mask])
		if not ratio.size:
			return {"samples": 0}
		local_worst = int(np.argmax(absolute_strain))
		indices = np.flatnonzero(mask)
		return {
			"samples": int(ratio.size),
			"minimum_ratio": finite(ratio.min()),
			"maximum_ratio": finite(ratio.max()),
			"mean_absolute_fractional_strain": finite(absolute_strain.mean()),
			"p95_absolute_fractional_strain": percentile(absolute_strain, 95),
			"p99_absolute_fractional_strain": percentile(absolute_strain, 99),
			"maximum_absolute_fractional_strain": finite(absolute_strain[local_worst]),
			"maximum_absolute_measure_change": finite(absolute_measure_change.max()),
			"elements_ratio_gt_3": int(np.count_nonzero(ratio > 3.0)),
			"elements_ratio_lt_0_2": int(np.count_nonzero(ratio < 0.2)),
			"worst_element_index": int(indices[local_worst]),
			"worst_rest_measure": finite(rest_values[indices[local_worst]]),
			"worst_pose_measure": finite(current_values[indices[local_worst]]),
		}

	displacement = np.linalg.norm(current - rest, axis=1)
	return {
		"macro_thresholds": {
			"rest_edge_length": finite(edge_cutoff),
			"rest_triangle_area": finite(area_cutoff),
		},
		"edge_length_all_macro": ratio_report(
			current_edge_lengths, rest_edge_lengths, valid_edges
		),
		"edge_length_arm_weighted": ratio_report(
			current_edge_lengths, rest_edge_lengths, arm_edges
		),
		"triangle_area_all_macro": ratio_report(
			current_triangle_areas, rest_triangle_areas, valid_triangles
		),
		"triangle_area_arm_weighted": ratio_report(
			current_triangle_areas, rest_triangle_areas, arm_triangles
		),
		"vertex_displacement": {
			"maximum": finite(displacement.max()),
			"p95": percentile(displacement, 95),
			"mean": finite(displacement.mean()),
		},
	}


def closest_surface_gap(
	pose_coordinates: dict[str, np.ndarray],
	weight_arrays: dict[str, dict[str, np.ndarray]],
	threshold: float = 0.25,
) -> dict[str, Any]:
	primary_points: list[tuple[str, int, Vector]] = []
	secondary_points: list[tuple[str, int, Vector]] = []
	for object_name, coordinates in pose_coordinates.items():
		weights = weight_arrays[object_name]
		for index in np.flatnonzero(weights["hand"] > threshold):
			primary_points.append((object_name, int(index), Vector(coordinates[index])))
		for index in np.flatnonzero(weights["hand2"] > threshold):
			secondary_points.append((object_name, int(index), Vector(coordinates[index])))
	if not primary_points or not secondary_points:
		return {
			"available": False,
			"reason": "No vertices exceeded the exact hand/hand2 weight threshold",
			"weight_threshold": threshold,
			"primary_vertices": len(primary_points),
			"secondary_vertices": len(secondary_points),
		}
	tree = KDTree(len(secondary_points))
	for tree_index, (_name, _vertex_index, point) in enumerate(secondary_points):
		tree.insert(point, tree_index)
	tree.balance()
	best = (float("inf"), None, None, None)
	for primary in primary_points:
		nearest, tree_index, distance = tree.find(primary[2])
		if distance < best[0]:
			best = (float(distance), primary, secondary_points[tree_index], nearest)
	primary = best[1]
	secondary = best[2]
	return {
		"available": True,
		"weight_threshold": threshold,
		"primary_vertices": len(primary_points),
		"secondary_vertices": len(secondary_points),
		"minimum_unsigned_vertex_gap": finite(best[0]),
		"note": (
			"Unsigned nearest weighted-vertex distance: zero/near-zero may mean contact "
			"or interpenetration; inspect the contact renders."
		),
		"primary_closest": {
			"object": primary[0],
			"vertex": primary[1],
			"position_blender": vec(primary[2]),
		},
		"secondary_closest": {
			"object": secondary[0],
			"vertex": secondary[1],
			"position_blender": vec(secondary[2]),
		},
	}


def pose_hand_metrics(
	armature: bpy.types.Object,
	midline_x: float,
	pose_coordinates: dict[str, np.ndarray],
	weight_arrays: dict[str, dict[str, np.ndarray]],
) -> dict[str, Any]:
	def hand_data(name: str) -> dict[str, Any]:
		wrist = bone_point_world(armature, name)
		tip = bone_point_world(armature, name, True)
		center = (wrist + tip) * 0.5
		return {
			"wrist_blender": vec(wrist),
			"tip_blender": vec(tip),
			"center_blender": vec(center),
			"wrist_godot_model": vec(blender_to_godot(wrist)),
			"tip_godot_model": vec(blender_to_godot(tip)),
		}
	primary = hand_data("hand")
	secondary = hand_data("hand2")

	def weighted_probe(bone_name: str, threshold: float = 0.12) -> tuple[Vector, int]:
		point_sets = []
		count = 0
		for object_name, coordinates in pose_coordinates.items():
			selection = weight_arrays[object_name][bone_name] > threshold
			if np.any(selection):
				point_sets.append(coordinates[selection])
				count += int(selection.sum())
		if not point_sets:
			return Vector(), 0
		return Vector(np.vstack(point_sets).mean(axis=0)), count

	primary_probe, primary_probe_count = weighted_probe("hand")
	secondary_probe, secondary_probe_count = weighted_probe("hand2")
	p_wrist, s_wrist = Vector(primary["wrist_blender"]), Vector(secondary["wrist_blender"])
	p_tip, s_tip = Vector(primary["tip_blender"]), Vector(secondary["tip_blender"])
	p_center = (p_wrist + p_tip) * 0.5
	s_center = (s_wrist + s_tip) * 0.5
	reflected_center = Vector((2.0 * midline_x - p_center.x, p_center.y, p_center.z))
	return {
		"primary_armU_armF_hand": primary,
		"secondary_armU2_armF2_hand2": secondary,
		"wrist_gap": finite((p_wrist - s_wrist).length),
		"tip_gap": finite((p_tip - s_tip).length),
		"bone_center_gap": finite((p_center - s_center).length),
		"center_axis_separations_blender": {
			"x_lateral": finite(abs(p_center.x - s_center.x)),
			"y_depth": finite(abs(p_center.y - s_center.y)),
			"z_height": finite(abs(p_center.z - s_center.z)),
		},
		"mirrored_center_error": finite((reflected_center - s_center).length),
		"weighted_probe_centroids": {
			"definition": (
				"Mean deformed position of vertices with >0.12 influence from the "
				"named hand bone; identical to tools/audit_motions.py probe_set."
			),
			"primary_count": primary_probe_count,
			"secondary_count": secondary_probe_count,
			"primary_blender": vec(primary_probe),
			"secondary_blender": vec(secondary_probe),
			"primary_godot_model": vec(blender_to_godot(primary_probe)),
			"secondary_godot_model": vec(blender_to_godot(secondary_probe)),
			"gap": finite((primary_probe - secondary_probe).length)
			if primary_probe_count and secondary_probe_count
			else None,
		},
		"weighted_mesh_hand_surface": closest_surface_gap(
			pose_coordinates, weight_arrays
		),
	}


def t_pose_quality(
	armature: bpy.types.Object, hand_metrics: dict[str, Any]
) -> dict[str, Any]:
	if _RUNTIME_RIG is None:
		raise RuntimeError("Source glTF rig is required for T-pose validation")
	angles = {}
	heights = []
	shoulders: dict[str, Vector] = {}
	for chain in (ARM_PRIMARY, ARM_SECONDARY):
		shoulder = armature.matrix_world @ _RUNTIME_RIG.joint_head_blender(
			chain[0], _POSE_DELTAS
		)
		shoulders[chain[0]] = shoulder
		target = GD_RIGHT if shoulder.x >= 0.0 else -GD_RIGHT
		for bone_name, child_name in zip(chain[:2], chain[1:]):
			head = armature.matrix_world @ _RUNTIME_RIG.joint_head_blender(
				bone_name, _POSE_DELTAS
			)
			child = armature.matrix_world @ _RUNTIME_RIG.joint_head_blender(
				child_name, _POSE_DELTAS
			)
			direction = child - head
			angles[bone_name] = finite(angle_degrees(direction, target))
			heights.extend([head.z, child.z])
	probes = hand_metrics["weighted_probe_centroids"]
	primary_probe = Vector(probes["primary_blender"])
	secondary_probe = Vector(probes["secondary_blender"])
	primary_target = GD_RIGHT if shoulders["armU"].x >= 0.0 else -GD_RIGHT
	secondary_target = GD_RIGHT if shoulders["armU2"].x >= 0.0 else -GD_RIGHT
	primary_reach = float((primary_probe - shoulders["armU"]).dot(primary_target))
	secondary_reach = float((secondary_probe - shoulders["armU2"]).dot(secondary_target))
	reach_difference = abs(primary_reach - secondary_reach)
	mean_reach = max((abs(primary_reach) + abs(secondary_reach)) * 0.5, 1.0e-9)
	return {
		"segment_deviation_from_outward_model_x_degrees": angles,
		"maximum_segment_deviation_degrees": finite(max(angles.values())),
		"full_arm_vertical_spread": finite(max(heights) - min(heights)),
		"weighted_hand_shoulder_local_outward_reach": {
			"definition": (
				"Outward model-X projection from each posed shoulder joint head to "
				"the matching >0.12 hand-bone weighted-vertex centroid. Subtracting "
				"each shoulder preserves native shoulder pose/depth while testing "
				"functional T-frame reach parity."
			),
			"primary_armU_hand": finite(primary_reach),
			"secondary_armU2_hand2": finite(secondary_reach),
			"absolute_difference": finite(reach_difference),
			"difference_fraction_of_bilateral_mean": finite(
				reach_difference / mean_reach
			),
		},
		"scope_note": "Upper-arm and forearm segments; rigid hands have no child/finger joint.",
	}


def make_wire_overlays(deform_meshes: list[bpy.types.Object]) -> list[bpy.types.Object]:
	wires = []
	for source in deform_meshes:
		wire = source.copy()
		wire.name = f"AUDIT_TOPOLOGY_{source.name}"
		wire.data = source.data
		bpy.context.collection.objects.link(wire)
		wire.color = (0.025, 0.035, 0.10, 1.0)
		wire.show_wire = True
		wire.show_all_edges = True
		modifier = wire.modifiers.new("AUDIT_EXACT_TOPOLOGY", "WIREFRAME")
		modifier.thickness = 0.00075
		modifier.offset = 1.0
		modifier.use_even_offset = True
		modifier.use_boundary = True
		wires.append(wire)
	return wires


def bone_category(name: str) -> str:
	if name in ARM_PRIMARY:
		return "arm_primary"
	if name in ARM_SECONDARY:
		return "arm_secondary"
	if name.startswith("hair"):
		return "hair"
	if name.startswith("tail") or name.startswith("fin"):
		return "tail"
	return "core"


OVERLAY_COLORS = {
	"core": (0.05, 0.90, 1.00, 1.0),
	"arm_primary": (1.00, 0.25, 0.08, 1.0),
	"arm_secondary": (1.00, 0.08, 0.70, 1.0),
	"hair": (0.60, 0.25, 1.00, 1.0),
	"tail": (0.15, 1.00, 0.42, 1.0),
}


class SkeletonOverlay:
	def __init__(self, armature: bpy.types.Object, prefix: str, thickness: float):
		self.armature = armature
		self.entries: list[tuple[bpy.types.Spline, str]] = []
		self.objects = []
		for category, color in OVERLAY_COLORS.items():
			curve = bpy.data.curves.new(f"{prefix}_{category}", "CURVE")
			curve.dimensions = "3D"
			curve.resolution_u = 1
			curve.bevel_depth = thickness * (1.55 if category.startswith("arm") else 1.0)
			curve.bevel_resolution = 1
			curve.resolution_u = 1
			curve.use_fill_caps = True
			obj = bpy.data.objects.new(f"{prefix}_{category}", curve)
			obj.color = color
			bpy.context.collection.objects.link(obj)
			self.objects.append(obj)
			for pose_bone in armature.pose.bones:
				if bone_category(pose_bone.name) != category:
					continue
				spline = curve.splines.new("POLY")
				spline.points.add(1)
				self.entries.append((spline, pose_bone.name))

	def update(self, offset: Vector) -> list[Vector]:
		points = []
		for spline, bone_name in self.entries:
			head = bone_point_world(self.armature, bone_name) + offset
			tail = bone_point_world(self.armature, bone_name, True) + offset
			spline.points[0].co = (*head, 1.0)
			spline.points[1].co = (*tail, 1.0)
			points.extend((head, tail))
		return points


def evaluated_bounds_points(deform_meshes: list[bpy.types.Object]) -> list[Vector]:
	points = []
	for obj in deform_meshes:
		coordinates = world_vertices(obj)
		minimum = coordinates.min(axis=0)
		maximum = coordinates.max(axis=0)
		for x in (minimum[0], maximum[0]):
			for y in (minimum[1], maximum[1]):
				for z in (minimum[2], maximum[2]):
					points.append(Vector((x, y, z)))
	return points


def setup_render_scene(resolution: int) -> bpy.types.Object:
	scene = bpy.context.scene
	scene.render.engine = "BLENDER_WORKBENCH"
	scene.display.shading.light = "STUDIO"
	scene.display.shading.studio_light = "paint.sl"
	scene.display.shading.color_type = "OBJECT"
	scene.display.shading.show_shadows = True
	scene.display.shading.show_cavity = True
	scene.display.shading.cavity_type = "BOTH"
	scene.display.shading.curvature_ridge_factor = 1.6
	scene.display.shading.curvature_valley_factor = 1.2
	scene.display.shading.background_type = "VIEWPORT"
	scene.display.shading.background_color = (0.93, 0.96, 1.0)
	scene.render.resolution_x = int(round(resolution * 1.28))
	scene.render.resolution_y = resolution
	scene.render.resolution_percentage = 100
	scene.render.image_settings.file_format = "PNG"
	scene.render.image_settings.color_mode = "RGBA"
	scene.render.film_transparent = False
	scene.render.use_file_extension = True
	scene.render.use_stamp = True
	scene.render.use_stamp_date = False
	scene.render.use_stamp_time = False
	scene.render.use_stamp_render_time = False
	scene.render.use_stamp_frame = False
	scene.render.use_stamp_filename = False
	scene.render.use_stamp_camera = False
	scene.render.use_stamp_scene = False
	scene.render.use_stamp_memory = False
	scene.render.use_stamp_hostname = False
	scene.render.use_stamp_note = True
	scene.render.stamp_font_size = max(13, resolution // 42)
	scene.render.stamp_foreground = (1.0, 1.0, 1.0, 1.0)
	scene.render.stamp_background = (0.025, 0.035, 0.10, 0.82)
	world = scene.world or bpy.data.worlds.new("AUDIT_WORLD")
	scene.world = world
	world.color = (0.93, 0.96, 1.0)
	camera_data = bpy.data.cameras.new("AUDIT_CAMERA")
	camera_data.type = "ORTHO"
	camera = bpy.data.objects.new("AUDIT_CAMERA", camera_data)
	bpy.context.collection.objects.link(camera)
	scene.camera = camera
	return camera


VIEW_DIRECTIONS = {
	"front": Vector((0.0, 1.0, 0.02)).normalized(),
	"three_quarter": Vector((0.72, 0.69, 0.08)).normalized(),
	"side": Vector((1.0, 0.0, 0.02)).normalized(),
}


def render_pose_view(
	pose_name: str,
	view_name: str,
	view_direction: Vector,
	deform_meshes: list[bpy.types.Object],
	on_body: SkeletonOverlay,
	diagram: SkeletonOverlay,
	camera: bpy.types.Object,
	output_path: Path,
	hand_gap: float,
) -> None:
	scene = bpy.context.scene
	up = Vector((0.0, 0.0, 1.0))
	right = up.cross(view_direction).normalized()
	screen_up = view_direction.cross(right).normalized()
	body_points = evaluated_bounds_points(deform_meshes)
	projected_width = max(p.dot(right) for p in body_points) - min(
		p.dot(right) for p in body_points
	)
	diagram_offset = right * max(projected_width * 1.12 + 0.12, 0.95)
	on_body_points = on_body.update(Vector((0.0, 0.0, 0.0)))
	diagram_points = diagram.update(diagram_offset)
	all_points = body_points + on_body_points + diagram_points
	right_values = [point.dot(right) for point in all_points]
	up_values = [point.dot(screen_up) for point in all_points]
	depth_values = [point.dot(view_direction) for point in all_points]
	center = (
		right * ((min(right_values) + max(right_values)) * 0.5)
		+ screen_up * ((min(up_values) + max(up_values)) * 0.5)
		+ view_direction * ((min(depth_values) + max(depth_values)) * 0.5)
	)
	width = max(right_values) - min(right_values)
	height = max(up_values) - min(up_values)
	aspect = scene.render.resolution_x / scene.render.resolution_y
	# Generous framing is intentional: pathological arm spikes are evidence and
	# must not make an underbound hand look absent merely because it was cropped.
	camera.data.ortho_scale = max(height * 1.30, width / aspect * 1.30, 1.0)
	camera.location = center + view_direction * 6.0
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	scene.render.filepath = str(output_path)
	scene.render.stamp_note_text = (
		f"{pose_name.replace('_', ' ').upper()} | {view_name.replace('_', ' ').upper()} | "
		f"LEFT: deformed topology + bones  RIGHT: full skeleton  weighted-hand gap {hand_gap:.3f}"
	)
	bpy.ops.render.render(write_still=True)


def make_contact_sheet(render_paths: list[Path], output_path: Path, columns: int = 3) -> None:
	"""Build a PNG contact sheet with Blender's image API (no Pillow dependency)."""
	if not render_paths:
		return
	images = [bpy.data.images.load(str(path), check_existing=False) for path in render_paths]
	try:
		rows = math.ceil(len(images) / columns)
		tile_width = 360
		first = images[0]
		tile_height = max(1, int(round(tile_width * first.size[1] / first.size[0])))
		gutter = 8
		sheet_width = columns * tile_width + (columns + 1) * gutter
		sheet_height = rows * tile_height + (rows + 1) * gutter
		sheet_pixels = np.ones((sheet_height, sheet_width, 4), dtype=np.float32)
		sheet_pixels[:, :, :3] = np.asarray((0.025, 0.035, 0.10), dtype=np.float32)
		for index, image in enumerate(images):
			source = np.empty(image.size[0] * image.size[1] * 4, dtype=np.float32)
			image.pixels.foreach_get(source)
			source = source.reshape((image.size[1], image.size[0], 4))
			y_indices = np.linspace(0, image.size[1] - 1, tile_height).astype(np.int64)
			x_indices = np.linspace(0, image.size[0] - 1, tile_width).astype(np.int64)
			thumbnail = source[y_indices][:, x_indices]
			row, column = divmod(index, columns)
			x0 = gutter + column * (tile_width + gutter)
			# Blender images are bottom-up, so row zero belongs at the sheet top.
			y0 = sheet_height - gutter - (row + 1) * tile_height - row * gutter
			sheet_pixels[y0 : y0 + tile_height, x0 : x0 + tile_width] = thumbnail
		sheet = bpy.data.images.new(
			"Roshan rig diagnostic contact sheet",
			width=sheet_width,
			height=sheet_height,
			alpha=True,
		)
		sheet.pixels.foreach_set(sheet_pixels.reshape(-1))
		sheet.filepath_raw = str(output_path)
		sheet.file_format = "PNG"
		sheet.save()
		bpy.data.images.remove(sheet)
	finally:
		for image in images:
			bpy.data.images.remove(image)


def aggregate_findings(report: dict[str, Any]) -> list[dict[str, str]]:
	findings: list[dict[str, str]] = []

	def add(code: str, severity: str, message: str) -> None:
		findings.append({"code": code, "severity": severity, "message": message})

	asymmetry = report["arm_chain_asymmetry_rest"]
	length_delta = asymmetry["total_length_difference_fraction_of_mean"] or 0.0
	longer_excess = asymmetry["longer_chain_excess_fraction_of_shorter"] or 0.0
	mirror_rms = asymmetry["mirrored_joint_rms_fraction_of_height"] or 0.0
	if length_delta > 0.10:
		add(
			"ARM_CHAIN_PROPORTION_PARITY",
			"review",
			f"Rest shoulder-to-wrist proportions differ materially: the longer side is "
			f"{longer_excess:.1%} longer ({length_delta:.1%} of bilateral mean; "
			"review threshold 10%).",
		)
	else:
		add(
			"ARM_CHAIN_PROPORTION_PARITY",
			"ok",
			f"Rest shoulder-to-wrist chain-length difference is {length_delta:.1%} "
			"of the bilateral mean (within the 10% proportion threshold).",
		)
	add(
		"NATIVE_SHOULDER_POSE_OFFSET",
		"info",
		f"Raw mirrored-joint RMS is {mirror_rms:.1%} of character height; native "
		f"shoulder height/depth offsets are {asymmetry['shoulder_height_difference']:.3f}/"
		f"{asymmetry['shoulder_depth_difference']:.3f}. These rest-pose coordinates "
		"remain reported for inspection but do not determine arm proportion parity.",
	)

	cohesive = report["cohesive_arm_surface"]
	component_reports = cohesive.get("component_reports", [])
	component_labels = {component.get("label") for component in component_reports}
	dedicated_ok = (
		cohesive.get("present", False)
		and cohesive.get("mode") == "dedicated_closed_underlay"
		and cohesive.get("matching_primitives") == 1
		and cohesive.get("connected_components") == 2
		and cohesive.get("boundary_edges") == 0
		and cohesive.get("edges_with_more_than_two_faces") == 0
		and cohesive.get("degenerate_triangles_area_lt_1e-10") == 0
		and component_labels == {"positive_x", "negative_x"}
		and all(
			component.get("coverage", {}).get("all_chain_bones_present", False)
			for component in component_reports
		)
	)
	native_ok = (
		cohesive.get("present", False)
		and cohesive.get("mode") == "native_continuous_mesh"
		and component_labels == {"positive_x", "negative_x"}
		and all(
			component.get("coverage", {}).get("all_chain_bones_present", False)
			and (
				component.get("dominant_component_fraction_of_chain_weight", 0.0) or 0.0
			) > 0.80
			and component.get("shoulder_torso_bridge_vertices", 0) > 0
			for component in component_reports
		)
	)
	if dedicated_ok:
		add(
			"COHESIVE_ARM_SURFACE",
			"ok",
			f"Dedicated anatomical underlay contains two closed manifold arm surfaces "
			f"({cohesive['vertices']} vertices, {cohesive['triangles']} triangles); each "
			"covers upper arm, forearm, and hand influences from shoulder into palm.",
		)
	elif native_ok:
		fractions = [
			component["dominant_component_fraction_of_chain_weight"]
			for component in component_reports
		]
		add(
			"COHESIVE_ARM_SURFACE",
			"ok",
			f"Both native arm surfaces have one dominant connected shoulder-to-palm "
			f"region ({fractions[0]:.1%}/{fractions[1]:.1%} of chain weight), with "
			f"upper-arm, forearm, hand, and torso-blended shoulder coverage.",
		)
	else:
		add(
			"COHESIVE_ARM_SURFACE",
			"problem",
			"No continuous native or repaired shoulder-to-palm surface covers both "
			f"complete arm chains: {cohesive}.",
		)

	open_gap = report["poses"]["clap_open"]["hands"]["weighted_probe_centroids"]["gap"]
	contact_gap = report["poses"]["clap_contact"]["hands"]["weighted_probe_centroids"]["gap"]
	open_surface_gap = report["poses"]["clap_open"]["hands"]["weighted_mesh_hand_surface"][
		"minimum_unsigned_vertex_gap"
	]
	contact_surface_gap = report["poses"]["clap_contact"]["hands"][
		"weighted_mesh_hand_surface"
	]["minimum_unsigned_vertex_gap"]
	height = report["character_height"]
	if contact_gap > height * 0.075 or contact_surface_gap > height * 0.01:
		add(
			"CLAP_CONTACT_GAP",
			"problem",
			f"The authored clap-contact key leaves weighted hand probes {contact_gap:.3f} apart "
			f"and the closest hand surfaces {contact_surface_gap:.3f} apart; this is not "
			"convincing contact.",
		)
	elif contact_gap >= open_gap * 0.90 or (
		open_surface_gap - contact_surface_gap
	) < height * 0.05:
		add(
			"CLAP_CONTACT_MOTION",
			"review",
			f"The contact key (centroids {contact_gap:.3f}, surfaces "
			f"{contact_surface_gap:.3f}) is not much closer than the open key "
			f"({open_gap:.3f}, {open_surface_gap:.3f}).",
		)
	else:
		add(
			"CLAP_CONTACT_GAP",
			"ok",
			f"The contact key reduces weighted-hand centroid gap from {open_gap:.3f} "
			f"to {contact_gap:.3f} and surface gap from {open_surface_gap:.3f} "
			f"to {contact_surface_gap:.3f}.",
		)

	cheer = report["poses"]["cheer_peak"]["overhead_quality"]
	primary_clearance = cheer["primary_weighted_hand_clearance_above_head"]
	secondary_clearance = cheer["secondary_weighted_hand_clearance_above_head"]
	if min(primary_clearance, secondary_clearance) < height * 0.02:
		add(
			"CHEER_OVERHEAD",
			"problem",
			f"The cheer does not place both weighted hand regions clearly above the "
			f"head joint (clearances {primary_clearance:.3f}, "
			f"{secondary_clearance:.3f}).",
		)
	else:
		add(
			"CHEER_OVERHEAD",
			"ok",
			f"Both weighted hand regions clear the posed head joint by "
			f"{primary_clearance:.3f} and {secondary_clearance:.3f}; bilateral "
			f"height mismatch is {cheer['weighted_hand_height_mismatch']:.3f}.",
		)

	worst_strain_pose = None
	worst_change_pose = None
	worst_strain = -1.0
	worst_absolute_change = -1.0
	for pose_name, pose in report["poses"].items():
		if pose_name == "rest":
			continue
		for mesh_strain in pose["strain_by_mesh"].values():
			edge_report = mesh_strain["edge_length_arm_weighted"]
			value = edge_report.get(
				"p99_absolute_fractional_strain", 0.0
			) or 0.0
			absolute_change = edge_report.get("maximum_absolute_measure_change", 0.0) or 0.0
			if value > worst_strain:
				worst_strain_pose = pose_name
				worst_strain = value
			if absolute_change > worst_absolute_change:
				worst_change_pose = pose_name
				worst_absolute_change = absolute_change
	if worst_absolute_change > report["character_height"] * 0.04:
		add(
			"ARM_EDGE_STRAIN",
			"problem",
			f"An arm-weighted connected edge changes length by {worst_absolute_change:.3f} "
			f"({worst_absolute_change / report['character_height']:.1%} of height) in {worst_change_pose}; "
			f"peak p99 relative edge strain is {worst_strain:.1%} in {worst_strain_pose}. "
			"inspect shoulder/elbow collapse in the wireframe.",
		)
	elif worst_strain > 0.18:
		add(
			"ARM_EDGE_STRAIN",
			"review",
			f"Arm-weighted p99 edge strain peaks at {worst_strain:.1%} in {worst_strain_pose}.",
		)
	else:
		add(
			"ARM_EDGE_STRAIN",
			"ok",
			f"Arm-weighted p99 macro-edge strain stays at or below {worst_strain:.1%}.",
		)

	for mesh_name, weights in report["weights"].items():
		contamination = weights["arm_to_torso_weight_contamination"]
		positive = contamination["positive_x_full_arm"]
		negative = contamination["negative_x_full_arm"]
		if (positive["median_torso_weight"] or 0.0) > 0.10 and (
			negative["median_torso_weight"] or 0.0
		) < 0.01:
			add(
				"ASYMMETRIC_ARM_TORSO_WEIGHTS",
				"problem",
				f"{mesh_name}'s +X arm has {positive['vertices_with_torso_weight_gt_0_05']}/"
				f"{positive['arm_influenced_vertices']} influenced vertices above 5% torso weight "
				f"(median {positive['median_torso_weight']:.1%}); the -X arm median is "
				f"{negative['median_torso_weight']:.1%}.",
			)
		hand_regions = weights["hand_weighted_regions"]
		left_hand = hand_regions["positive_x_anatomical_left_hand"]
		right_hand = hand_regions["negative_x_anatomical_right_hand"]
		if left_hand["vertices"] == 0:
			add(
				"LEFT_HAND_MISSING_BINDING",
				"problem",
				"No rendered vertex carries the anatomical-left hand bone.",
			)
		elif left_hand["vertices"] < right_hand["vertices"] * 0.5:
			left_extent = left_hand["bounds_blender"]["extent"]
			right_extent = right_hand["bounds_blender"]["extent"]
			add(
				"LEFT_HAND_UNDERBOUND",
				"problem",
				f"The anatomical left hand exists, but only {left_hand['vertices']} vertices "
				f"carry its hand bone versus {right_hand['vertices']} on the right "
				f"(weight sums {left_hand['weight_sum']:.1f} vs {right_hand['weight_sum']:.1f}); "
				f"its bind envelope is {left_extent[0]:.3f}x{left_extent[1]:.3f}x{left_extent[2]:.3f} "
				f"versus {right_extent[0]:.3f}x{right_extent[1]:.3f}x{right_extent[2]:.3f}.",
			)
		else:
			add(
				"LEFT_HAND_BINDING",
				"ok",
				f"The anatomical left hand has a complete binding region: "
				f"{left_hand['vertices']} vertices versus {right_hand['vertices']} on "
				"the anatomical right.",
			)

	unweighted = sum(mesh["unweighted_vertices"] for mesh in report["weights"].values())
	over_four = sum(mesh["vertices_over_four_influences"] for mesh in report["weights"].values())
	if unweighted or over_four:
		add(
			"WEIGHT_COVERAGE",
			"problem",
			f"Weight audit found {unweighted} unweighted vertices and {over_four} vertices over four influences.",
		)
	else:
		add(
			"WEIGHT_COVERAGE",
			"ok",
			"Every deform vertex has weights and no vertex exceeds four influences.",
		)

	practical = report["practical_weld_topology"]
	boundary = practical["boundary_edges_one_face"]
	more_than_two = practical["nonmanifold_edges_more_than_two_faces"]
	if boundary or more_than_two:
		add(
			"NON_MANIFOLD_TOPOLOGY",
			"review",
			f"At a {practical['position_weld_tolerance']:.0e}-unit practical weld, topology contains "
			f"{boundary} boundary edges and {more_than_two} edges shared by more than two faces. "
			"Some may be intentional garment/hair shells, but they deserve visual review.",
		)
	else:
		add("NON_MANIFOLD_TOPOLOGY", "ok", "The deform mesh is closed two-manifold by edge incidence.")

	t_quality = report["poses"]["t_pose"].get("t_pose_quality", {})
	t_deviation = t_quality.get("maximum_segment_deviation_degrees", 0.0) or 0.0
	if t_deviation > 2.0:
		add(
			"T_POSE_ALIGNMENT",
			"review",
			f"Diagnostic T-pose solver left {t_deviation:.2f} degrees maximum segment error.",
		)
	else:
		add(
			"T_POSE_ALIGNMENT",
			"ok",
			f"Diagnostic T-pose is genuinely lateral (maximum segment error {t_deviation:.2f} degrees).",
		)
	t_reach = t_quality["weighted_hand_shoulder_local_outward_reach"]
	t_reach_difference = t_reach["absolute_difference"] or 0.0
	t_reach_fraction = t_reach["difference_fraction_of_bilateral_mean"] or 0.0
	if t_reach_fraction > 0.05:
		add(
			"T_POSE_HAND_REACH_PARITY",
			"review",
			f"Shoulder-local weighted-hand reaches differ by {t_reach_difference:.4f} "
			f"({t_reach_fraction:.1%} of their bilateral mean; review threshold 5%).",
		)
	else:
		add(
			"T_POSE_HAND_REACH_PARITY",
			"ok",
			f"Shoulder-local weighted-hand reaches differ by {t_reach_difference:.4f} "
			f"({t_reach_fraction:.1%} of their bilateral mean; within the 5% threshold).",
		)
	return findings


def write_summary(path: Path, report: dict[str, Any]) -> None:
	lines = [
		"MERMAID ROSHAN V4 — NON-DESTRUCTIVE WIREFRAME / RIG AUDIT",
		"=" * 66,
		f"Source: {report['source_integrity']['path']}",
		f"SHA-256 unchanged: {report['source_integrity']['unchanged']}",
		f"Character height: {report['character_height']:.3f} Blender units",
		"",
		"Findings:",
	]
	for finding in report["findings"]:
		lines.append(
			f"- [{finding['severity'].upper()}] {finding['code']}: {finding['message']}"
		)
	lines.extend(
		[
			"",
			"Pose weighted-hand probe gaps (>0.12 hand-bone influence):",
		]
	)
	for pose_name, pose in report["poses"].items():
		lines.append(
			f"- {pose_name}: {pose['hands']['weighted_probe_centroids']['gap']:.4f}"
		)
	lines.extend(
		[
			"",
			"Interpret the numeric report together with the PNGs. Nearest-vertex hand",
			"distance is unsigned, and open garment/hair shells may intentionally produce",
			"boundary edges. This audit never writes back to or exports the source GLB.",
		]
	)
	path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
	global _RUNTIME_RIG
	args = parse_args()
	glb = Path(args.glb).resolve()
	out = Path(args.out).resolve()
	if not glb.is_file():
		raise FileNotFoundError(f"GLB not found: {glb}")
	if out == glb:
		raise ValueError("--out must be a directory and may not be the source GLB")
	out.mkdir(parents=True, exist_ok=True)
	render_dir = out / "renders"
	if not args.no_render:
		render_dir.mkdir(parents=True, exist_ok=True)

	before_stat = glb.stat()
	before_hash = sha256(glb)
	bpy.ops.wm.read_factory_settings(use_empty=True)
	bpy.ops.import_scene.gltf(filepath=str(glb))
	_RUNTIME_RIG = GltfRuntimeRig(glb)
	armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
	if len(armatures) != 1:
		raise RuntimeError(f"Expected one armature, found {len(armatures)}")
	armature = armatures[0]
	deform_meshes = imported_deform_meshes(armature)
	if not deform_meshes:
		raise RuntimeError("No mesh has an Armature modifier targeting the imported rig")
	# glTF and Godot use linear blend skinning.  Blender's optional dual-
	# quaternion "Preserve Volume" mode gives different hand positions and is
	# therefore explicitly disabled for this runtime-equivalence audit.
	for obj in deform_meshes:
		for modifier in obj.modifiers:
			if modifier.type == "ARMATURE" and modifier.object == armature:
				modifier.use_deform_preserve_volume = False
	required = ARM_BONES | set(MIDLINE_BONES)
	missing = sorted(required - {bone.name for bone in armature.data.bones})
	if missing:
		raise RuntimeError(f"Missing required Roshan bones: {missing}")

	hidden_helpers = hide_import_helpers(armature, deform_meshes)
	reset_pose(armature)
	if len(deform_meshes) != 1:
		raise RuntimeError(
			f"Expected one imported deform mesh for direct GLB skinning, found {len(deform_meshes)}"
		)
	direct_mapping_residual = _RUNTIME_RIG.configure_direct_mesh(deform_meshes[0])
	midline_x = float(
		sum(bone_point_world(armature, name).x for name in MIDLINE_BONES)
		/ len(MIDLINE_BONES)
	)
	rest_coordinates = {obj.name: world_vertices(obj) for obj in deform_meshes}
	global_min = np.min(
		np.vstack([coordinates.min(axis=0) for coordinates in rest_coordinates.values()]),
		axis=0,
	)
	global_max = np.max(
		np.vstack([coordinates.max(axis=0) for coordinates in rest_coordinates.values()]),
		axis=0,
	)
	height = float(global_max[2] - global_min[2])

	topology_report: dict[str, Any] = {}
	topology_arrays: dict[str, dict[str, np.ndarray]] = {}
	weight_report: dict[str, Any] = {}
	weight_arrays: dict[str, dict[str, np.ndarray]] = {}
	for obj in deform_meshes:
		topology_report[obj.name], topology_arrays[obj.name] = mesh_topology(
			obj, rest_coordinates[obj.name]
		)
		weight_report[obj.name], weight_arrays[obj.name] = mesh_weights(
			obj,
			armature,
			rest_coordinates[obj.name],
			height,
			midline_x,
		)

	report: dict[str, Any] = {
		"schema": "roshan-wireframe-audit-v1",
		"blender_version": bpy.app.version_string,
		"source_glb_structure": {
			"meshes": len(_RUNTIME_RIG.gltf.get("meshes", [])),
			"mesh_primitives": sum(
				len(mesh.get("primitives", []))
				for mesh in _RUNTIME_RIG.gltf.get("meshes", [])
			),
			"skins": len(_RUNTIME_RIG.gltf.get("skins", [])),
			"skin_joints": len(_RUNTIME_RIG.skin_joints),
			"animations": len(_RUNTIME_RIG.gltf.get("animations", [])),
			"morph_targets": sum(
				len(primitive.get("targets", []))
				for mesh in _RUNTIME_RIG.gltf.get("meshes", [])
				for primitive in mesh.get("primitives", [])
			),
			"position_entries": len(_RUNTIME_RIG.positions),
			"referenced_position_entries": len(_RUNTIME_RIG.referenced_indices),
			"triangles": len(_RUNTIME_RIG.indices) // 3,
			"maximum_vertex_influences": 4,
		},
		"source_glb_validation": _RUNTIME_RIG.validation_metrics(),
		"coordinate_system": {
			"metrics": "Blender model/world coordinates (X right, Y forward, Z up)",
			"godot_conversion": "(Blender X, Y, Z) -> (Godot X, Y, Z) = (X, Z, -Y)",
		},
		"source_integrity": {
			"path": str(glb),
			"bytes_before": before_stat.st_size,
			"mtime_ns_before": before_stat.st_mtime_ns,
			"sha256_before": before_hash,
			"policy": "Imported read-only; no bpy save/export operation is used",
		},
		"armature": {
			"name": armature.name,
			"bones": len(armature.data.bones),
			"deform_bones": sum(1 for bone in armature.data.bones if bone.use_deform),
			"bone_names": [bone.name for bone in armature.data.bones],
			"hidden_import_helpers": hidden_helpers,
			"icosphere_custom_shape_hidden": any(
				name.lower().startswith("icosphere") for name in hidden_helpers
			),
			"gltf_to_blender_rest_head_max_residual": finite(
				_RUNTIME_RIG.rest_head_residual(armature)
			),
		},
		"character_bounds_blender": {"min": vec(global_min), "max": vec(global_max)},
		"character_height": finite(height),
		"topology": topology_report,
		"practical_weld_topology": _RUNTIME_RIG.practical_weld_topology(),
		"cohesive_arm_surface": cohesive_arm_surface_report(_RUNTIME_RIG),
		"weights": weight_report,
		"arm_chain_asymmetry_rest": arm_asymmetry(armature, midline_x, height),
		"pose_method": {
			"game_authored": (
				"Authoritative glTF linear-blend-skinned vertices equivalent to "
				"tools/audit_motions.py and player.gd::_model_axis_quat are written "
				"directly into Blender's imported mesh; the armature is retained for diagrams. "
				"Cheer/clap values are copied from VERB_LIB."
			),
			"t_pose": (
				"Rest-aware quaternion alignment of upper arms and forearms to outward model X; "
				"not a game-authored angle."
			),
			"direct_mesh_mapping_max_rest_residual": finite(direct_mapping_residual),
		},
		"poses": {},
	}

	render_paths: list[Path] = []
	if not args.no_render:
		for obj in deform_meshes:
			obj.color = (0.72, 0.62, 0.88, 1.0)
		make_wire_overlays(deform_meshes)
		on_body_overlay = SkeletonOverlay(armature, "AUDIT_ON_BODY", 0.0045)
		diagram_overlay = SkeletonOverlay(armature, "AUDIT_DIAGRAM", 0.0090)
		camera = setup_render_scene(max(240, int(args.resolution)))
	else:
		on_body_overlay = None
		diagram_overlay = None
		camera = None

	for pose in build_pose_specs():
		pose.apply(armature, midline_x)
		_RUNTIME_RIG.write_direct_mesh(_POSE_DELTAS)
		pose_coordinates = {obj.name: world_vertices(obj) for obj in deform_meshes}
		pose_report: dict[str, Any] = {
			"description": pose.description,
			"source": pose.game_source,
			"hands": pose_hand_metrics(
				armature, midline_x, pose_coordinates, weight_arrays
			),
			"strain_by_mesh": {},
		}
		primary_gltf, primary_count = _RUNTIME_RIG.hand_probe("hand", _POSE_DELTAS)
		secondary_gltf, secondary_count = _RUNTIME_RIG.hand_probe("hand2", _POSE_DELTAS)
		runtime_gap = float(np.linalg.norm(primary_gltf - secondary_gltf))
		rendered_gap = float(pose_report["hands"]["weighted_probe_centroids"]["gap"])
		gap_residual = abs(runtime_gap - rendered_gap)
		if gap_residual > 5.0e-6:
			raise RuntimeError(
				f"Direct-render hand probe diverged from source GLB in {pose.name}: "
				f"{rendered_gap:.9f} vs {runtime_gap:.9f}"
			)
		pose_report["source_gltf_lbs_reconciliation"] = {
			"primary_count": primary_count,
			"secondary_count": secondary_count,
			"source_gap": finite(runtime_gap, 9),
			"rendered_mesh_gap": finite(rendered_gap, 9),
			"absolute_gap_residual": finite(gap_residual, 9),
		}
		if pose.name == "cheer_peak":
			head_world = _RUNTIME_RIG.joint_head_blender("head", _POSE_DELTAS)
			primary_height = float(
				pose_report["hands"]["weighted_probe_centroids"]["primary_blender"][2]
			)
			secondary_height = float(
				pose_report["hands"]["weighted_probe_centroids"]["secondary_blender"][2]
			)
			primary_depth = float(
				pose_report["hands"]["weighted_probe_centroids"]["primary_blender"][1]
			)
			secondary_depth = float(
				pose_report["hands"]["weighted_probe_centroids"]["secondary_blender"][1]
			)
			pose_report["overhead_quality"] = {
				"posed_head_joint_height_blender": finite(head_world.z),
				"primary_weighted_hand_height_blender": finite(primary_height),
				"secondary_weighted_hand_height_blender": finite(secondary_height),
				"primary_weighted_hand_clearance_above_head": finite(
					primary_height - head_world.z
				),
				"secondary_weighted_hand_clearance_above_head": finite(
					secondary_height - head_world.z
				),
				"weighted_hand_height_mismatch": finite(
					abs(primary_height - secondary_height)
				),
				"weighted_hand_depth_mismatch": finite(
					abs(primary_depth - secondary_depth)
				),
			}
		for obj in deform_meshes:
			pose_report["strain_by_mesh"][obj.name] = strain_stats(
				pose_coordinates[obj.name],
				rest_coordinates[obj.name],
				topology_arrays[obj.name],
				weight_arrays[obj.name]["arm"],
				height,
			)
		if pose.name == "t_pose":
			pose_report["t_pose_quality"] = t_pose_quality(
				armature, pose_report["hands"]
			)
		report["poses"][pose.name] = pose_report

		if not args.no_render:
			hand_gap = float(pose_report["hands"]["weighted_probe_centroids"]["gap"])
			for view_name, direction in VIEW_DIRECTIONS.items():
				path = render_dir / f"{pose.name}_{view_name}.png"
				render_pose_view(
					pose.name,
					view_name,
					direction,
					deform_meshes,
					on_body_overlay,
					diagram_overlay,
					camera,
					path,
					hand_gap,
				)
				render_paths.append(path)

	if render_paths:
		make_contact_sheet(render_paths, out / "roshan_rig_contact_sheet.png", columns=3)

	after_stat = glb.stat()
	after_hash = sha256(glb)
	report["source_integrity"].update(
		{
			"bytes_after": after_stat.st_size,
			"mtime_ns_after": after_stat.st_mtime_ns,
			"sha256_after": after_hash,
			"unchanged": (
				before_stat.st_size == after_stat.st_size
				and before_stat.st_mtime_ns == after_stat.st_mtime_ns
				and before_hash == after_hash
			),
		}
	)
	report["renders"] = [str(path) for path in render_paths]
	report["contact_sheet"] = (
		str(out / "roshan_rig_contact_sheet.png") if render_paths else None
	)
	report["findings"] = aggregate_findings(report)
	with (out / "audit_report.json").open("w", encoding="utf-8") as target:
		json.dump(report, target, indent=2, sort_keys=False)
		target.write("\n")
	write_summary(out / "audit_summary.txt", report)

	for finding in report["findings"]:
		print(
			f"ROSHAN_AUDIT|{finding['severity'].upper()}|{finding['code']}|{finding['message']}"
		)
	print(f"ROSHAN_AUDIT|SOURCE_UNCHANGED|{report['source_integrity']['unchanged']}")
	print(f"ROSHAN_AUDIT|REPORT|{out / 'audit_report.json'}")
	if render_paths:
		print(f"ROSHAN_AUDIT|CONTACT_SHEET|{out / 'roshan_rig_contact_sheet.png'}")


if __name__ == "__main__":
	main()
