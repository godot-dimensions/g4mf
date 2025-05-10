# G4MF Shape

## Overview

A shape in G4MF is a pure geometric object defined by an enumerated type and a set of size parameters. Shapes are useful for things like physics calculations, but are not expected to be directly used for rendering.

The surface of a G4MF shape is usually a mathematical [implicit surface](https://en.wikipedia.org/wiki/Implicit_surface) meaning that its surface is defined by a mathematical function and it has an explicit inside and outside. G4MF shapes are usually manifolds, but this is not a requirement. One important exception is the concave mesh shape, whose surface is defined by the cells of a mesh, not a mathematical function. Concave mesh shapes often do not have a well-defined inside and outside, so are not implicit surfaces, and are often not manifolds. Also, lines and rays are not implicit surfaces, and lines, rays, and planes are not manifolds.

See "Common General Shapes" below for examples of how to define many common shapes in G4MF, including boxes, spheres, capsules, cylinders, and so on.

## Shape Properties

| Property    | Type       | Description                                                   | Default value       | Valid on shape types |
| ----------- | ---------- | ------------------------------------------------------------- | ------------------- | -------------------- |
| **curves**  | `object[]` | The curves of the shape, if any.                              | Empty array         | General              |
| **heights** | `integer`  | The index of the accessor storing the heightmap data, if any. | `-1` (no heightmap) | Heightmap            |
| **length**  | `number`   | The length of the ray shape in meters, if the shape is a ray. | `1.0`               | Ray                  |
| **mesh**    | `integer`  | The index of the mesh to use for a mesh-based shape.          | `-1` (no mesh)      | Concave, Convex      |
| **size**    | `number[]` | The base size of the shape in meters.                         | Zero vector         | General, Heightmap   |
| **type**    | `string`   | The type of the shape.                                        | `"general"`         | Always valid         |

### Curves

The `"curves"` property is an array of objects, each of which defines a curve on the shape. See "Curve Properties" below for the properties of each curve. The `"curves"` property is optional, and if omitted, the shape is assumed to have no curves.

### Heights

The `"heights"` property is an integer index of a G4MF accessor containing heightmap data. If not specified, the default value is `-1`, meaning the shape does not use a heightmap.

The heights property contains a multi-dimensional array of height values. The size of the array is defined by the `"size"` property of the shape, which MUST have its components set to integer values. The Y coordinate is not used for heightmap dimensions, but SHOULD be set to a reasonable value that allows a box shape to be generated as a crude fallback if an implementation does not support heightmaps. The heights property is required for heightmap shapes. If `"type"` is set to `"heightmap"`, the heights property MUST be set to a valid index of a G4MF accessor in the document-level `"accessors"` array.

For example, a heightmap shape with a size of `[5, 1, 5, 5]` defines a 5x5x5 3D grid of height values for a 4D heightmap, which means the accessor MUST have 125 values. The first value in the accessor is the height at the most-negative part of the grid, with the values first increasing in the X direction, then the Z direction, and finally the W direction. For other dimensions, resize the array to the appropriate length, for example `[5, 1, 5, 5, 5]` would be a 5x5x5x5 4D grid of height values for a 5D heightmap, which means the accessor MUST have 625 values.

By default, each height value is 1 meter apart from its non-height axis-aligned neighbors, which means the above example heightmap is 4x4x4 meters in size in the non-vertical axes. To change the density of the height values, the heightmap shape may be scaled by the scale of the G4MF node it is attached to. Note that this also scales the height values in the shape, so if a given height value is `5.0` meters, and the G4MF node has a global uniform scale of `0.5`, the final global height of that point is `2.5` meters in the local Y direction of the G4MF node's origin.

### Length

The `"length"` property is a number that defines the length of the ray shape in meters. If not specified, the default value is `1.0`, meaning the ray has a length of `1.0` meter. If defined, the length MUST be a positive number.

The length property is used to define the length of a ray shape. It is not used for other built-in shape types. The ray points in the local -Y direction from the local origin. If a ray is desired in a different location or direction, transform the G4MF node it is attached to.

### Mesh

The `"mesh"` property is an integer index of a G4MF mesh. If not specified, the default value is `-1`, meaning the shape does not use a mesh.

The mesh property is used to define the geometry of a concave mesh shape or a convex hull mesh shape. If `"type"` is set to `"concave"` or `"convex"`, the mesh property MUST be set to a valid index of a G4MF mesh in the document-level `"meshes"` array.

### Size

The `"size"` property is an array of numbers that defines the base size of the shape in meters. If defined, its length MUST match the dimension of the shape, which is the same as the dimension of the G4MF document. If not defined, the default value is a zero vector.

The size property is used to define the base size of general shapes, which includes boxes, spheres, capsules, cylinders, and so on. It is not used for mesh-based shapes or the plane shape. The numbers in the array MUST NOT be negative, only zero or finite positive numbers are allowed.

### Type

The `"type"` property is a string that defines the type of the shape. The default value is `"general"`, meaning the shape is a general shape with a size and optional curves.

The following shape types are defined in the base G4MF specification:

- `"general"`: A general shape with a size and optional curves. The center of the shape is at the origin of the local coordinate system.
- `"concave"`: A concave mesh shape, defined by a mesh. The mesh exists relative to the local coordinate system.
- `"convex"`: A convex hull mesh shape, defined by a mesh. The mesh exists relative to the local coordinate system.
- `"heightmap"`: A heightmap shape, defined by an array of height values, with the size property defining the dimensions of the data in the heights accessor.
- `"plane"`: A plane shape, defining an infinite boundary. The plane points up in the local +Y direction from the local origin.
- `"ray"`: A ray shape, defining a one-way line segment. The ray points in the local -Y direction from the local origin.

For all shape types, the center of the shape is at the origin of the local coordinate system, such as the G4MF node it is attached to, if any. To get a shape in a different location or orientation, transform the G4MF node it is attached to. The plane shape has no properties because all planes can be achieved by rotating or translating the G4MF node the plane is attached to.

For most shapes, scaling the G4MF node the shape is attached to is not recommended. Instead, scale the data in the shape itself, which will result in better compatibility with physics engines. However, for heightmap shapes, scaling the G4MF node is required to achieve different heightmap densities. Heightmaps SHOULD only be used for static objects, not moving objects. For all shapes, both the local and global transform of all G4MF nodes the shape is attached to MUST be conformal, meaning that their basis vectors are orthogonal and have the same length, and only position, rotation, and uniform scaling are allowed. If a shape is attached to a non-conformal G4MF node, the G4MF file is invalid and the behavior is undefined.

## Curve Properties

| Property     | Type       | Description                        | Default     |
| ------------ | ---------- | ---------------------------------- | ----------- |
| **radii**    | `number[]` | The radii of the curve in meters.  | Zero vector |
| **exponent** | `number`   | The exponent of the curve.         | `2.0`       |
| **taper**    | `object[]` | The tapering of the curve, if any. | Empty array |

### Radii

The `"radii"` property is an array of numbers that defines the radii of the curve in meters. The length of the array MUST match the dimension of the shape, which is the same as the dimension of the G4MF document. If not defined, the default value is a zero vector.

The radii property is used to define the radii of the curve in each axis. The numbers in the array MUST NOT be negative, only zero or finite positive numbers are allowed. If a curve is not on an axis, this is indicated by a zero value in the radii array on that axis. All curves SHOULD have at least two non-zero positive radius values, otherwise the curve is undefined, but different types of curves may be defined by an extension. Multiple entries in the `"curves"` array usually do not have overlapping axes, meaning that if one of the curves has a non-zero radius in an axis, no other curve should have a non-zero radius in that axis. If multiple curves have overlapping axes, the resulting shape is a Steinmetz solid, or multicylinder, which is not a common shape.

See the below examples for how to define many types of general shapes with curves and the `"radii"` property.

### Exponent

The `"exponent"` property is a number that defines the exponent of the curve. If not defined, the default value is `2.0`, meaning normal elliptical curves are used.

The exponent property defines a unitless value for the exponent of the curve. Values less than `2.0` create a shape pointier than circles in the axis-aligned directions. Values greater than `2.0` create a superellipse or squircle shape which is pointier than circles in the diagonal directions. See the uncommon general shape examples for more information.

### Taper

The `"taper"` property is an array of objects, each of which defines a position to taper, and properties for the taper at that position. If not defined, the default value is an empty array, meaning the curve does not have any tapering.

The allowed properties in a curve taper object are the same as the properties of a curve, but with the addition of a `"position"` property, and the lack of nested `"taper"` properties. As such, the `"radii"` and `"exponent"` properties are allowed on taper objects, and behave the same as on curves. G4MF extensions that apply to curve objects are automatically allowed on curve taper objects as well, however, extensions may also be defined for curve taper objects directly.

## Common General Shapes

Dimension-specific physics systems usually feature different shape types for boxes, spheres, capsules, cylinders, and so on. These have different combinations of sizes and curves, but the available combinations greatly expand when considering higher dimensions. To capture this concept for all dimensions at once, G4MF's default `"general"` shape type has a size and allows any number of curves to be defined in addition to the size. The arrays in the below examples can be used with any other dimension by resizing the arrays to the appropriate length.

A 4D box is defined by only a size property, with no curves:

```json
{
	"size": [1.0, 1.0, 1.0, 1.0]
}
```

A 4D sphere is defined by only a curve with the same radius in all axes, with the size property either omitted or all values set to zero:

```json
{
	"curves": [
		{
			"radii": [1.0, 1.0, 1.0, 1.0]
		}
	]
}
```

A 4D capsule, like a 3D capsule, can be thought of as a line segment and a radius. The size property defines the length of the line segment (the "mid height" of the capsule), and the curves property defines the radius of the capsule. In technical terms, each curve entry is applied as a Minkowski sum of an N‑ball over the base box. This example defines a 4D capsule with a "mid height" size of `1.0` meter and a radius of `0.5` meters, resulting in a "full height" of `2.0` meters:

```json
{
	"size": [0.0, 1.0, 0.0, 0.0],
	"curves": [
		{
			"radii": [0.5, 0.5, 0.5, 0.5]
		}
	]
}
```

A 4D cylinder, like a 3D cylinder, can be thought of as a line segment and a radius, but without any capping spheres, instead being flat in the vertical axis beyond the size. This is represented by the curve having the radius for that axis set to zero, indicating the curve does not apply in that axis. This example defines a 4D cylinder with a height of `2.0` meters and a radius of `0.5` meters in all axes except the vertical axis:

```json
{
	"size": [0.0, 2.0, 0.0, 0.0],
	"curves": [
		{
			"radii": [0.5, 0.0, 0.5, 0.5]
		}
	]
}
```

Exporters SHOULD prefer the "normal" vertical orientations of capsule and cylinder shapes, to better align with the typical way these are implemented. This allows the shapes to more easily be imported into other systems, such as a dedicated "capsule" type with a radius and height, or a "cylinder" type with a radius and height.

A 4D cubinder is an extruded version of a 3D cylinder, in a similar way to how a 3D cylinder is an extruded version of a 2D circle. It has two axes with a size, and a curve in the other two axes. For symmetry with 3D cylinders, the curve is usually in the XZ plane, with the sizes in the Y and W axes. This example defines a 4D cubinder with a height of `2.0` meters, a thickness of `1.0` meter, and a radius of `0.5` meters in the XZ plane:

```json
{
	"size": [0.0, 2.0, 0.0, 1.0],
	"curves": [
		{
			"radii": [0.5, 0.0, 0.5, 0.0]
		}
	]
}
```

A 4D duocylinder is a shape with no equivalent in 3D. It is the cartesian product of two circles, and can be thought of as a cylinder with two curves and two radiuses, but no "tall" part. This example defines a 4D duocylinder with a radius of `0.5` meters in the XY plane and a radius of `1.0` meter in the ZW plane:

```json
{
	"curves": [
		{
			"radii": [0.5, 0.5, 0.0, 0.0]
		},
		{
			"radii": [0.0, 0.0, 1.0, 1.0]
		}
	]
}
```

Multiple entries in the `"curves"` array usually do not have overlapping axes, meaning that if one of the curves has a non-zero radius in an axis, no other curve should have a non-zero radius in that axis.

## Uncommon General Shapes

The above describes examples of how to define common general shapes in G4MF. It is recommended that implementations support all of the above cases, and asset authors are recommended to use those simple common shapes for wider compatibility. However, this shape definition is highly flexible and can be used to define many advanced shapes in any dimension, which are optional for implementations to support.

A somewhat common shape is a tapered cylinder or tapered capsule. These have a radius that varies along the length of the shape. A cone shape has a tapering radius of zero at one end. To define this, another array inside of a curve may be specified, called `"taper"`. Each item in this array defines a new value for the radii at a specific point on the shape, which is usually on the range of plus or minus half the base `"size"`, but may be beyond it, which is useful for Steinmetz solids.

This example defines a cone that points straight up, with a height of `2.0` meters and a radius of `0.5` meters at the base. The radius outside of `"taper"` is provided as a fallback for implementations that do not support the `"taper"` property, and may be set to any value regardless of the `"taper"` values.

```json
{
	"size": [0.0, 2.0, 0.0, 0.0],
	"curves": [
		{
			"radii": [0.25, 0.0, 0.25, 0.25],
			"taper": [
				{
					"position": [0.0, 1.0, 0.0, 0.0],
					"radii": [0.0, 0.0, 0.0, 0.0]
				},
				{
					"position": [0.0, -1.0, 0.0, 0.0],
					"radii": [0.5, 0.0, 0.5, 0.5]
				}
			]
		}
	]
}
```

If a non-zero size and a curve exist on the same dimension, the curve is always added on top of the size, in the form of a Minkowski sum. This definition allows for a wide variety of shapes to be defined as a combination of size and curves. For example, a rounded or tapered box can be defined with a size and curve on all axes. The below example defines a 4D rounded box with a size of `1.0` meter and a radius of `0.25` meters on all axes, resulting in a maximum axis-aligned diameter of `1.5` meters in all axes.

```json
{
	"size": [1.0, 1.0, 1.0, 1.0],
	"curves": [
		{
			"radii": [0.25, 0.25, 0.25, 0.25]
		}
	]
}
```

On each curve, the `"radii"` array defines the radius of the curve in each axis. Usually, for circular curves, the radii are either zero or the same in all axes. However, it is possible to use different radius values in each axis to create an ellipse or ellipsoid. This is not recommended because functions like finding the surface area or perimeter have no closed form solution, but it is possible to specify the shape anyway. This example defines a 2D ellipse with an X radius of `1.0` meter and a Y radius of `0.5` meters (full width of `2.0` meters and full height of `1.0` meter):

```json
{
	"curves": [
		{
			"radii": [1.0, 0.5]
		}
	]
}
```

Usually, such as with circles, ellipses, spheres, hyperspheres, and so on, the curve follows a similar mathematical equation with an exponent of `2.0`, meaning the curve behaves with a constant Euclidean distance (after rescaling by the different radius values, if not all radii are the same). However, in rare cases, other exponent values may be desired. The `"exponent"` property may be defined on a curve to specify the unitless exponent value to use for that curve.

Values less than `2.0` create a shape pointier than circles in the axis-aligned directions. This example defines a 2D orthoplex or "diamond" shape with a radius of `1.0` meter:

```json
{
	"curves": [
		{
			"radii": [1.0, 1.0],
			"exponent": 1.0
		}
	]
}
```

Values greater than `2.0` create a superellipse or squircle shape which is pointier than circles in the diagonal directions. This example defines a 2D quartic squircle with a radius of `1.0` meter:

```json
{
	"curves": [
		{
			"radii": [1.0, 1.0],
			"exponent": 4.0
		}
	]
}
```

Multiple entries in the `"curves"` array usually SHOULD NOT have overlapping axes. If multiple curves have overlapping axes, the resulting shape is a [Steinmetz solid](https://en.wikipedia.org/wiki/Steinmetz_solid), or multicylinder. This example defines a byclinder on the XY and XZ planes with a radius of `1.0` meter extruded into 4 dimensions along the W axis by `2.0` meters:

```json
{
	"size": [0.0, 0.0, 0.0, 2.0],
	"curves": [
		{
			"radii": [1.0, 1.0, 0.0, 0.0]
		},
		{
			"radii": [1.0, 0.0, 1.0, 0.0]
		}
	]
}
```

These shapes are not generally expected to be supported by physics engines, but show the flexibility of the G4MF general shape type.

Even more advanced curves can be created by extending the items in the `"curves"` array with a G4MF extension.

## JSON Schema

See these files for the JSON schema of the shape properties:

- Shape: [g4mf.shape.schema.json](../../schema/physics/g4mf.shape.schema.json)
- Shape Curve: [g4mf.shape.curve.schema.json](../../schema/physics/g4mf.shape.curve.schema.json)
- Shape Curve Taper: [g4mf.shape.curve.taper.schema.json](../../schema/physics/g4mf.shape.curve.taper.schema.json)

## References

- Wikipedia Implicit Surface: https://en.wikipedia.org/wiki/Implicit_surface
- Wikipedia Steinmetz Solid: https://en.wikipedia.org/wiki/Steinmetz_solid
