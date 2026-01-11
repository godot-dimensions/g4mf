# G4MF Blend Shape Mesh Deformation

## Overview

G4MF allows meshes to be deformed using blend shapes, also known as morph targets. This feature enables the creation of complex animations and transformations by defining how a mesh can be altered by displacing its vertex positions and other attributes. For example, blend shapes are often used for facial animations, where the mouth, eyes, and other features can be morphed into different expressions or lip synced to match audio.

## Example

The following example defines.

## Mesh Blend Properties

| Property    | Type       | Description                                                             | Default                                  |
| ----------- | ---------- | ----------------------------------------------------------------------- | ---------------------------------------- |
| **amounts** | `number[]` | How much each blend shape is activated and influences the mesh.         | All-zero array of size equal to `shapes` |
| **shapes**  | `object[]` | Array of blend shapes that define the deformations applied to the mesh. | Required, no default.                    |

### Amounts

The `"amounts"` property is an array of numbers that specifies how much each blend shape is activated. If not defined, all amounts are implicitly set to `0.0`.

Blend amounts are also known as weights or activations. Each value typically ranges from `0.0` to `1.0`, where `0.0` means no influence and `1.0` means full influence, but values can exceed this range for exaggerated effects, or use negative values for inverted effects. The size of this array must match the number of items in the `shapes` array, or if `amounts` is not explicitly defined, `amounts` is implicitly defined to be the same size as `shapes` filled with all values set to `0.0`.

### Shapes

The `"shapes"` property is an array of objects that define the blend shapes, also known as morph targets. This property is required and does not have a default value.

Each blend shape may contain any of the below properties, including none or multiple at once, to define how the various attributes of the mesh are deformed by the blend shape. Additional properties may be added by extensions to allow for more complex deformations.

In addition to the below listed properties, blend shapes are highly recommended to define the `"name"` property, which is a unique human-readable name for the blend shape, allowing applications to interpret the purpose of the blend shape, or simply display it to the user.

## Blend Shape Properties

| Property               | Type     | Description                                                               | Default          |
| ---------------------- | -------- | ------------------------------------------------------------------------- | ---------------- |
| **normal**             | `object` | The offset or displacement of the per-vertex-instance normals.            | No displacement. |
| **position**           | `object` | The offset or displacement of the vertex positions.                       | No displacement. |
| **textureMap**         | `object` | The offset or displacement of the per-vertex-instance texture map.        | No displacement. |
| **topologyNormal**     | `object` | Like `"normal"` but for the per-topology-vertex-instance normals.         | No displacement. |
| **topologyTextureMap** | `object` | Like `"textureMap"` but for the per-topology-vertex-instance texture map. | No displacement. |

All of these properties use the [Blend Shape Target](#blend-shape-target-properties) schema to contain the indices and offsets.

### Normal

The `"normal"` property is an object that defines the offset or displacement of the per-vertex-instance normals for the blend shape. This property is optional and defaults to no displacement.

If the mesh has multiple surfaces, the blend shape target indices are a combination of the per-vertex-instance indices for all surfaces in the mesh. For example, for a 4D mesh with two surfaces, the first with 10 tetrahedral simplex cells and the second with 20 tetrahedral simplex cells, indices 0 to 39 refer to the first surface's vertex indices, and indices 40 to 119 refer to the second surface's vertex indices.

Normals MUST be re-normalized after applying all blend shapes for a mesh.

### Position

The `"position"` property is an object that defines the offset or displacement of the vertex positions for the blend shape relative to the base mesh's `vertices` property. This property is optional and defaults to no displacement.

### Texture Map

The `"textureMap"` property is an object that defines the offset or displacement of the per-vertex-instance texture space coordinates for the blend shape. This property is optional and defaults to no displacement.

If the mesh has multiple surfaces, the blend shape target indices are a combination of the per-vertex-instance indices for all surfaces in the mesh. For example, for a 4D mesh with two surfaces, the first with 10 tetrahedral simplex cells and the second with 20 tetrahedral simplex cells, indices 0 to 39 refer to the first surface's vertex indices, and indices 40 to 119 refer to the second surface's vertex indices.

### Topology Normal

The `"topologyNormal"` property is an object that defines the offset or displacement of the per-topology-vertex-instance normals for the blend shape. This property is optional and defaults to no displacement.

If the mesh has multiple surfaces, the blend shape target indices are a combination of the per-topology-vertex-instance indices for all boundary geometry items in all mesh surfaces. For example, for a 4D mesh with two surfaces, the first with 10 cubic cells and the second with 20 cubic cells, indices 0 to 79 refer to the first surface's topology vertex indices, and indices 80 to 239 refer to the second surface's topology vertex indices.

Normals MUST be re-normalized after applying all blend shapes for a mesh.

### Topology Texture Map

The `"topologyTextureMap"` property is an object that defines the offset or displacement of the per-topology-vertex-instance texture space coordinates for the blend shape. This property is optional and defaults to no displacement.

If the mesh has multiple surfaces, the blend shape target indices are a combination of the per-topology-vertex-instance indices for all boundary geometry items in all mesh surfaces. For example, for a 4D mesh with two surfaces, the first with 10 cubic cells and the second with 20 cubic cells, indices 0 to 79 refer to the first surface's topology vertex indices, and indices 80 to 239 refer to the second surface's topology vertex indices.

This property may only be used when at least one mesh surface has the `"

## Blend Shape Target Properties

| Property    | Type      | Description                                                                   | Default               |
| ----------- | --------- | ----------------------------------------------------------------------------- | --------------------- |
| **indices** | `integer` | The index of the accessor that contains the indices of the items to target.   | Required, no default. |
| **offsets** | `integer` | The index of the accessor that contains the offsets to displace the items by. | Required, no default. |

### Indices

The `"indices"` property is an integer that defines the index of the accessor that contains the indices for the mesh deformation blend shape morph target. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an unsigned integer component type, and MUST have the `"vectorSize"` property undefined or set to its default value of 1. Each index in this accessor corresponds to an item in the mesh that the blend shape morph target applies to, such as a vertex position, per-vertex-instance normal, or another attribute, and MUST NOT exceed the number of items in the targeted accessor.

### Offsets

The `"offsets"` property is an integer that defines the index of the accessor that contains the offsets or displacements for the mesh deformation blend shape morph target. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have the `"vectorSize"` property set to the type expected for the targeted attribute. For example, for a 4D mesh, targeting vertex positions needs `"vectorSize"` set to 4, while targeting texture space coordinates needs `"vectorSize"` set to the dimension of the texture space.

## JSON Schema

- See [g4mf.mesh.blend.schema.json](../../schema/mesh/g4mf.mesh.blend.schema.json) for the mesh blend properties JSON schema.
- See [g4mf.mesh.blend.shape.schema.json](../../schema/mesh/deformation/g4mf.mesh.blend.shape.schema.json) for the blend shape properties JSON schema.
- See [g4mf.mesh.blend.shape.target.schema.json](../../schema/mesh/deformation/g4mf.mesh.blend.shape.target.schema.json) for the blend shape target properties JSON schema
