# G4MF Node

## Overview

Nodes are the core building block of a G4MF file. Each node defines an object in the scene with a transform, defines child nodes that are attached to it, and have other data attached to them to define the type of object they represent.

Each node defines a transform, which is a combination of a position, and a basis or rotor+scale. The basis is a set of usually orthogonal vectors that define the local rotation, scale, and shear of the object, giving full control over the object's transform. The the rotor+scale representation allows defining the rotation and scale separately, which is useful for human readability and animations that change these properties independently. The scale is defined within the node's own local space, including the node's own rotation, while all other transform properties are defined relative to the parent node's space.

The node at index 0 is the root node. All other nodes in the file are either descendants of the root node, or are not used. Nodes not used in the core scene hierarchy MAY be used by extensions. G4MF files may also contain zero nodes, in which case the file is not a scene, but a collection of data, such as a 4D mesh. The root node at index 0 MUST be untransformed, meaning its transform properties either MUST NOT be set or MUST be set to their default values.

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

| Property     | Type        | Description                                                 | Default            |
| ------------ | ----------- | ----------------------------------------------------------- | ------------------ |
| **position** | `number[]`  | The position of the node, relative to its parent node.      | Zero vector        |
| **basis**    | `number[]`  | The basis of the node, relative to its parent node.         | Identity matrix    |
| **rotor**    | `number[]`  | The rotation of the node, relative to its parent node.      | Identity rotor     |
| **scale**    | `number[]`  | The scale of the node, relative to its own local rotation.  | Scale of 1         |
| **children** | `integer[]` | The indices of the child nodes of this node.                | `[]` (empty array) |
| **camera**   | `object`    | If this node is a camera, the camera properties.            | `null`             |
| **light**    | `integer`   | If this node is a light, the index of the light properties. | `-1` (no light)    |
| **mesh**     | `integer`   | If this node is a mesh instance, the index of the mesh.     | `-1` (no mesh)     |
| **visible**  | `boolean`   | Whether the node is visible or not (affects rendering).     | `true`             |

### Transform Properties

#### Position

The `"position"` property is an array of numbers defining the position of the node, relative to its parent node. The default value is a zero vector, meaning the node is at the origin of its parent node.

If defined, the number of elements in the array MUST be equal to the dimension of the model. For example, with `"dimension": 4`, the `"position"` property MUST be an array of 4 numbers. If the number of elements is not equal to the dimension, the file is not a valid G4MF file.

#### Basis

The `"basis"` property is an array of numbers defining the basis of the node, relative to its parent node. If not specified, use `"rotor"` and `"scale"` instead, or the node's local basis is the identity matrix.

The basis is defined as an NxN matrix, stored as a linear array in column-major order, where N is the dimension of the model. If defined, the number of elements in the array MUST be equal to the square of the dimension of the model. For example, with `"dimension": 4`, the `"basis"` property MUST be an array of 16 numbers. If the number of elements is not equal to the square of the dimension, the file is not a valid G4MF file.

When the `"basis"` property is not defined, a basis can be calculated from the `"rotor"` and `"scale"` properties. The `"rotor"` property defines the rotation of the local basis vectors relative to the identity, and the `"scale"` property defines the length of each local basis vector. The calculated basis represents the local basis relative to the parent node's basis. Similarly, if the `"basis"` property is orthogonal and has a positive determinant, the `"rotor"` and `"scale"` properties can be calculated from the basis.

#### Rotor

The `"rotor"` property is an array of numbers defining a geometric algebra rotor, encoding the rotation relative to the parent node. If not specified and `"basis"` is not specified, the node is unrotated.

A geometric algebra rotor contains all elements of the even subalgebra of geometric algebra: scalar, bivector, 4-vector, 6-vector, and so on, which combine to represent simple rotations, double rotations, and so on. For 4D, the rotor is composed of scalar, bivector, and optional pseudoscalar parts, for a total of 7 or 8 numbers. The scalar part is the first number at index 0, the bivector part is the next 6 numbers, and the optional pseudoscalar is the last number at index 7. A 2D bivector has 1 number, a 3D bivector has 3 numbers, a 4D bivector has 6 numbers, and a 5D bivector has 10 numbers, and so on. Therefore, a 2D rotor has 2 numbers, a 3D rotor has 4 numbers, a 4D rotor has 7 or 8 numbers, and a 5D rotor has 11 or 16 numbers (five 4-vectors), and so on. A 3D rotor is the isomorphic to a quaternion, but the element order and rotation convention is different from most software.

The components of `"rotor"` are stored in an algebra-increasing and then dimensionally-increasing order. A 2D rotor is `[scalar, xy]`, a 3D rotor is `[scalar, xy, xz, yz]`, a 4D rotor is `[scalar, xy, xz, yz, xw, yw, zw, xyzw]`, a 5D rotor is `[scalar, xy, xz, yz, xw, yw, zw, xv, yv, zv, wv, xyzw, xyzv, xywv, xzwv, yzwv]`, and so on. In terms of dimension indices, a 2D rotor is `[scalar, 01]`, a 3D rotor is `[scalar, e01, e02, e12]`, a 4D rotor is `[scalar, e01, e02, e12, e03, e13, e23, e0123]`, a 5D rotor is `[scalar, e01, e02, e12, e03, e13, e23, e04, e14, e24, e34, e0123, e0124, e0134, e0234, e1234]`, and so on.

