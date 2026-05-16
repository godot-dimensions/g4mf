# G4MF Node

## Overview

Nodes are the core building block of a G4MF file. Each node defines an object in the scene with a transform, defines child nodes that are attached to it, and have other data attached to them to define the type of object they represent.

Each node defines a transform, which is a combination of a position, and a basis or rotor+scale. The details of the transform properties are defined in a separate file, [G4MF Transform](transform.md), and has its own schema. Transforms are separated from nodes to allow the transform properties to be reused without having to redefine them in multiple places.

The node at index 0 is the root node. All other nodes in the file are either descendants of the root node, or are not used. Nodes not used in the core scene hierarchy MAY be used by extensions. G4MF files may also contain zero nodes, in which case the file is not a scene, but a collection of data, such as a 4D mesh. The root node at index 0 MUST NOT have any transform properties defined, since it represents the origin of the file itself.

Node names MUST be file-unique, MUST NOT include `"`, `.`, `:`, `@`, `{`, `}`, `[`, `]`, `/`, and literal `\` characters, and MUST follow all of the requirements for G4MF item names as defined in [G4MF Core](core.md#name). Node names are RECOMMENDED to be PascalCase, however any compliant name is allowed.

G4MF nodes may be empty nodes, or at most "one thing". For example, a single node MUST NOT be both a camera and a mesh instance at the same time.

## Example

The following example defines a 4-dimensional G4MF file with a root node at index 0 and a child node at index 1 with a position of (1, 2, 3, 4).

```json
{
	"asset": {
		"dimension": 4
	},
	"nodes": [
		{
			"children": [1],
			"name": "RootNode"
		},
		{
			"name": "ChildNode",
			"position": [1, 2, 3, 4]
		}
	]
}
```

## Properties

Note that this table does not include properties defined in [G4MF Transform](transform.md) and [G4MF Item](core.md#items).

| Property          | Type        | Description                                                | Default                   |
| ----------------- | ----------- | ---------------------------------------------------------- | ------------------------- |
| **children**      | `integer[]` | The indices of the child nodes of this node.               | `[]` (empty array)        |
| **visible**       | `boolean`   | Whether the node is visible or not (affects rendering).    | `true`                    |
| **bone**          | `object`    | If this node is a skeleton bone, the bone properties.      | `undefined` (no bone)     |
| **camera**        | `object`    | If this node is a camera, the camera properties.           | `undefined` (no camera)   |
| **light**         | `object`    | If this node is a light, the light properties.             | `undefined` (no light)    |
| **meshInstance**  | `object`    | If this node is a mesh instance, the mesh properties.      | `undefined` (no mesh)     |
| **modelInstance** | `object`    | If this node is a model instance, the model properties.    | `undefined` (no model)    |
| **physics**       | `object`    | If this node is a physics object, the physics properties.  | `undefined` (no physics)  |
| **skeleton**      | `object`    | If this node is a skeleton root, the skeleton properties.  | `undefined` (no skeleton) |

### Children

The `"children"` property is an array of integers that defines the indices of the child nodes of this node. If not specified, the default value is an empty array, meaning the node has no children.

The indices in the array MUST be valid indices in the G4MF file's document-level `"nodes"` array. The order of the indices in the array is significant, as it affects the order of the nodes in the scene tree. A node may only be a child at most once, meaning that each node may only have at most one parent. The node at index 0 is the root node, it has no parent in the G4MF file, and no other node may use it as a child.

### Visible

The `"visible"` property is a boolean value that defines whether the node is visible or not. If not specified, the default value is `true`, meaning the node is visible. If set to `false`, the node is not rendered in the scene.

The visibility of a node in a tree is determined by its own visibility and the visibility of all its ancestors. If a node is has `"visible"` set to false, it and all its descendants are not visible in the tree. If a node is visible in the tree, that may only occur when it and all its ancestors are visible.

The `"visible"` property is not a generic way to disable nodes in the scene. It only defines the ability of a node and its descendants to be rendered. Physics objects, such as bodies and collision shapes, are not affected by the visibility of a node.

### Component Properties

G4MF nodes exist in the tree and have a transform, but in order for that tree of nodes to be useful, some nodes must have additional properties defined. These properties define the type of object the node represents, such as a bone, camera, light, mesh, model, or physics object. For lack of a better term, these are referred to as "component properties".

Each node may only represent at most "one thing", allowing it to be imported as a single object of a single class. The `"bone"`, `"camera"`, `"light"`, `"meshInstance"`, `"modelInstance"`, `"physics"`, and `"skeleton"` component properties are all mutually exclusive, meaning that a node MUST NOT have more than one of these properties defined at the same time. This means that a single G4MF node cannot be both a light and a mesh, or both a bone and a camera, instead multiple G4MF nodes are required to represent such scenarios. This requirement greatly simplifies the implementation of G4MF importers, and ensures that each conceptual part has its own transform on its own node in the tree.

Note for extension authors: Properties defined by extensions SHOULD follow the same principle, such that they only combine properties where it makes sense as "one thing". For example, a vehicle body class should extend a dynamic physics body class, meaning that the resulting class has properties of both. Therefore, a vehicle body extension data should be defined within the physics motion properties. Each of these properties is a JSON object, allowing extension data specific to those components to be defined within them, ensuring that the extension data is only present when the appropriate component is present. For another example, an audio emitter class does not extend any of these, so it must not be defined on the same G4MF node as a bone, camera, light, mesh, model, or physics object.

Note for asset authors: A G4MF node with physics motion properties is referred to as a "physics body" for short. To add a mesh to a physics body, the node mesh property MUST be defined on a separate node, which is then used as a child of the physics body node. Similarly, other types may be used together on separate nodes. Asset authors SHOULD prefer the top node of such a subtree to be the physics body, and then have other nodes as children of it, to ensure the component nodes follow the physics body when it moves. For skeletons, each bone MUST be a child of another bone or of the skeleton itself, meaning that to attach a light or other component to a bone, such a node must be added as a child of the bone. For subtrees without physics motion or skeletons, asset authors SHOULD prefer types _other than mesh or model_ as the top node. Mesh nodes are often leaf nodes, which simplifies some use cases of mesh nodes. This is not a requirement, but a recommendation to improve consistency when importing G4MF files into different applications with different requirements on tree structure.

#### Bone

The `"bone"` property is an object that defines the bone properties for this node. If not specified, the default value is `undefined`, meaning the node is not a bone.

The `"bone"` property MUST NOT be used together with the `"camera"`, `"light"`, `"meshInstance"`, `"modelInstance"`, `"physics"`, or `"skeleton"` properties on the same node.

See [G4MF Skeleton Skinned Mesh Deformation](mesh/skeleton.md) for more information about skeleton bones and skinned meshes.

#### Camera

The `"camera"` property is an object that defines the camera properties for this node. If not specified, the default value is `undefined`, meaning the node is not a camera.

The `"camera"` property MUST NOT be used together with the `"bone"`, `"light"`, `"meshInstance"`, `"modelInstance"`, `"physics"`, or `"skeleton"` properties on the same node.

See [G4MF Camera](camera.md) for more information about cameras.

#### Light

The `"light"` property is an object that defines the light properties for this node. If not specified, the default value is `undefined`, meaning the node is not a light.

The `"light"` property MUST NOT be used together with the `"bone"`, `"camera"`, `"meshInstance"`, `"modelInstance"`, `"physics"`, or `"skeleton"` properties on the same node.

See [G4MF Light](light.md) for more information about lights.

#### Mesh Instance

The `"meshInstance"` property is an object defining a mesh instance attached to this node. If not specified, the default value is `undefined`, meaning the node is not a mesh instance.

Meshes are the most common way to provide visible geometry for a node. A mesh may be instanced by multiple nodes, or a mesh may be used by zero nodes. Each mesh instance object defines a `"mesh"` property inside of it, which is a reference to a mesh in the G4MF file's document-level `"meshes"` array. When a node's `"meshInstance"` is defined, its `"mesh"` MUST be a valid index in the `"meshes"` array.

The `"meshInstance"` property MUST NOT be used together with the `"bone"`, `"camera"`, `"light"`, `"modelInstance"`, `"physics"`, or `"skeleton"` properties on the same node.

See [G4MF Node Mesh Instance](mesh/node_mesh_instance.md) for more information about mesh instances, and see [G4MF Mesh](mesh/mesh.md) for more information about meshes.

#### Model Instance

The `"modelInstance"` property is an object defining a model instance attached to this node. If not specified, the default value is `undefined`, meaning the node is not a model instance.

Models are references to other self-contained files that can be used in the scene hierarchy. They are not to be confused with meshes, which are geometry data only, while models may be complex objects made of many nodes and many meshes. Models may be embedded or saved as separate files. Models may be in the G4MF format, or in other formats such as [OFF](https://en.wikipedia.org/wiki/OFF_%28file_format%29), glTF™, [OCIF](https://github.com/ocwg/spec), or any other format.

When a host node has a `"modelInstance"` property defined, it is an instance of that model, such that the host node becomes a new instance of the model's nodes, inserting a potentially large tree of nodes into the scene hierarchy. The instantiated root node replaces the host node, except that the host's properties, such as the transform properties, override the properties of the instantiated model's root node. Additionally, model instances may specify overrides for nodes and materials within the model instance, referring to them by unique names defined within the model.

The `"modelInstance"` property MUST NOT be used together with the `"bone"`, `"camera"`, `"light"`, `"meshInstance"`, `"physics"`, or `"skeleton"` properties on the same node.

See [G4MF Node Model Instance](model/node_model_instance.md) for more information about model instances, and see [G4MF Model File Reference](model/model_file_ref.md) for more information about models.

#### Physics

The `"physics"` property is an object that defines the physics properties for this node. If not specified, the default value is `undefined`, meaning the node has no physics properties.

Physics information MAY be ignored by static renderers or any other applications that do not support physics simulation. For such applications, physics nodes may be treated as plain/empty nodes with no special properties or behavior other than the children, visibility, and transform properties, entirely ignoring the `"physics"` property.

The `"physics"` property MUST NOT be used together with the `"bone"`, `"camera"`, `"light"`, `"meshInstance"`, `"modelInstance"`, or `"skeleton"` properties on the same node.

See [G4MF Node Physics](physics/node_physics.md) for more information about physics properties.

#### Skeleton

The `"skeleton"` property is an object that defines the skeleton root properties for this node. If not specified, the default value is `undefined`, meaning the node is not a skeleton root.

The `"skeleton"` property is used to define the root of a hierarchy of bones used for skeletal animation. Skinned meshes MAY be added as direct children of the skeleton root node to be animated by the skeleton.

The `"skeleton"` property MUST NOT be used together with the `"bone"`, `"camera"`, `"light"`, `"meshInstance"`, `"modelInstance"`, or `"physics"` properties on the same node.

See [G4MF Skeleton Skinned Mesh Deformation](mesh/skeleton.md) for more information about skeletons and skinned meshes.

## JSON Schema

See [g4mf.node.schema.json](../schema/g4mf.node.schema.json) for the node properties JSON schema.
