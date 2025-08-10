# G4MF Material

## Overview

G4MF uses materials to define the appearance of surfaces. Each material is made of multiple channels, each of which may have a separate modulate factor, texture, and more. Materials are stored in the document-level `"materials"` array, and each surface in a mesh may reference a material by its index in the array. Material channels may have per-cell data, per-edge data, per-vertex data, and/or texture mapping, each of which points to an accessor that encodes the data (see [G4MF Data](data.md)). Channel data may be thought of as colors, but they may also encode other data, such as normal vectors, or ORM values.

## Example

The following example defines.

## Material Properties

| Property      | Type     | Description                                                     | Default |
| ------------- | -------- | --------------------------------------------------------------- | ------- |
| **baseColor** | `object` | The base color channel of the material.                         | White   |
| **emissive**  | `object` | The emissive color channel of the material.                     | Black   |
| **normal**    | `object` | The normal map channel of the material.                         | Flat    |
| **orm**       | `object` | The occlusion, roughness, and metallic channel of the material. | Rough   |

### Base Color

The `"baseColor"` property is an object that defines the base color channel of the material. If not defined, the default is a white color with no texture.

The base color is also known as the albedo color or diffuse color. It is the color of the surface when illuminated by white light.

### Emissive

The `"emissive"` property is an object that defines the emissive color channel of the material. If not defined, the default is a black color with no texture, which means the surface does not emit light.

The emissive strength can be controlled by increasing the `"factor"` property of the emissive channel. For emissive materials, the `"factor"` property may go beyond the normal range of 0.0 to 1.0, allowing for highly emissive materials.

### Normal

The `"normal"` property is an object that defines the normal map channel of the material. If not defined, the default is a flat normal map with no texture, which means the surface has flat shading and only uses the cell normals for light angle calculations.

Note that the "colors" in normal maps are not visual colors, but instead encode vectors. For example, a 4D material may use three or four numbers in a color, RGB(A), to encode a 4D normal vector's XYZ(W) components, similar to how a 3D material may use two or three numbers in a color, RG(B), to encode a 3D normal vector's XY(Z) components. Generalizing further, a 5D, 6D, 7D, etc material may use four, five, six, seven, etc numbers in a color to encode a 5D, 6D, 7D, etc normal vector's XYZW(VUT) components, at which point the data is no longer interpretable as an RGB(A) color. This is why the material channel properties use generic names like `"factor"` and `"perCell"` instead of specific names like `"color"` and `"perCellColor"`.

In the form of colors or textures, the red channel represents the X component, the green channel represents the Y component, the blue channel represents the Z component, and the alpha channel represents the W component of the normal vector. Alternatively, if the texture refers to a format with dedicated normal channels, such as OpenEXR, use those channels instead of red, green, blue, and alpha. This allows for a single OpenEXR texture to encode potentially dozens of channels, including dedicated channels for normals. For 6D and higher-dimensional materials, a standard RGBA texture cannot encode the normals, and therefore formats like OpenEXR are required, or alternatively, the normals may be encoded in the per-vertex data.

An object with smooth shading may be represented by having the normal channel's per-vertex data set to the average of the polytope cell normals connected to the vertex, normalized, which sets the vertex normals to the average of the polytope cell normals.

### ORM

The `"orm"` property is an object that defines the occlusion, roughness, and metallic channel of the material. If not defined, the default is a rough material with no texture.

The occlusion, roughness, and metallic values are all packed together. In the form of colors or textures, the red channel represents the occlusion value, the green channel represents the roughness value, and the blue channel represents the metallic value. This is the industry standard layout for ORM, and is codified as a requirement in the G4MF specification. If the texture has an alpha channel, this is not used. Alternatively, if the texture refers to a format with dedicated occlusion, roughness, and metallic channels, such as OpenEXR, use those channels instead of red, green, and blue. This allows for a single OpenEXR texture to encode potentially dozens of channels, including dedicated channels for occlusion, roughness, and metallic.

The default is a rough material with no texture, which means the surface has an occlusion value of `0.0`, a roughness value of `1.0`, and a metallic value of `0.0`. The ORM values should be on a range of `0.0` to `1.0`.

## Material Channel Properties

| Property       | Type       | Description                                                                            | Default             |
| -------------- | ---------- | -------------------------------------------------------------------------------------- | ------------------- |
| **factor**     | `number[]` | The modulate factor, value, or RGB(A) color for the channel.                           | No factor.          |
| **perCell**    | `integer`  | The index of the accessor that contains the per-cell data for this channel.            | No per cell data.   |
| **perEdge**    | `integer`  | The index of the accessor that contains the per-edge data for this channel.            | No per edge data.   |
| **perVertex**  | `integer`  | The index of the accessor that contains the per-vertex-instance data for this channel. | No per vertex data. |
| **textureMap** | `integer`  | The index of the accessor that contains the per-vertex-instance texture map data.      | No texture map.     |
| **texture**    | `integer`  | The index of the texture used by the texture map.                                      | No texture.         |

