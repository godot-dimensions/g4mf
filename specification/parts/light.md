# G4MF Light

## Overview

G4MF allows for defining lights in the scene using the `"lights"` array to define light properties, and referencing them by index in the `"light"` property of a node. Each light object in the array is one of the `"directional"`, `"point"`, or `"spot"` types, and may have further properties depending on the light type, specifically `"range"` for point and spot lights, and `"coneInnerAngle"` and `"coneOuterAngle"` for spot lights. All lights have a `"color"` and an `"intensity"` property, with the intensity unit changing depending on the type of light. Additional light types may be defined by extensions by extending the base light object.

Implementations may choose to ignore lights if they are not supported or not desired. Instead, implementations may use unshaded rendering, angle-dependent shading, lighting from the environment, lights provided by the engine or application, or any other method of rendering the model.

## Example

This example defines a red spot light with a range of 10 meters used on a node. The intensity and cone angle properties are not defined, meaning that it uses the default intensity and the default cone angles.

```json
{
	"lights": [
		{
			"type": "spot",
			"color": [1.0, 0.0, 0.0],
			"range": 10.0
		}
	],
	"nodes": [
		{
			"name": "MySpotLight",
			"light": 0,
		}
	]
}
```

## Light Properties

| Property           | Type        | Description                                                            | Default              |
| ------------------ | ----------- | ---------------------------------------------------------------------- | -------------------- |
| **type**           | `string`    | The type of light, as a string-based enum.                             | `"point"`            |
| **color**          | `number[3]` | The RGB color value for the light, usually on the range 0.0 to 1.0.    | `[1.0, 1.0, 1.0]`    |
| **coneInnerAngle** | `number`    | The inner angle radius of the light cone in radians.                   | `0.0`                |
| **coneOuterAngle** | `number`    | The outer angle radius of the light cone in radians.                   | `0.7853981633974483` |
| **intensity**      | `number`    | The intensity of the light, in lumens per radial unit or surface unit. | `1000.0`             |
| **range**          | `number`    | The range of the light in meters.                                      | Infinity             |

### Type

The `"type"` property is a string-based enum that defines the type of light. The following types are defined in the base specification:

- `"directional"`: A directional light is like sunlight, it emits light in the node's local -Z direction.
- `"point"`: A point light emits light in all directions from a single point in space, the node's local origin.
- `"spot"`: A spot light emits light in a cone shape from a single point in space, the node's local origin, in the node's local -Z direction.

Additional light types may be defined by extensions by extending the base light object. If not specified, the default is `"point"`.

### Color

The `"color"` property is an array of three numbers that defines the RGB color value for the light. If not specified, the default is plain white `[1.0, 1.0, 1.0]`.

The color is defined in linear color space. The color is represented as an array of exactly three numbers, each usually in the range 0.0 to 1.0, except for overbright colors. Prefer using the range 0.0 to 1.0 for colors, and increasing the `"intensity"` instead, when increased brightness is needed. The final light emitted is the product of the color and the intensity.

### Cone Inner Angle

The `"coneInnerAngle"` property is a number that defines the inner angle radius of the light cone in radians. If not specified, the default is `0.0`.

This property is only used for spot lights. Inside the cone inner angle, the intensity of the light is maximal. Between the cone inner angle and the cone outer angle, the intensity of the light is interpolated.

### Cone Outer Angle

The `"coneOuterAngle"` property is a number that defines the outer angle radius of the light cone in radians. If not specified, the default is `0.7853981633974483` radians (45 degrees).

This property is only used for spot lights. Beyond the cone outer angle, the intensity of the light is zero. Between the cone inner angle and the cone outer angle, the intensity of the light is interpolated.

TODO: Currently, the cone angles use the angular radius like Godot and glTF™, but the Web Audio API uses the angular diameter. These are not consistent with each other, so we can't be consistent with all of them either way. It's still up for debate if we should switch to the angular diameter, or if we should keep the angular radius. Which is more useful, which is more common?

### Intensity

The `"intensity"` property is a number that defines the intensity of the light. If not specified, the default is `1000.0`.

The intensity unit depends on the type of light. Point and spot lights use lumens per radial unit (radian for 2D models, steradian for 3D models, choradian for 4D models, etc), while directional lights use lumens per surface unit (meter for 2D models, square meter for 3D models, cubic meter for 4D models, etc). The final light emitted is the product of the color and the intensity.

The intensity MUST scale up with the uniform scale of the node the light is attached to, in order to ensure that a scaled model keeps the same light intensity relative to itself. For a 3D model, a uniform scale of 2.0 should scale up the intensity by 4.0. For a 4D model, a uniform scale of 2.0 should scale up the intensity by 8.0.

### Range

The `"range"` property is a number that defines the range of the light in meters. If not specified, the default is `Infinity`.

The range is only used for point and spot lights. The range defines the distance from the light source beyond which the light intensity is zero. The range MUST scale up with the uniform scale of the node the light is attached to, in order to ensure that a scaled model keeps the same light range relative to itself. For a uniform scale of 2.0, the range should be scaled up by 2.0.

## JSON Schema

See [g4mf.light.schema.json](../schema/g4mf.light.schema.json) for the G4MF Light properties JSON schema.
