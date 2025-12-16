# G4MF Texture

## Overview

G4MF textures are N-dimensional images with an optional sampler, which may be referenced by the `"texture"` property in material channels, or used for any other purpose. Multiple images may be used to define high-dimensional textures, such as 3D textures, and optionally provide fallback images of different formats.

## Example

The following example defines.

## Texture Properties

| Property        | Type        | Description                                             | Default                |
| --------------- | ----------- | ------------------------------------------------------- | ---------------------- |
| **images**      | `object[]`  | An array of zero or more images that this texture uses. | `[]` (no images)       |
| **placeholder** | `number[]`  | The color to use when no images are available.          | Required, no default.  |
| **sampler**     | `object`    | The sampler settings used for the texture.              | `{}` (default sampler) |
| **size**        | `integer[]` | The size or resolution of the texture in pixels.        | Required, no default.  |

### Images

The `"images"` property is an array of objects that defines the images used by the texture. If not specified or empty, the texture has no images.

Each image is a [G4MF File Reference](core.md#file-references) which references image data stored in a file or in a buffer view, and MUST declare its MIME type using the `"mimeType"` property. File names SHOULD use snake case and all lowercase letters to avoid case sensitivity issues across platforms, such as `my_texture.png`. If a texture has one image and it is stored in a file, the texture SHOULD have its name property set to the name of the file, excluding the file extension. For example, `{ "images": [{ "mimeType": "image/png", "uri": "my_texture.png" }], "name": "my_texture" }`. This is recommended for the purposes of clarity and semantic preservation during embedding, but any name is allowed, including no name at all.

The file reference's URI may be relative to the G4MF file's location, or alternatively, may be a web address, or any other valid URI format. If the URI starts with `https://`, it is treated as a web address and indicates the model is located there. Implementations may cache and reuse downloaded models as they see fit. If the URI starts with any other scheme, it uses that protocol. If the URI does not contain `://`, it is treated as a relative path to the G4MF file's location.

Images SHOULD NOT contain embedded color space profiles (ICC profiles) or other metadata that alters the visual appearance of the image. This is to ensure that the image is displayed consistently in applications that do not support color spaces or other visual-affecting metadata.

Images may use any format that supports being imported as a grid of pixels, particularly MIME types starting with `image/`. This means the MIME type is not limited to a specific set of values, but may be any valid MIME type. Implementations are highly encouraged to support at least the PNG, JPEG, and WebP formats (`image/png`, `image/jpeg`, and `image/webp`). When a media type is registered with IANA, the `"mimeType"` MUST match the media type string as registered with IANA. When a media type is not registered with IANA, any placeholder name may be used pending registration.

For more information on MIME types, see the list of IANA media types: https://www.iana.org/assignments/media-types/media-types.xhtml#image

See [Assembling High-Dimensional Textures](#assembling-high-dimensional-textures) below for more information on how to represent high-dimensional textures using multiple images.

### Placeholder

The `"placeholder"` property is an array of numbers that defines the color to use when no images are available. This property is required and has no default value.

This value is NOT a modulate color applied to the texture. It is only used when the texture cannot fill the given pixels due to no images being available, such as when the `"images"` array is empty, all image formats are unsupported, or there is not enough image data to fill the texture.

This value is a floating-point color on the range of 0.0 to 1.0, in linear color space as described in [G4MF Coordinate System Colors](coordinate_system.md#colors). If using this value to fill in pixel values with a different target color space, the values MUST be converted to the target color space before being used. For example, a linear value of 1.0 corresponds to 255 in traditional 8-bit integer image formats, while the linear value 0.5 may correspond to 127 (or 128) in linear 8-bit integer image formats, 187 (or 188) in non-linear sRGB 8-bit integer image formats, or 0.7354 in non-linear sRGB floating-point image formats.

The array's length defines the number of color channels in the texture used by the G4MF file, even if it does not match the color channels found in the images. For example, an image with RGB color channels used as an RGB color texture would have a placeholder array of length 3. For example, an image with RGBA color channels used as an opaque RGB color texture would have a placeholder array of length 3, with the alpha channel ignored. For example, an image with RGB color channels used as a transparent RGBA color texture would have a placeholder array of length 4, using the 4th placeholder value for the alpha channel. For example, an OpenEXR image with 10 color channels used as a 10-dimensional normal map texture would have a placeholder array of length 10.

### Sampler

The `"sampler"` property is an object that defines how the texture is sampled when resized or read outside of its bounds. This property is optional and defaults to an empty object, which means the default sampler settings are used.

See [Texture Filtering](#texture-filtering) and [Texture Sampler Properties](#texture-sampler-properties) below for more information on the sampler properties.

### Size

The `"size"` property is an array of integers that defines the size or resolution of the texture in pixels. This property is required and has no default value.

The `"size"` array MUST have at least one item, and each item MUST be a positive integer, not zero or negative. The length of the array defines the dimension of the texture. For example, a 2D texture may have a size of `[1024, 1024]`, or a 3D texture may have a size of `[128, 128, 128]`. Textures are RECOMMENDED to have power-of-two sizes and be the same in all dimensions, but any size is allowed.

## Assembling High-Dimensional Textures

When texturing the 3D surface of a 4D mesh, a 3D texture is required. There are some image formats with capability for volumetric 3D image data, such as [KTX2 3D textures](https://github.com/donmccurdy/KTX2-Samples/tree/main/ktx2) and [JPEG 2000 Part 10 - Extensions for Three-Dimensional Data](https://ieeexplore.ieee.org/document/1693474). However, these formats are not widely supported by image editors and other applications, and also they only provide up to 3D textures, while G4MF allows textures to be of any dimension.

G4MF provides a built-in way to assemble high-dimensional textures from lower-dimensional images by allowing the image data to be sliced and stacked together as needed. This technique is also known as "flipbook" textures, commonly used for animation frames. This is the dominant way 3D textures are made in game engines, such as in Godot's [Texture3D](https://docs.godotengine.org/en/stable/classes/class_texture3d.html), Unity's [Texture3D](https://docs.unity3d.com/6000.2/Documentation/Manual/class-Texture3D.html), and Unreal Engine's [Volume Texture](https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-volume-textures?application_version=4.27). G4MF supports textures of any dimension, including 2D textures, 3D textures, 4D textures, and beyond.

The first two numbers in the `"size"` array define the width and height of the slice size. Each image's size MUST be a whole multiple of the slice size. For example, a texture with a width of 64 requires all images to have a width of 64, 128, 192, 256, and so on. The amount of multiples in the image defines how many slices exist in the image, and are then stacked together to form the full texture, until the full texture is filled with pixels.

Here are several examples of how to represent high-dimensional textures:

- A 3D texture with a size of `[64, 64, 64]` may be represented by 64 images, each with a size of 64x64 pixels. Each image only contains a single slice, so 64 of them are stacked together.
- A 3D texture with a size of `[64, 64, 64]` may be represented by 1 image with a size of 4096x64 pixels. 4096 divided by 64 is 64, so the image contains 64 slices arranged in a single row, and all need to be stacked together.
- A 3D texture with a size of `[64, 64, 64]` may be represented by 1 image with a size of 512x512 pixels. 512 divided by 64 is 8, so the image contains an 8x8 grid of slices, and all need to be stacked together, starting with the first slice in the top-left corner, then the rest of the slices in the same row, and then the next row, until all slices are stacked together.
- A 3D texture with a size of `[64, 64, 64]` may be represented by 4 images, each with a size of 256x256 pixels. Each image contains a 4x4 grid of slices, so the first image contains slices 0 to 15, the second image contains slices 16 to 31, and so on. This combines the previous examples of multiple images and multiple slices per image.
- A 3D texture with a size of `[64, 64, 64]` may be represented by 1 image of a 3D image format such as KTX2 with a size of 64x64x64 pixels. This is the most straightforward option, but requires support for the specific image format. G4MF permits this, but does not require support for it.
- A 3D texture with a size of `[64, 64, 64]` may be represented by no images at all. In this case, the image data would default to a texture filled with the `"placeholder"` value, unless an extension provides more data. Extensions may be used to define procedural textures, such as a noise texture, or a texture generated from a shader.
- A 3D texture with a size of `[256, 256, 256]` may be represented by 1 image with a size of 4096x4096 pixels. 4096 divided by 256 is 16, so the image contains a 16x16 grid of slices, for 256 total slices. Practical limits mean that 3D texture resolutions are usually stuck with low resolutions, since even a 256x256x256 cube of voxels has the same amount of pixels as a 4K image. However, those are guidelines, G4MF does not impose any arbitrary hard limits on the size of textures.
- A 4D texture with a size of `[64, 64, 64, 64]` may be represented by 1 image with a size of 4096x4096 pixels. 4096 divided by 64 is 64, so the image contains a 64x64 grid of slices, for 4096 total slices. The slices first build a 3D image, in this case all the slices in the first row. Then the next slices build the next 3D image, and so on, then all 3D images are stacked together to form the 4D texture. A 4D texture may be used to texture a 4D mesh without texture mapping, or may be used to texture the 4D surface of a 5D mesh.

Image pixels may be split and stacked, but MUST NOT be stitched together. For example, a 2D texture with a size of `[64, 64]` MUST NOT be represented by 4 images with a size of 32x32 pixels each. If this invalid data existed, it MUST fail validation because 32 is not a multiple of 64, and all images must have their dimension as a whole number multiple of the texture size. The only valid way to represent a 2D texture is with a single 2D image with the same size as the texture, plus optionally fallback images as defined below.

Note that, in addition to assembling textures from an images, an alternative is to use a procedural texture, such as a noise texture, or a texture generated from a shader. Such things may be defined in G4MF extensions, which would specify the noise algorithm or shader language to use. The G4MF base specification itself focuses on the base cases that are portable, widely supported, and will stand the test of time. Shaders may only work in some applications, and shading languages may evolve over time; the same applies to noise algorithms and other procedural texture techniques.

## Fallback Images For Textures

In addition to slicing and stacking images together, G4MF allows defining fallback images for textures. When reading images, each image is read in order, filling the requested size grid of pixels for the texture. If an image is not supported by the application, it is skipped, and the next image is read instead. As soon as the requested size grid of pixels is filled, no further images are read.

For example, a 3D texture with a size of `[64, 64, 64]` may be represented by 2 images: a WebP image with a size of 512x512 pixels, and a fallback JPEG image with a size of 512x512 pixels. When reading the texture, one of these three things happen depending on what the application supports:

- If the application supports WebP, it reads the WebP image, then slices and stacks it into a 64x64x64 grid of pixels. Since these pixels fill the entire texture, no further items are read from the `"images"` array.
- If the application does not support WebP, it skips the WebP image due to an unsupported format as indicated by the MIME type. Then it moves on to the next image, the JPEG image. If the application supports JPEG, it then uses its pixels to fill the 64x64x64 grid of pixels, which then fills the entire texture. Since these pixels fill the entire texture, no further items are read from the `"images"` array (there are none in this example, but still, a filled texture means no attempt is made to check for more images).
- If the application does not support WebP and does not support JPEG, it skips both images due to unsupported formats as indicated by the MIME types. Then it uses a default empty texture filled with the `"placeholder"` color on all pixels.

The same pattern happens for any number of images in the `"images"` array. For example, a 3D texture with a size of `[64, 64, 64]` may be represented by 1 OpenEXR image with a size of 4096x4096 pixels, 1 KTX2 image with a size of 64x64x64 pixels, 4 WebP images with a size of 256x256 pixels each, 64 PNG images with a size of 64x64 pixels each, and 8 JPEG images with a size of 256x128 pixels each. Applications read the images in order, grabbing the first pixels from the first supported images. In this example, this means that the OpenEXR image is given first priority if supported, then the KTX2 image, then the WebP images, then the PNG images, and finally the JPEG images.

This way of defining fallback images is clearer than when compared to glTF™. The base glTF™ specification supports PNG and JPEG images, and extensions may define additional image formats, using PNG or JPEG as a fallback. However, if multiple image format extensions are used, such as KTX2 and WebP on the same texture, the behavior of which image is the first choice and which is the fallback is not clearly defined. G4MF avoids this ambiguity by explicitly placing all images in order of priority.

## Texture Filtering

Each texture may optionally define a texture sampler, which defines how the texture is sampled when resized or read outside of its bounds. Samplers contain properties that define the filter modes used for magnification, minification, mipmaps, and the wrap mode of the texture on each axis.

Filtering controls the appearance of the texture when it is sampled indirectly, such as when it is scaled up or down, or applied to a mesh surface. In such cases, it may be the case that a given pixel on the screen corresponds to halfway between pixels on a texture, or any other fractional position. For uses of textures that do not involve sampling, the filter mode is not used.

The following filter modes are defined:

- `"linear"`: Each position sampled reads from the surrounding pixels multi-linearly interpolated. For example, within a single mipmap level, 2D textures use bilinear interpolation of the four nearest pixels, while 3D textures use trilinear interpolation of the eight nearest pixels.
  - When minifying or scaling down, if both `"minFilter"` and `"mipmapFilter"` are set to `"linear"`, this adds one dimension of interpolation, which means trilinear filtering in 2D textures and quadrilinear filtering in 3D textures.
- `"nearest"`: Each position sampled reads from the nearest neighbor texel. This results in a pixelated appearance when the texture is scaled up, useful for pixel art or retro-style graphics.
- `"none"`: Only available for `"mipmapFilter"`. Indicates that mipmaps are not used. This means that the texture will not be sampled using lower-resolution versions. This reduces memory usage, but can result in low performance or aliasing artifacts when the texture is scaled down.
- Extensions may define additional filter modes, using any string value.

For pixel art graphics, the `"magFilter"` property should be set to `"nearest"` to avoid blurring, while the others can be left at their defaults. Using `"nearest"` for magnification results in a pixelated appearance when the texture is scaled up, while using `"nearest"` for minification or mipmaps can result in Moiré patterns or aliasing artifacts when the texture is scaled down.

Applications SHOULD use anisotropic filtering when available, which is a technique that improves the quality of textures viewed at oblique angles. G4MF considers anisotropic filtering settings to be part of the application's graphical quality settings, not a part of the model data, and therefore does not define a property for it.

## Texture Sampler Properties

| Property         | Type       | Description                                            | Default      |
| ---------------- | ---------- | ------------------------------------------------------ | ------------ |
| **magFilter**    | `string`   | The filter mode used for magnification of the texture. | `"linear"`   |
| **minFilter**    | `string`   | The filter mode used for minification of the texture.  | `"linear"`   |
| **mipmapFilter** | `string`   | The filter mode used for mipmaps.                      | `"linear"`   |
| **wrap**         | `string[]` | The wrap mode of the texture on each axis.             | `["repeat"]` |

### Mag Filter

The `"magFilter"` property is a string-based enum that defines the filter mode of the texture when magnified. The default value is `"linear"`.

This property defines how the texture is sampled when zooming in on a texture or looking closely at a texture on a surface, resulting in the texture being larger on the screen than its original size. Valid values are `"linear"`, `"nearest"`, and any additional values defined by extensions. For pixel art graphics, this is the property that should be set to `"nearest"` to avoid blurring, while the other filter properties can be left at their defaults.

### Min Filter

The `"minFilter"` property is a string-based enum that defines the filter mode of the texture when minified. The default value is `"linear"`.

This property defines how the texture is sampled when zooming out on a texture or looking at a texture from a distance, resulting in the texture being smaller on the screen than its original size. Valid values are `"linear"`, `"nearest"`, and any additional values defined by extensions. The `"nearest"` value can result in aliasing artifacts, but is cheaper to calculate.

### Mipmap Filter

The `"mipmapFilter"` property is a string-based enum that defines the filter mode of the texture when mipmaps are used. The default value is `"linear"`.

This property defines how the texture is sampled when mipmaps are used, which are precomputed lower-resolution versions of the texture. This setting is used together with `"minFilter"` to determine the appearance during minification. Valid values are `"linear"`, `"nearest"`, `"none"`, and any additional values defined by extensions. The `"none"` value means that mipmaps are not used, which reduces memory usage but can result in low performance and aliasing artifacts when the texture is scaled down. If the `"mipmapFilter"` is set to a value other than `"none"`, mipmaps SHOULD be generated by the application on import, since mipmap data is not stored in G4MF files.

### Wrap

The `"wrap"` property is an array of strings that defines the wrap mode of the texture on each axis. The default value is `["repeat"]`.

This property defines how the texture is repeated when sampling outside of the texture bounds. The length of the array MUST either be 1 or equal to the number of dimensions in the texture. For example, a 3D texture may have `["repeat"]` or `["repeat", "repeat", "repeat"]`, but NOT `["repeat", "repeat"]` or `["repeat", "repeat", "repeat", "repeat"]`.

If only one wrap mode is specified, it applies to all axes. If multiple wrap modes are specified, they apply to each axis in the order of the texture's dimensions. For example, an equirectangular panorama skybox 3D texture for the sky of a 4D scene may have a wrap mode of `["repeat", "clamp", "repeat"]`, meaning that the texture repeats horizontally but is clamped vertically at the poles.

The following wrap modes are defined:

- `"clamp"`: Clamp the texture on its boundary. This means that sampling outside of the texture bounds will return the color at the nearest border position.
- `"mirror"`: Mirror the texture across boundaries. Each odd number of repetitions on an axis mirrors the texture on that axis. This means that a given normalized texture coordinate is "ping-ponged" across the texture bounds, so a texture coordinate of `1.25` is treated as `0.75`, a texture coordinate of `2.25` is treated as `0.25`, and a texture coordinate of `-0.25` is treated as `0.25`.
- `"repeat"`: Repeats the texture infinitely. This means that sampling outside of the texture bounds will repeat the texture in a tiled manner. This means that a given normalized texture coordinate is treated modulus 1, so a texture coordinate of `1.25` is treated as `0.25`, and a texture coordinate of `-0.25` is treated as `0.75`. This is the default wrap mode.
- Extensions may define additional wrap modes, using any string value.

## JSON Schema

- See [g4mf.texture.schema.json](../schema/g4mf.texture.schema.json) for the G4MF Texture properties JSON schema.
- See [g4mf.texture.sampler.schema.json](../schema/g4mf.texture.sampler.schema.json) for the G4MF Texture Sampler properties JSON schema.
- See [g4mf_file_ref.schema.json](../schema/g4mf_file_ref.schema.json) for the G4MF File Reference properties JSON schema.
