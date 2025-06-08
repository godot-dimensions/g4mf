# G4MF Camera

## Overview

G4MF uses cameras to define the view of the scene. A node may be defined as a camera by setting the `"camera"` property to an object containing the camera properties defined in this file. Cameras are optional to include in a G4MF file. If not defined, any objects in the G4MF file are meant to be rendered with an external camera.

## Example

This example defines a single G4MF node with a camera. This example defines no camera properties, so the camera has all default values.

```json
{
	"name": "MyCamera",
	"position": [0.5, 1.0, 0.5, 0.5],
	"camera": {}
}
```

Additionally, here is a G4MF node with a camera where all properties are set to a value. The properties do not need to be specified if they are equal to the default value. The size property is unused because this is a perspective camera.

```json
{
	"name": "MyCamera",
	"position": [0.5, 1.0, 0.5, 0.5],
	"camera": {
		"clipFar": 4000.0,
		"clipNear": 0.05,
		"fov": 1.5707963267948966,
		"keepAspect": 1,
		"size": 1.0,
		"type": "perspective"
	},
}
```

## Properties

| Property       | Type      | Description                                                          | Default                 |
| -------------- | --------- | -------------------------------------------------------------------- | ----------------------- |
| **clipFar**    | `number`  | The distance to the far clipping plane.                              | No far clipping plane.  |
| **clipNear**   | `number`  | The distance to the near clipping plane.                             | No near clipping plane. |
| **fov**        | `number`  | The field of view of the camera in degrees.                          | `1.5707963267948966`    |
| **keepAspect** | `integer` | The screen space dimension index that `"fov"` and `"size"` refer to. | `1`                     |
| **size**       | `number`  | The size in meters of the camera.                                    | `1.0`                   |
| **type**       | `string`  | The type of camera projection.                                       | `perspective`           |

### Clip Far

The `"clipFar"` property is a number that defines the distance to the far clipping plane in meters. If not defined, the camera does not have an explicitly defined far clipping plane.

The far clipping plane is the distance from the camera to the farthest point that will be rendered. If defined, it MUST be a finite number greater than `"clipNear"`. When defined for perspective cameras, this must be positive. When defined for orthographic cameras, it is usually positive, but may be positive, negative, or zero. Implementations may treat the lack of a far clipping plane as infinite, or as a very large number determined by the implementation.

### Clip Near

The `"clipNear"` property is a number that defines the distance to the near clipping plane in meters. If not defined, the camera does not have an explicitly defined near clipping plane.

The near clipping plane is the distance from the camera to the closest point that will be rendered. If defined, it MUST be a finite number less than `"clipFar"`. When defined for perspective cameras, this must be positive. Implementations may treat the lack of a near clipping plane on a perspective camera as a value very close to zero. When defined for orthographic cameras, it may be positive, negative, or zero. Implementations may treat the lack of a near clipping plane on an orthographic camera as a very large negative number, or as negative infinity.

### FOV

The `"fov"` property is a number that defines the field of view of the camera in radians. If not defined, the default is `1.5707963267948966` radians (90 degrees).

This property is only used for perspective cameras, and has no effect on orthographic cameras. The field of view is the angle in radians that the camera can see. If defined, it MUST be greater than 0 and no more than 3.1415925 radians (180 degrees), which is the maximum value less than `tau/2` that can be represented in a 32-bit single-precision floating point number. By default, this number refers to the vertical field of view, but it may refer to other dimensions depending on the `"keepAspect"` property.

### Keep Aspect

The `"keepAspect"` property is an integer that defines what `"fov"` and `"size"` refer to. If not defined, the default is `1`, referring to the screen height.

The value is the screen space dimension index that the `"fov"` and `"size"` correspond to. `0` refers to the screen width, `1` refers to the screen height, `2` or more refer to additional dimensions. For cameras intending to render to a real world 2D screen, this should be set to `0` or `1`. Other values are intended for use cases like rendering 4D scenes to a virtual 3D screen inside a 4D scene. The FOV and size of the other directions are calculated depending on the aspect ratio of the target screen or viewport the camera is rendering to.

### Size

The `"size"` property is a number that defines the size of the camera in meters. If not defined, the default is `1.0`, or one meter.

This property is only used for orthographic cameras, and has no effect on perspective cameras. The value is measured in meters, and MUST be greater than `0.0`. By default, this number refers to the vertical size, but it may refer to other dimensions depending on the `"keepAspect"` property.

### Type

The `"type"` property is a string that defines the projection type of the camera. If not defined, the default is `"perspective"`.

If the type is `"orthographic"`, the `"size"` property is used but the `"fov"` property is ignored, and the `"clipNear"` value is allowed to be zero or negative. If the type is `"perspective"`, the `"fov"` property is used but the `"size"` property is ignored, and the `"clipNear"` value MUST be positive. Both types of cameras use the `"clipFar"` and `"keepAspect"` properties in the same way.

The type property MUST be either `"orthographic"` or `"perspective"`. If other camera types are needed, such as sheared frustum cameras, oblique clipping plane cameras, fisheye cameras, and so on, they may be defined in extensions, keeping this property as a fallback.

## Using Focal Length

The `"fov"` property is the field of view in radians. In some use cases, using a focal length is more convenient.

The `"fov"` property may be converted to and from focal length using the following formulas:

$$
\mathrm{focalLength}
= \tan\Bigl(\frac{\pi - \mathrm{fov}}{2}\Bigr)
$$

$$
\mathrm{fov}
= \pi - 2\arctan\bigl(\mathrm{focalLength}\bigr)
$$

These formulas assume the sensor size is of unit length and has the same unit of measurement as the focal length. For example, with a sensor size of 1 meter, a focal length of 1 meter would give a field of view of 90 degrees. If you need a different sensor size, you may rescale the focal length as needed. Also, the trigonometric functions in these formulas use radians.

## JSON Schema

See [g4mf.node.camera.schema.json](../schema/g4mf.node.camera.schema.json) for the camera properties JSON schema.
