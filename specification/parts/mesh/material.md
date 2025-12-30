# G4MF Material

## Overview

G4MF uses materials to define the appearance of surfaces. Each material is made of multiple channels, each of which may have a separate modulate factor, texture, and more. Materials are stored in the document-level `"materials"` array, and each surface in a mesh may reference a material by its index in the array. Material channels may have bindings for per-element data and/or texture mapping. Channel data may be thought of as colors, but they may also encode other data, such as normal vectors, or ORM values.

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

The `"normal"` property is an object that defines the normal map channel of the material. If not defined, the default is a flat normal map with no texture, which means the surface has flat shading and uses only the normals derived from the geometry itself for light angle calculations (see [Calculating Cell Normals](mesh.md#calculating-cell-normals)).

Note that the "colors" in normal maps are not visual colors, but instead encode vectors. For example, a 4D material may use three or four numbers in a color, RGB(A), to encode a 4D normal vector's XYZ(W) components, similar to how a 3D material may use two or three numbers in a color, RG(B), to encode a 3D normal vector's XY(Z) components. Generalizing further, a 5D, 6D, 7D, etc material may use four, five, six, seven, etc numbers in a color to encode a 5D, 6D, 7D, etc normal vector's XYZW(VUT) components, at which point the data is no longer interpretable as an RGB(A) color. This is why the material channel properties use generic names like `"factor"` and `"elementMap"` instead of specific names like `"color"` and `"perSimplexColor"`.

In the form of colors or textures, the red channel represents the X component, the green channel represents the Y component, the blue channel represents the Z component, and the alpha channel represents the W component of the normal vector. Alternatively, if the texture refers to a format with dedicated normal channels, such as OpenEXR, use those channels instead of red, green, blue, and alpha. This allows for a single OpenEXR texture to encode potentially dozens of channels, including dedicated channels for normals. For 6D and higher-dimensional materials, a standard RGBA texture cannot encode the normals, and therefore formats like OpenEXR are required, or alternatively, the normals may be encoded in the per-vertex data.

When importing normal maps from textures, the texture MUST be interpreted as raw linear data, not as a color in any color space. Each color channel's data is mapped to a range of -1.0 to 1.0, representing the coordinates of a normal vector relative to the local surface. All Z values, used for depth, MUST exist in the positive part of this range. For example, with a floating-point 4D normal map texture, the red, green, and alpha channels have 0.0 to 1.0 values remapped to -1.0 to 1.0, while the blue channel has 0.5 to 1.0 values remapped to 0.0 to 1.0, where all pixels MUST have a blue channel value greater than 0.5. For example, with an 8-bit integer 4D normal map texture, the red, green, and alpha channels have 0 to 255 values remapped to -1.0 to 1.0, while the blue channel has 128 to 255 values remapped to 0.004 to 1.0, where all pixels MUST have a blue channel value greater than or equal to 128.

### ORM

The `"orm"` property is an object that defines the occlusion, roughness, and metallic channel of the material. If not defined, the default is a rough material with no texture.

The occlusion, roughness, and metallic values are all packed together. In the form of colors or textures, the red channel represents the occlusion value, the green channel represents the roughness value, and the blue channel represents the metallic value. This is the industry standard layout for ORM, and is codified as a requirement in the G4MF specification. If the texture has an alpha channel, this is not used. Alternatively, if the texture refers to a format with dedicated occlusion, roughness, and metallic channels, such as OpenEXR, use those channels instead of red, green, and blue. This allows for a single OpenEXR texture to encode potentially dozens of channels, including dedicated channels for occlusion, roughness, and metallic.

The default is a rough material with no texture, which means the surface has an occlusion value of `0.0`, a roughness value of `1.0`, and a metallic value of `0.0`. The ORM values should be on a range of `0.0` to `1.0`.

## Material Channel Properties

| Property       | Type       | Description                                                               | Default                   |
| -------------- | ---------- | ------------------------------------------------------------------------- | ------------------------- |
| **elementMap** | `object`   | A binding that associates channel values to mesh surface elements.        | No binding.               |
| **factor**     | `number[]` | The modulate factor, value, or RGB(A) color for the channel.              | No factor.                |
| **texture**    | `integer`  | The index of the texture used by the texture map.                         | No texture.               |
| **textureMap** | `object`   | A binding that overrides the mesh surface's texture map for this channel. | Uses surface texture map. |

### Element Map

The `"elementMap"` property is a binding object that associates channel values to mesh surface elements through indices. If not defined, the channel does not have per-element data.

Use `"values"` to store the channel data (color values, normal values), and associate that data with parts of the mesh using the binding's index properties. For example, with the `baseColor` channel, `"simplexes"` allows per-index coloring in each simplex cell (corners), `"perSimplex"` allows one color per entire simplex cell, `"vertices"` allows coloring the vertices shared between multiple cells, `"geometry"` allows coloring polytope elements or their decompositions, and so on.

See [G4MF Mesh Surface Bindings](bindings.md) for more information on how bindings work.

### Factor

The `"factor"` property is an array of numbers that defines the modulate factor, also known as value or single color, for the channel. For `"baseColor"`, this is the RGB(A) color value in linear space. If not defined, the default depends on the channel (white for base color, black for emissive, etc).

If used together with other properties, this acts as a modulate which is per-component multiplied with the other properties. The color is represented as an array of usually three or four numbers, each usually in the range 0.0 to 1.0, but may go above 1.0 for overbright colors. A plain white color of `[1.0, 1.0, 1.0]` produces no modulation.

### Texture

The `"texture"` property is an integer index that references a texture used by the texture map. If not defined, the channel does not have a texture.

Usually, a texture's dimension is 1 dimension less than the dimension of the mesh. For 3D meshes, the texture is usually a 2D texture. For 4D meshes, the texture is usually a 3D texture. However, any dimension of texture is allowed. A 4D mesh may use a 2D texture, though this is not very useful because it will look untextured from certain angles. Alternatively, a 4D mesh may use a 4D texture, mapping the 4D vertices in the same dimension as the texture coordinates.

This property is intended to be used together with the `"textureMap"` property, but may be used without it. In the case of using a 4D texture on a 4D mesh, the mesh's local vertex positions are directly used as texture coordinates, and the `"textureMap"` property is not required.

This is a reference to a texture defined in the G4MF document-level `"textures"` array. The texture MUST be defined in the same file as the material. If not defined, the channel does not have a texture, but a texture map may still be defined and used by extensions.

### Texture Map

The `"textureMap"` property is a binding object that overrides the mesh surface's texture map for this channel. If not defined, the mesh surface's texture map is used instead.

A texture map, also known as a UV map, UVW map, or texture coordinate map, contains texture coordinates, and information on how those coordinates bind to domains. The `"values"` accessor within the texture map MUST have its vector size set to the dimension of the texture space, MUST have a floating-point `componentType`, and the numbers within are usually on a range of 0.0 to 1.0.

The binding's index properties (such as `"vertices"`, `"edges"`, `"simplexes"`, or `"geometry"` decompositions) control how the texture coordinate values are associated with mesh elements. See [G4MF Mesh Surface Bindings](bindings.md) for more information.

Texture map transforms, such as those supplied by `KHR_texture_transform` in glTF™, are not supported in G4MF. Instead, any texture transforms present in an application, such as scaling or translation, MUST be baked into the texture coordinates in the accessor when exporting the G4MF file. If dynamic texture transforms are required, such as for animation purposes, they may be defined by an extension, as long as the actual texture coordinates in the texture map properties have the current transforms baked in at export time.

## JSON Schema

- See [g4mf.material.schema.json](../../schema/mesh/g4mf.material.schema.json) for the material properties JSON schema
- See [g4mf.material.channel.schema.json](../../schema/mesh/g4mf.material.channel.schema.json) for the material channel properties JSON schema.
