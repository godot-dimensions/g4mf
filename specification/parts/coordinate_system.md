# G4MF Coordinate System

## Overview

Generally speaking, G4MF defines a coordinate system that is a superset of the right-handed 3D coordinate system found in OpenGL™, glTF™, and other 3D software and formats. This part of the G4MF specification describes the coordinate system in detail, including the axis labels, units, and direction and side conventions for nodes and objects.

Some of this information is not relevant for all applications. A 4D application can ignore all 5D and beyond information. An application that does not display axis labels or direction names can ignore any or all such information. If an application has the concepts described here, it SHOULD follow the conventions described here, and SHOULD NOT deviate from them. Applications MAY convert the coordinate system to a different one on import or export as needed, under the assumption that existing G4MF files follow these conventions, and generated G4MF files are made to follow the conventions described here.

## Labels and Dimensions

G4MF is a multi-dimensional format which can be used for any number of dimensions. While it is possible to think of the data as abstract N-dimensional data, most common use cases require explicitly defining how these numbers map to dimensions on the user's computer screen.

Dimensions in G4MF can be referred to by index, or by convention, they can be labeled with capital letters. By convention, the first four dimensions are X, Y, Z, and W, which correspond to zero-based indices 0, 1, 2, and 3 respectively. If letter labels are used for additional dimensions, follow the alphabet in reverse from W, so V, U, T, S, etc. Labels beyond index 25 (the "A axis") are not defined by G4MF, but may be extended by applications, such as [by using additional alphabets](https://github.com/godot-dimensions/godot-nd/blob/3ff3e2dc7766c768997780fad1285ab0f1ffc254/math/vector_nd.cpp#L55).

G4MF defines the following coordinate system, relative to an unrotated camera projecting to a real-world 2D screen:

- The axis at index 0, the "X axis", points to the right on the 2D screen.
- The axis at index 1, the "Y axis", points up on the 2D screen.
- The axis at index 2, the "Z axis", points out of the 2D screen towards the viewer, and is used for depth.
- The axis at index 3, the "W axis", is perpendicular to the first three axes.
  - The W axis does not change the projected position on the 2D screen unless the object or camera is rotated in the additional dimensions.
  - The same applies to any other additional dimensions at index 4 (the "V axis"), index 5 (the "U axis"), etc.
- This defines a coordinate system that is a superset of the right-handed 3D coordinate system found in OpenGL™, glTF™, and other 3D software and formats.

See also [G4MF Math](math.md) for information on how to perform calculations with vectors in this coordinate system.

## Direction and Side Conventions

Directed node types point in the -Z direction. Spot lights and directional lights emit light in the -Z direction, cameras look in the -Z direction, and conical audio emitters emit audio in the -Z direction. Therefore, **the -Z direction is the "forward" direction**, +Z is the "back" direction, +X is the right direction, -X is the left direction, +Y is the up direction, and -Y is the down direction. Note the usage of the word "direction" here, in contrast to "side" below.

Objects with sides have their front side in the +Z direction. For example, characters face the +Z direction, vehicles have their front in the +Z direction, and other meshes are oriented so that their front is in the +Z direction. Therefore, **the +Z side is the "front" side**, -Z is the "rear" side, +X is the left side, -X is the right side, +Y is the top side, and -Y is the bottom side. Note the usage of the word "side" here, in contrast to "direction" above.

The above two paragraphs mean that cameras and lights face towards the front of characters and other objects by default, illuminating and viewing their fronts. This is the standard convention in most 3D software, and is [codified in glTF™ as part of the glTF™ 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#coordinate-system-and-units), therefore G4MF follows the same convention. For more information, read [Godot's documentation on 3D asset directions](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html#d-asset-direction-conventions).

The above paragraphs only apply for G4MF files of dimension 3 or greater, with 0D, 1D, or 2D G4MF files using different conventions. Generally, for 1D and 2D, replace +Z with +X, and replace -Z with -X. For 1D or 2D G4MF files, cameras are typically screen-aligned and don't point in any direction, but if directed cameras are needed, they look in the -X direction. For 1D or 2D G4MF files, directed objects have their front on the +X axis. For 2D G4MF files, spot and directional lights emit light in the -Y direction (down). Note that many 2D game engines have +Y as down, therefore this maps to +Y in those engines. For 1D G4MF files, spot and directional lights emit light in the -X direction.

For assets without an intrinsic front side or forward direction, such as a game map or terrain, take note of the cardinal directions instead. For G4MF files of dimension 3 or greater, the +X axis is east, the -X axis is west, the +Z axis is south, and the -Z axis is north. For G4MF files of dimension 2, north and south are often not meaningful concepts, since the Y axis is often up and down, but if the G4MF represents a "top-down" view, then +Y is north and -Y is south. Note that many 2D game engines have +Y as down, therefore this maps to +Y as south and -Y as north in those engines.

For G4MF files of dimension 4 or greater, additional names can be assigned to the additional axes. For directed node types such as cameras, +W is ana, -W is kata, +V is sursum, and -V is deorsum. For directed objects such as characters, append the word "side" to each: +W is the ana side, -W is the kata side, +V is the sursum side, and -V is the deorsum side. For cardinal directions, +W is anth, -W is kenth, +V is surth, and -V is deorth. When abbreviating these on a compass, use the first letter of each word, but use the dollar sign "$" for sursum to avoid confusion with south: N S E W A K $ D. This is the same convention used by [4D Golf](https://store.steampowered.com/app/2147950/4D_Golf/). Names for 6D and beyond are not defined by G4MF. Consider instead using labels like +X, -X, +Z, +W, and so on, which are more extensible and avoid confusion, but require two characters instead of one.

## Units

All units are [SI](https://en.wikipedia.org/wiki/International_System_of_Units) metric units whenever possible:

- All length is in meters.
- All time is in seconds.
- All mass is in kilograms.
- All angles are in radians.
- All lights are in lumen-based units.
- All derived units are based on these, such as velocity in meters per second, or power in watts.
- All solid angles use radian-based units, such as steradians for 3D cones, choradians for 4D cones, etc.

The use of SI metric units is mandatory in all G4MF files whenever possible, to ensure interoperability and consistency. If a G4MF file does not use SI metric units, the file is invalid. G4MF extensions MUST NOT change the base units of a G4MF file, and any additional units defined by extensions MUST be derived from SI metric units when possible. For example, an extension redefining length in feet or centimeters is invalid; such an extension MUST NOT be created and MUST NOT be implemented. Extensions may define completely new units ONLY if those units cannot be derived from SI metric units. For example, a G4MF file of a pepper and an extension describing its spiciness may define Scoville Heat Units (SHU) as a new unit.

## Colors

Colors are defined by red, green, blue, and an optional alpha channel. Each channel is a floating-point number on the range of 0.0 to 1.0, inclusive, where [0.0, 0.0, 0.0, 1.0] represents opaque black, and [1.0, 1.0, 1.0, 1.0] represents opaque white. Colors MUST use floating-point values instead of integers to ensure a consistent 0.0 to 1.0 range and to allow for increased precision near zero. Overbright colors MAY be allowed on some properties but SHOULD generally be avoided. The alpha channel is optional and defaults to 1.0 (fully opaque) if omitted.

The color space of G4MF colors is linear, with gamut, primaries, and white point exactly matching both the sRGB and the ITU Rec. 709 standard color spaces. All colors MUST be defined in linear color space and SHOULD use this gamut. If a different gamut beyond sRGB is required, it MAY be defined by an extension and used by color properties in extensions.
