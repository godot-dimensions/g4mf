# G4MF Blend Shape Mesh Deformation

## Overview

G4MF allows meshes to be deformed using blend shapes, also known as shape keys or morph targets. This feature enables the creation of complex animations and transformations by defining how a mesh can be altered by displacing its vertex positions and other attributes. For example, blend shapes are often used for facial animations, where the mouth, eyes, and other features can be morphed into different expressions or lip synced to match audio.

## Example

The following example defines a mesh with one blend shape that deforms the mesh's vertex positions and normals. The blend shape is activated by an amount of `0.5`, which means the displayed mesh will be deformed halfway between the base mesh data and the fully activated blend shape.

```json
{
    "meshes": [
        {
            "name": "ExampleMesh",
            "vertices": 0,
            "surfaces": [
                {
                    "name": "ExampleMeshSurface",
                    "material": 0,
                    "simplexes": 1,
                    "normals": {
                        "values": 2,
                        "simplexes": 3
                    }
                }
            ],
            "blend": {
                "amounts": [0.5],
                "shapes": [
                    {
                        "name": "Smile",
                        "position": {
                            "indices": 4,
                            "offsets": 5
                        },
                        "surfaces": [
                            {
                                "surface": 0,
                                "normal": {
                                    "indices": 6,
                                    "offsets": 7
                                }
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```

## Mesh Blend Properties

| Property    | Type       | Description                                                             | Default                                  |
| ----------- | ---------- | ----------------------------------------------------------------------- | ---------------------------------------- |
| **amounts** | `number[]` | How much each blend shape is activated and influences the mesh.         | All-zero array of size equal to `shapes` |
| **shapes**  | `object[]` | Array of blend shapes that define the deformations applied to the mesh. | Required, no default.                    |

In addition to these listed properties, blend shapes are highly recommended to define the `"name"` property, which is a unique human-readable name for the blend shape, allowing applications to interpret the purpose of the blend shape, or simply display it to the user.

### Amounts

The `"amounts"` property is an array of numbers that specifies how much each blend shape is activated. If not defined, all amounts are implicitly set to `0.0`.

Blend amounts are also known as weights or activations. Each value typically ranges from `0.0` to `1.0`, where `0.0` means no influence and `1.0` means full influence, but values can exceed this range for exaggerated effects, or use negative values for inverted effects. The size of this array must match the number of items in the `shapes` array, or if `amounts` is not explicitly defined, `amounts` is implicitly defined to be the same size as `shapes` filled with all values set to `0.0`.

### Shapes

The `"shapes"` property is an array of objects that define the blend shapes, also known as morph targets. This property is required and does not have a default value.

Each blend shape may contain any of the below properties, including none or multiple at once, to define how the various attributes of the mesh are deformed by the blend shape. Additional properties may be added by extensions to allow for more complex deformations.

## Blend Shape Properties

| Property     | Type       | Description                                               | Default          |
| ------------ | ---------- | --------------------------------------------------------- | ---------------- |
| **position** | `object`   | The offset or displacement of the vertex position values. | No displacement. |
| **surfaces** | `object[]` | The offset or displacement of per-surface data.           | No displacement. |

### Position

The `"position"` property is an object that defines the offset or displacement of the vertex positions for the blend shape relative to the base mesh's `vertices` property. This property is optional and defaults to no displacement.

This property uses the [Blend Shape Target](#blend-shape-target-properties) schema to contain the indices and offsets.

### Surfaces

The `"surfaces"` property is an array of objects that define the offset or displacement of any per-surface data for the blend shape. This property is optional and defaults to no displacement.

Surface data includes normals, texture maps, and any other per-surface attributes that may be defined in the mesh, either by future spec versions or by extensions. The amount of items in the blend shape's surfaces array may be less than the number of surfaces in the mesh, but MUST NOT exceed the number of surfaces in the mesh. Each surface object in the `"surfaces"` array explicitly points to a surface in the mesh using the `"surface"` property, which is an integer index into the mesh's `"surfaces"` array.

If a given blend shape surface object has no properties other than `"surface"`, it MUST be omitted entirely rather than set to an object with only a `"surface"` index. Furthermore, if there is no per-surface data for this blend shape, the `"surfaces"` property MUST be omitted entirely rather than set to an empty array.

## Blend Shape Surface Properties

| Property       | Type      | Description                                                            | Default               |
| -------------- | --------- | ---------------------------------------------------------------------- | --------------------- |
| **normal**     | `object`  | The offset or displacement of the normal direction values.             | No displacement.      |
| **surface**    | `integer` | The index of the surface in the mesh that this blend shape applies to. | Required, no default. |
| **textureMap** | `object`  | The offset or displacement of the texture map coordinate values.       | No displacement.      |

### Normal

The `"normal"` property is an object that defines the offset or displacement of the normal direction values for this blend shape surface. This property is optional and defaults to no displacement.

This property uses the [Blend Shape Target](#blend-shape-target-properties) schema to contain the indices and offsets.

Normals MUST be re-normalized before rendering after applying all blend shapes for a mesh.

### Surface

The `"surface"` property is an integer that defines the index of the surface in the mesh that this blend shape applies to. This property is required and has no default value.

This property explicitly points to a surface in the mesh. The value MUST be a valid index into the mesh's `"surfaces"` array, and MUST NOT exceed the bounds of the mesh's surfaces array. Each blend shape surface in the array MUST have a unique surface index, such that there is at most one blend shape surface object in a given blend shape for each surface in the mesh.

### Texture Map

The `"textureMap"` property is an object that defines the offset or displacement of the texture map's texture space coordinate values for this blend shape surface. This property is optional and defaults to no displacement.

This property uses the [Blend Shape Target](#blend-shape-target-properties) schema to contain the indices and offsets.

## Blend Shape Target Properties

| Property    | Type      | Description                                                                   | Default               |
| ----------- | --------- | ----------------------------------------------------------------------------- | --------------------- |
| **indices** | `integer` | The index of the accessor that contains the indices of the items to target.   | Required, no default. |
| **offsets** | `integer` | The index of the accessor that contains the offsets to displace the items by. | Required, no default. |

### Indices

The `"indices"` property is an integer that defines the index of the accessor that contains the indices for the mesh deformation blend shape morph target. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an unsigned integer component type, and MUST have the `"vectorSize"` property undefined or set to its default value of 1. Each index in this accessor corresponds to an item in the mesh that the blend shape morph target applies to, such as a vertex position, normal direction value, or another attribute, and MUST NOT exceed the number of items in the targeted accessor.

### Offsets

The `"offsets"` property is an integer that defines the index of the accessor that contains the offsets or displacements for the mesh deformation blend shape morph target. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have the `"vectorSize"` property set to the type expected for the targeted attribute. For example, for a 4D mesh, targeting vertex positions needs `"vectorSize"` set to 4, while targeting texture space coordinates needs `"vectorSize"` set to the dimension of the texture space.

## JSON Schema

- See [g4mf.mesh.blend.schema.json](../../schema/mesh/deformation/g4mf.mesh.blend.schema.json) for the blend shape properties JSON schema.
- See [g4mf.mesh.blend.shape.schema.json](../../schema/mesh/deformation/g4mf.mesh.blend.shape.schema.json) for the blend shape properties JSON schema.
- See [g4mf.mesh.blend.shape.surface.schema.json](../../schema/mesh/deformation/g4mf.mesh.blend.shape.surface.schema.json) for the blend shape surface properties JSON schema.
- See [g4mf.mesh.blend.shape.target.schema.json](../../schema/mesh/deformation/g4mf.mesh.blend.shape.target.schema.json) for the blend shape target properties JSON schema