This order allows, for simple rotations, easy casting between dimensions by adding or discarding the last numbers. For example, a 4D rotor can be cast to a 3D rotor by discarding all but the first 4 numbers and normalizing, a 5D rotor can be cast to a 4D rotor by discarding all but the first 7 numbers and normalizing, a 3D rotor can be upgraded to a 4D rotor by resizing the array to have 7 or 8 numbers, and a 4D rotor can be upgraded to a 5D rotor by resizing the array to have 11 or 16 numbers and moving the pseudoscalar. G4MF is a multi-dimensional format and requires all objects within the file to use the dimension declared in `"asset"`, however, this order makes it easier for software to read a file and convert it to a different dimension on import without completely discarding the data. This allows, for example, 4D engines to read 5D models, without any downsides for applications that correctly read the entirety of information from all dimensions, such as 4D engines reading 4D models.

The elements beyond scalar and bivector are optional to allow for increased storage efficiency. When storing the entire even subalgebra, a 7D rotation matrix is 49 numbers, but the 7D even subalgebra is 64 numbers. By making the 4-vector etc elements optional, this means for the common case of a node with a single rotation, an incomplete scalar-and-bivector-only rotor can be used to store this simple rotation in less than half the space of a rotation matrix, with all missing 4-vector, 6-vector, etc numbers assumed to be zero. This is also why in the 5D case the number at index 7 is NOT `xyzw`/`e0123`, but rather the start of 5D-specific bivector numbers. By contrast, for more complex cases in higher dimensions, storing the full rotation matrix in the `"basis"` property is more efficient, and SHOULD be preferred for complex rotations in 7D and higher.

Note that this may be different from other conventions, such as 3D quaternions (usually `[x, y, z, w]` meaning `[yz, zx, xy, scalar]`), or dimensional-specific lexicographic geometric algebra (4D `[scalar, xy, xz, xw, yz, yw, zw, xyzw]` note the position of `xw`). By convention, "lexicographic" in this context refers to the axis indices, not the letter labels placed on them, which means that W comes after X, Y, and Z even though W comes before them alphabetically. To convert between different ordering conventions, simply re-order the numbers in the array.

Note that each component is also dimensionally-increasing within itself, meaning `xy` is used instead of `yx`, `xz` is used instead of `zx`, and so on. 3D software typically uses the convention of `zx` to follow the right-hand rule, but this does not generalize to higher dimensions. To convert between the two bivector conventions, negate the component: `xz == -zx` and `zx == -xz`. For the ordering of 4-vector, 6-vector, etc, the sign flips whenever an odd number of neighboring indices are swapped: `xyzw == -xywz == xwyz == -wxyz`.

#### Scale

The `"scale"` property is an array of numbers defining the scale of the node, relative to its own local space. If not specified and `"basis"` is not specified, the node is unscaled.

The scale may either be an array of one number, which defines a uniform scale, or an array of N numbers, which defines a non-uniform scale. The number of elements in the array MUST either be 1 or equal to the dimension of the model. For example, with `"dimension": 4`, the `"scale"` property MUST be either an array of 1 number, or an array of 4 numbers. If the number of elements is not equal to 1 or the dimension, the file is not a valid G4MF file.

The scale MUST consist of only positive numbers as values. The values MUST NOT be zero, and MUST NOT be negative. This requirement is because standards for negative scale are tricky across dimensions. An even number of negative scales is equivalent to a positive scale with a rotation, so a 4D node would need either 1 or 3 of the scale numbers to be negative for a negative scale to result in a flip. The choice of which scale numbers to be negative when decomposing from a transformation matrix is arbitrary and may vary between implementations. In order to represent a flip, a `"basis"` with a negative determinant can be used instead, which is a more explicit representation of the transformation.

### Children

The `"children"` property is an array of integers that defines the indices of the child nodes of this node. If not specified, the default value is an empty array, meaning the node has no children.

The indices in the array MUST be valid indices in the G4MF file's document-level `"nodes"` array. The order of the indices in the array is significant, as it affects the order of the nodes in the scene tree. A node may only be a child at most once, meaning that each node may only have at most one parent. The node at index 0 is the root node, it has no parent in the G4MF file, and no other node may use it as a child.

### Camera

The `"camera"` property is an object that defines the camera properties for this node. If not specified, the default value is `null`, meaning the node is not a camera.

The `"camera"` property MUST NOT be used together with the `"light"` or `"mesh"` properties.

See [G4MF Camera](camera.md) for more information about cameras.

### Light

The `"light"` property is an integer index of a G4MF light. If not specified, the default value is `-1`, meaning the node is not a light.

The `"light"` property MUST NOT be used together with the `"camera"` or `"mesh"` properties.

See [G4MF Light](light.md) for more information about lights.

### Mesh

The `"mesh"` property is an integer index of a G4MF mesh. If not specified, the default value is `-1`, meaning the node is not a mesh.

Meshes are the most common way to provide visible geometry for a node. A mesh may be used by multiple nodes, or a mesh may be not used by any nodes. This is a reference to a mesh in the G4MF file's document-level `"meshes"` array. When defined, it MUST be a valid index in the array.

The `"mesh"` property MUST NOT be used together with the `"camera"` or `"light"` properties.

See [G4MF Mesh](mesh.md) for more information about meshes.

### Visible

The `"visible"` property is a boolean value that defines whether the node is visible or not. If not specified, the default value is `true`, meaning the node is visible. If set to `false`, the node is not rendered in the scene.

The visibility of a node in a tree is determined by its own visibility and the visibility of all its ancestors. If a node is has `"visible"` set to false, it and all its descendants are not visible in the tree. If a node is visible in the tree, that may only occur when it and all its ancestors are visible.

The `"visible"` property is not a generic way to disable nodes in the scene. It only defines the ability of a node and its descendants to be rendered. Physics objects, such as bodies and collision shapes, are not affected by the visibility of a node.

## JSON Schema

See [g4mf.node.schema.json](../schema/g4mf.node.schema.json) for the node properties JSON schema.
