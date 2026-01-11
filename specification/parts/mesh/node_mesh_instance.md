# G4MF Node Mesh Instance

## Overview

G4MF stores the visible geometry of objects inside of meshes. These meshes may be instanced on 0 or more nodes in the scene hierarchy using the `"meshInstance"` property on nodes to provide visible geometry for those nodes.

See [G4MF Mesh](mesh.md) for the details of the data within each mesh.

## Example

The following example defines.

## Properties

| Property         | Type        | Description                                                     | Default                |
| ---------------- | ----------- | --------------------------------------------------------------- | ---------------------- |
| **blendAmounts** | `number[]`  | How much each blend shape is activated and influences the mesh. | Equal to mesh.         |
| **materials**    | `integer[]` | The indices of the material overrides for this mesh instance.   | No material overrides. |
| **mesh**         | `integer`   | The index of the mesh that this node references.                | Required, no default.  |

### Blend Amounts

The `"blendAmounts"` property is an array of numbers that specifies how much each blend shape is activated. If not defined, all amounts are equal to those defined in the mesh's blend shape data.

Blend amounts are also known as weights or activations. Each value typically ranges from `0.0` to `1.0`, where `0.0` means no influence and `1.0` means full influence, but values can exceed this range for exaggerated effects, or use negative values for inverted effects. The size of this array must match the number of items in the mesh's blend `shapes` array. If `blendAmounts` is not explicitly defined, `blendAmounts` is defined to be the same as the mesh's blend shape `amounts` array.

### Materials

The `"materials"` property is an array of integer indices that reference materials in the document-level `"materials"` array. If not defined, use the materials defined in the mesh's surfaces.

These are references to a material in the G4MF file's document-level `"materials"` array. If this array has just a single index, that material overrides all surfaces in the mesh. If this array has multiple indices, each index overrides the corresponding surface in the mesh by order. The array length MUST either be 1 or match the number of surfaces in the mesh. This array MUST NOT be empty, it should not be defined at all if there are no overrides.

For each index in the array, if it is -1, the corresponding mesh surface uses the material defined in the surface. Otherwise, the index MUST refer to a valid material in the materials array, and the index MUST NOT exceed the bounds of the materials array. If not defined, the mesh instance does not override any materials, and the mesh's default materials are used.

See [G4MF Material](material.md) for more information about materials.

### Mesh

The `"mesh"` property is an integer index that references a mesh in the document-level `"meshes"` array. This property is required and has no default value.

See [G4MF Mesh](mesh.md) for the details of the properties found on each mesh, which are referred to by index in each mesh instance.

## JSON Schema

- See [g4mf.node.mesh_instance.schema.json](../../schema/mesh/g4mf.node.mesh_instance.schema.json) for the node mesh instance properties JSON schema.
