# G4MF Material

## Overview

G4MF uses materials to define the appearance of surfaces. Each material is made of multiple channels, each of which may have a separate color, texture, and more. Materials are stored in the document-level `"materials"` array, and each surface in a mesh may reference a material by its index in the array. Material channels may have per-cell colors, per-edge colors, per-vertex colors, and/or texture mapping, each of which points to an accessor that encodes the data (see [G4MF Data](data.md)).

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

### Normal

The `"normal"` property is an object that defines the normal map channel of the material. If not defined, the default is a flat normal map with no texture, which means the surface has flat shading and only uses the cell normals for light angle calculations.

### ORM

The `"orm"` property is an object that defines the occlusion, roughness, and metallic channel of the material. If not defined, the default is a rough material with no texture.

The default is a rough material with no texture, which means the surface has an occlusion value of `0.0`, a roughness value of `1.0`, and a metallic value of `0.0`. The ORM values should be on a range of `0.0` to `1.0`.

## Material Channel Properties

| Property           | Type       | Description                                                                             | Default              |
| ------------------ | ---------- | --------------------------------------------------------------------------------------- | -------------------- |
| **color**          | `number[]` | The RGB(A) color value for the channel.                                                 | No color.            |
| **cellColors**     | `integer`  | The index of the accessor that contains the per-cell color data for this channel.       | No cell colors.      |
| **edgeColors**     | `integer`  | The index of the accessor that contains the per-edge color data for this channel.       | No edge colors.      |
| **vertexColors**   | `integer`  | The index of the accessor that contains the per-vertex color data for this channel.     | No vertex colors.    |
| **cellTextureMap** | `integer`  | The index of the accessor that contains the per-cell texture map data for this channel. | No cell texture map. |
| **cellTexture**    | `integer`  | The index of the texture used by the texture map.                                       | No cell texture.     |

### Color

The `"color"` property is an array of numbers that defines the RGB(A) color value for the channel. If not defined, the default depends on the channel (white for base color, black for emissive, etc).

If used together with other properties, this acts as a modulate which is per-component multiplied with the other properties. The color is represented as an array of usually three or four numbers, each usually in the range 0.0 to 1.0, but may go above 1.0 for overbright colors. A plain white color of `[1.0, 1.0, 1.0]` produces no modulation.

### Cell Colors

The `"cellColors"` property is an integer index that references an accessor containing the per-cell color data for this channel. If not defined, the channel does not have per-cell colors.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type, and values are usually on a range of 0.0 to 1.0. If defined, the amount of cell colors MUST match or exceed the amount of cells in all surfaces that use this channel.

### Edge Colors

The `"edgeColors"` property is an integer index that references an accessor containing the per-edge color data for this channel. If not defined, the channel does not have per-edge colors.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type, and values are usually on a range of 0.0 to 1.0. If defined, the amount of edge colors MUST match or exceed the amount of edges in all surfaces that use this channel.

### Vertex Colors

The `"vertexColors"` property is an integer index that references an accessor containing the per-vertex color data for this channel. If not defined, the channel does not have per-vertex colors.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type, and values are usually on a range of 0.0 to 1.0. If defined, the amount of vertex colors MUST match or exceed the amount of vertices in all surfaces that use this channel.

### Cell Texture Map

The `"cellTextureMap"` property is an integer index that references an accessor containing the per-cell texture map data for this channel. If not defined, the channel does not have per-cell texture maps.

A texture map, also known as a UV map, UVW map, or texture coordinate map, is a mapping from the indices of the cell vertices to the texture coordinates. The texture coordinates are usually on a range of 0.0 to 1.0. For 3D meshes, the texture coordinates usually refer to a 2D texture. For 4D meshes, the texture coordinates usually refer to a 3D texture. However, any dimension of texture coordinates is allowed. A 4D mesh may use a 2D texture, though this is not very useful because it will look untextured from certain angles, or a 4D texture, mapping the 4D vertices in the same dimension as the texture coordinates. This property is intended to be used together with the `"cellTexture"` property, but may be used without it, such as when defining a texture map for an untextured surface.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type. The accessor MUST have its vector size set to the dimension of the texture space, which may be `cellTexture` or defined by an extension. The amount of vector elements in the accessor MUST match or exceed the amount of primitive numbers in the cells array of all surfaces that use this channel.

### Cell Texture

The `"cellTexture"` property is an integer index that references a texture used by the texture map. If not defined, the channel does not have a cell texture.

Usually, a texture's dimension is 1 dimension less than the dimension of the mesh. For 3D meshes, the texture is usually a 2D texture. For 4D meshes, the texture is usually a 3D texture. However, any dimension of texture is allowed. A 4D mesh may use a 2D texture, though this is not very useful because it will look untextured from certain angles, or a 4D texture, mapping the 4D vertices in the same dimension as the texture coordinates. This property is intended to be used together with the `"cellTextureMap"` property, but may be used without it, such as when using a 4D texture on a 4D mesh and the local vertex positions are directly used as texture coordinates.

This is a reference to a texture defined in the G4MF document-level `"textures"` array. The texture MUST be defined in the same file as the material. If not defined, the channel does not have a texture, but a texture map may still be defined and used by extensions.