### Factor

The `"factor"` property is an array of numbers that defines the modulate factor, also known as value or single color, for the channel. For `"baseColor"`, this is the RGB(A) color value in linear space. If not defined, the default depends on the channel (white for base color, black for emissive, etc).

If used together with other properties, this acts as a modulate which is per-component multiplied with the other properties. The color is represented as an array of usually three or four numbers, each usually in the range 0.0 to 1.0, but may go above 1.0 for overbright colors. A plain white color of `[1.0, 1.0, 1.0]` produces no modulation.

### Per Cell

The `"perCell"` property is an integer index that references an accessor containing the per-cell data for this channel, such as colors. If not defined, the channel does not have per-cell data.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type, and values are usually on a range of 0.0 to 1.0. If defined, the amount of per-cell data MUST match or exceed the amount of cells in all mesh surfaces that use this material.

### Per Edge

The `"perEdge"` property is an integer index that references an accessor containing the per-edge data for this channel, such as colors. If not defined, the channel does not have per-edge data.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type, and values are usually on a range of 0.0 to 1.0. If defined, the amount of per-edge data MUST match or exceed the amount of edges in all mesh surfaces that use this material.

### Per Vertex

The `"perVertex"` property is an integer index that references an accessor containing the per-vertex-instance data for this channel, such as colors. If not defined, the channel does not have per-vertex data.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type, and values are usually on a range of 0.0 to 1.0. If defined, the amount of per-vertex data MUST match or exceed the amount of vertex instances in all mesh surfaces that use this material.

Per vertex data applies to a surface's vertex instances, which depend on the surface's `"cells"` and `"edges"` properties. See [G4MF Mesh Surface Vertex Instances](mesh.md#vertex-instances) for more information on how vertex instances are defined.

### Texture Map

The `"textureMap"` property is an integer index that references an accessor containing the per-cell texture map data for this channel. If not defined, the channel does not have per-cell texture maps.

A texture map, also known as a UV map, UVW map, or texture coordinate map, is a mapping from the indices of the vertex instances to the texture coordinates. Per vertex data applies to a surface's vertex instances, which depend on the surface's `"cells"` and `"edges"` properties. See [G4MF Mesh Surface Vertex Instances](mesh.md#vertex-instances) for more information on how vertex instances are defined.

The texture coordinates are usually on a range of 0.0 to 1.0. For 3D meshes, the texture coordinates usually refer to a 2D texture. For 4D meshes, the texture coordinates usually refer to a 3D texture. However, any dimension of texture coordinates is allowed. A 4D mesh may use a 2D texture, though this is discouraged and not very useful because it will look untextured from certain angles, or a 4D texture, mapping the 4D vertices in the same dimension as the texture coordinates. This property is intended to be used together with the `"texture"` property, but may be used without it, such as when defining a texture map for an untextured surface.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type. The accessor MUST have its `"vectorSize"` set to the dimension of the texture space, which is the same as the dimension of `texture` if defined. For example, a 4D mesh with a 3D texture would have a texture map accessor with a `"vectorSize"` of `3`. The amount of vector elements in the accessor MUST match or exceed the amount of vertex instances of all mesh surfaces that use this channel. For example, a 4D mesh with 10 tetrahedral cells needs at least 40 vector elements in the texture map accessor; with 3D texture coordinates, that means at least 120 numbers in the accessor.

### Texture

The `"texture"` property is an integer index that references a texture used by the texture map. If not defined, the channel does not have a texture.

Usually, a texture's dimension is 1 dimension less than the dimension of the mesh. For 3D meshes, the texture is usually a 2D texture. For 4D meshes, the texture is usually a 3D texture. However, any dimension of texture is allowed. A 4D mesh may use a 2D texture, though this is not very useful because it will look untextured from certain angles. Alternatively, a 4D mesh may use a 4D texture, mapping the 4D vertices in the same dimension as the texture coordinates.

This property is intended to be used together with the `"textureMap"` property, but may be used without it. In the case of using a 4D texture on a 4D mesh, the mesh's local vertex positions are directly used as texture coordinates, and the `"textureMap"` property is not required.

This is a reference to a texture defined in the G4MF document-level `"textures"` array. The texture MUST be defined in the same file as the material. If not defined, the channel does not have a texture, but a texture map may still be defined and used by extensions.

## JSON Schema

See [g4mf.material.schema.json](../schema/g4mf.material.schema.json) for the material properties JSON schema, and [g4mf.material.channel.schema.json](../schema/g4mf.material.channel.schema.json) for the material channel properties JSON schema.
