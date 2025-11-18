# G4MF Node Physics

## Overview

G4MF node physics defines the physical properties of objects in the scene. It allows using shapes to define solid colliders or non-solid triggers, and allows defining the motion properties of objects, including mass, inertia, and more. Physics properties are not needed for loading the mesh geometry of the scene, and may be ignored if the file is only used for visual purposes, or if loading into an application that does not support physics and only needs the mesh geometry.

## Physics Properties

G4MF node physics properties are defined in the `"physics"` property of a node, which is an object containing the following properties:

| Property     | Type     | Description                                                            | Default      |
| ------------ | -------- | ---------------------------------------------------------------------- | ------------ |
| **motion**   | `object` | If present, this node has its motion controlled by physics.            | No motion.   |
| **collider** | `object` | If present, this node has a solid shape that can be collided with.     | No collider. |
| **trigger**  | `object` | If present, this node has a non-solid shape that can act as a trigger. | No trigger.  |

Each of these properties MUST be defined on separate nodes. This results in a very clear, simple, and portable document structure, and ensures that each behavior has its own transform.

#### Motion

If a node has the `"motion"` property defined, its transform is driven by the physics engine.

For convenience, the details of how physics work are described in a separate file: [G4MF Physics Motion](motion.md).

#### Collider

If a node has the `"collider"` property defined, it is a solid collider node that objects can collide with.

Colliders contain a `"shape"` property, which is the index of a shape in the G4MF file's document-level shapes array. See [G4MF Shape](shape.md) for more details on the shape types.

#### Trigger

If a node has the `"trigger"` property defined, it is a non-solid trigger that can detect when objects enter it. Triggers are also known as sensors, areas, probes, overlap volumes, detection volumes, or other names in different physics engines. Triggers may be used to trigger events, such as running a function when an object enters or exits the volume.

Triggers contain a `"shape"` property, which is the index of a shape in the G4MF file's document-level shapes array. See [G4MF Shape](shape.md) for more details on the shape types.

## JSON Schema

See [g4mf.node.physics.schema.json](../../schema/physics/g4mf.node.physics.schema.json) for the physics properties JSON schema.
