# G4MF Node

## Overview

Nodes are the core building block of a G4MF file. Each node defines an object in the scene with a transform, defines child nodes that are attached to it, and have other data attached to them to define the type of object they represent.

The node at index 0 is the root node. All other nodes in the file are either descendants of the root node, or are not used. Nodes not used in the core scene hierarchy MAY be used by extensions. G4MF files may also contain zero nodes, in which case the file is not a scene, but a collection of data, such as a 4D mesh. The root node at index 0 MUST NOT have a transform defined, or any transform properties must be set to their default values.

Each node defines a transform, which is a combination of a position, and a basis or rotor+scale. The basis is a set of usually orthogonal vectors that define the local rotation, scale, and shear of the object, giving full control over the object's transform. The the rotor+scale representation allows defining the rotation and scale separately, which is useful for human readability and animations that change these properties independently. The scale is defined within the node's own local space, including the node's own rotation, while all other transform properties are defined relative to the parent node's space.

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

| Property     | Type     | Description                                                | Default         |
| ------------ | -------- | ---------------------------------------------------------- | --------------- |
| **position** | number[] | The position of the node, relative to its parent node.     | Zero vector     |
| **basis**    | number[] | The basis of the node, relative to its parent node.        | Identity matrix |
| **rotor**    | number[] | The rotation of the node, relative to its parent node.     | Identity rotor  |
| **scale**    | number[] | The scale of the node, relative to its own local rotation. | Scale of 1      |
| **visible**  | boolean  | Whether the node is visible or not (affects rendering).    | `true`          |

#### Position

The `"position"` property is an array of numbers defining the position of the node, relative to its parent node. The default value is a zero vector, meaning the node is at the origin of its parent node.

If defined, the number of elements in the array MUST be equal to the dimension of the model. For example, with `"dimension": 4`, the `"position"` property MUST be an array of 4 numbers. If the number of elements is not equal to the dimension, the file is not a valid G4MF file.

#### Basis

The `"basis"` property is an array of numbers defining the basis of the node, relative to its parent node. If not specified, use `"rotor"` and `"scale"` instead, or the node's local basis is the identity matrix.

The basis is defined as an NxN matrix, stored as a linear array in column-major order, where N is the dimension of the model. If defined, the number of elements in the array MUST be equal to the square of the dimension of the model. For example, with `"dimension": 4`, the `"basis"` property MUST be an array of 16 numbers. If the number of elements is not equal to the square of the dimension, the file is not a valid G4MF file.

When the `"basis"` property is not defined, a basis can be calculated from the `"rotor"` and `"scale"` properties. The `"rotor"` property defines the rotation of the local basis vectors relative to the identity, and the `"scale"` property defines the length of each local basis vector. The calculated basis represents the local basis relative to the parent node's basis. Similarly, if the `"basis"` property is orthogonal and has a positive determinant, the `"rotor"` and `"scale"` properties can be calculated from the basis.

#### Rotor

The `"rotor"` property is an array of numbers defining a geometric algebra rotor, encoding the rotation relative to the parent node. If not specified and `"basis"` is not specified, the node is unrotated.

A rotor contains a scalar part and a bivector part. The scalar part is the first element at index 0, and the bivector part is the remaining elements. A 2D bivector has 1 number, a 3D bivector has 3 numbers, a 4D bivector has 6 numbers, and a 5D bivector has 10 numbers, and so on. Therefore, a 2D rotor has 2 numbers, a 3D rotor has 4 numbers, a 4D rotor has 7 numbers, and a 5D rotor has 11 numbers, and so on. A 3D rotor is the same as a quaternion, but the element order and rotation convention may be different from your software.

The bivector components of `"rotor"` are stored in a dimensionally-increasing order. A 2D rotor is `[scalar, xy]`, a 3D rotor is `[scalar, xy, xz, yz]`, a 4D rotor is `[scalar, xy, xz, yz, xw, yw, zw]`, a 5D rotor is `[scalar, xy, xz, yz, xw, yw, zw, xv, yv, zv, wv]`, and so on. In terms of dimension indices, a 2D rotor is `[scalar, 01]`, a 3D rotor is `[scalar, 01, 02, 12]`, a 4D rotor is `[scalar, 01, 02, 12, 03, 13, 23]`, a 5D rotor is `[scalar, 01, 02, 12, 03, 13, 23, 04, 14, 24, 34]`, and so on.

This order allows for easy casting between dimensions by adding or discarding the last elements, making it easy for G4MF to be a multi-dimensional format. For example, a 4D rotor can be cast to a 3D rotor by discarding the last 3 elements and normalizing, a 5D rotor can be cast to a 4D rotor by discarding the last 4 elements and normalizing, a 3D rotor can be upgraded to a 4D rotor by adding 3 zero elements, and a 4D rotor can be upgraded to a 5D rotor by adding 4 zero elements.

Note that this may be different from other conventions, such as 3D quaternions (usually `[x, y, z, w]` meaning `[yz, zx, xy, scalar]`), or dimensional-specific lexicographic geometric algebra (4D `[scalar, xy, xz, xw, yz, yw, zw]`). By convention, "lexicographic" refers to the axis indices, not the letter labels placed on them. To convert between different ordering conventions, simply re-order the elements in the array.

Note that each component is also dimensionally-increasing within itself, meaning `xy` is used instead of `yx`, `xz` is used instead of `zx`, and so on. 3D software typically uses the convention of `zx` to follow the right-hand rule, but this does not generalize to higher dimensions. To convert between the two conventions, negate the component: `xz == -zx` and `zx == -xz`.

#### Scale

The `"scale"` property is an array of numbers defining the scale of the node, relative to its own local space. If not specified and `"basis"` is not specified, the node is unscaled.

The scale may either be an array of one number, which defines a uniform scale, or an array of N numbers, which defines a non-uniform scale. The number of elements in the array MUST either be 1 or equal to the dimension of the model. For example, with `"dimension": 4`, the `"scale"` property MUST be either an array of 1 number, or an array of 4 numbers. If the number of elements is not equal to 1 or the dimension, the file is not a valid G4MF file.

The scale MUST consist of only positive numbers as values. The values MUST NOT be zero, and MUST NOT be negative. This requirement is because standards for negative scale are tricky across dimensions. An even number of negative scales is equivalent to a positive scale with a rotation, so a 4D node would need either 1 or 3 of the scale numbers to be negative for a negative scale to result in a flip. The choice of which scale numbers to be negative when decomposing from a transformation matrix is arbitrary and may vary between implementations. In order to represent a flip, a `"basis"` with a negative determinant can be used instead, which is a more explicit representation of the transformation.

#### Visible

The `"visible"` property is a boolean value that defines whether the node is visible or not. If not specified, the default value is `true`, meaning the node is visible. If set to `false`, the node is not rendered in the scene.

The visibility of a node in a tree is determined by its own visibility and the visibility of all its ancestors. If a node is has `"visible"` set to false, it and all its descendants are not visible in the tree. If a node is visible in the tree, that may only occur when it and all its ancestors are visible.

The `"visible"` property is not a generic way to disable nodes in the scene. It only defines the ability of a node and its descendants to be rendered. Physics objects, such as bodies and collision shapes, are not affected by the visibility of a node.
