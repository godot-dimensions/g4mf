# G4MF Physics Motion

If a node has a `"physics"` property with the `"motion"` property defined, its transform is driven by the physics engine.

- Descendant nodes should move with that node. The physics engine should treat them as part of a single body.
- If a descendant node has its own motion property, that node should be treated as an independent body during simulation. There is no implicit requirement that a node with `"motion"` follows an ancestor in the tree with `"motion"`.
- If a node's transform is animated by animations in the file, those animations should take priority over the physics simulation.

## Example

This example defines a single G4MF node with a `"motion"` property defining `"dynamic"` motion with a mass of `5.0` kilograms.

```json
{
	"name": "MyDynamicNode",
	"physics": {
		"motion": {
			"type": "dynamic",
			"mass": 5.0
		}
	}
}
```

## Motion Properties

|                        | Type       | Description                                                                     | Default value        |
| ---------------------- | ---------- | ------------------------------------------------------------------------------- | -------------------- |
| **type**               | `string`   | The type of the physics body as a string.                                       | Required, no default |
| **mass**               | `number`   | The mass of the physics body in kilograms.                                      | `1.0`                |
| **inertiaDiagonal**    | `number[]` | The inertia in the principle rotation planes in kilogram meter squared (kg⋅m²). | Zero bivector        |
| **inertiaOrientation** | `number[]` | The inertia orientation as a rotor.                                             | Identity rotor       |
| **linearVelocity**     | `number[]` | The initial linear velocity of the body in meters per second.                   | Zero vector          |
| **angularVelocity**    | `number[]` | The initial angular velocity of the body in radians per second.                 | Zero bivector        |
| **gravityFactor**      | `number`   | A multiplier applied to the acceleration due to gravity.                        | `1.0`                |

### Motion Types

The `"type"` property is a lowercase string that defines what type of physics body this is. Different types of physics bodies have different interactions with physics systems and other bodies within a scene. This property is required.

The motion type may be one of these three values: `"static"`, `"kinematic"`, or `"dynamic"`.

#### Static

Static bodies can be collided with, but do not have simulated movement. They are usually used for level geometry. Specifying a static body is optional, as nodes with collider properties are assumed to be static without itself or an ancestor node having the motion property.

#### Kinematic

Kinematic bodies can be collided with, and can be moved using scripts or animations. They can be used for moving platforms and characters.

#### Dynamic

Dynamic bodies are bodies simulated with [rigid body dynamics](https://en.wikipedia.org/wiki/Rigid_body_dynamics). They collide with other bodies, and move around on their own in the physics simulation. They are affected by gravity. They can be used for props, vehicles, or other dynamic objects that move around in the world.

### Mass

The `"mass"` property is a number that defines how much mass this physics body has in kilograms. If not specified, the default value is 1 kilogram.

Not all body types can make use of mass, such as triggers or non-moving bodies, in which case the mass can be ignored. The center of mass is defined as the local space origin of the body. Calculations like torque and rotational inertia are done relative to the center of mass at the body's local space origin.

### Inertia Diagonal

The `"inertiaDiagonal"` property is an array of numbers that defines the inertia in the principle rotation planes in kilogram meter squared (kg⋅m²). If zero or not specified, the inertia should be automatically calculated by the physics engine.

This value is a bivector, meaning that in 4D, it has 6 numbers for the XY, XZ, YZ, XW, YW, and ZW rotation planes, in that order (dimensionally-increasing order). Only the "dynamic" motion type can make use of inertia.

### Inertia Orientation

The `"inertiaOrientation"` property is an array of numbers that defines a rotor for the orientation of the inertia's principle axes relative to the body's local space. If not specified or set to the default value of the identity rotor, the inertia's principle axes are aligned with the body's local space axes.

### Linear Velocity

The `"linearVelocity"` property is an array of numbers that defines how much linear velocity this physics body starts with in meters per second. If not specified, the default value is zero.

Not all body types can make use of linear velocity, such as non-moving bodies, in which case the linear velocity can be ignored.

### Angular Velocity

The `"angularVelocity"` property is an array of numbers that defines how much angular velocity this physics body starts with in radians per second. If not specified, the default value is zero.

This value is a bivector, meaning that in 4D, it has 6 numbers for the XY, XZ, YZ, XW, YW, and ZW rotation planes, in that order (dimensionally-increasing order). Not all body types can make use of angular velocity, such as non-moving bodies, in which case the angular velocity can be ignored.

### Gravity Factor

The `"gravityFactor"` property is a number that defines a multiplier applied to the acceleration due to gravity. Values other than 1.0 are not realistic, but may be useful for artistic effects. If not specified, the default value is 1.0.

## JSON Schema

See [g4mf.node.physics.motion.schema.json](../../schema/physics/g4mf.node.physics.motion.schema.json) for the motion properties JSON schema.
