# G4MF Skeleton Skinned Mesh Deformation

## Overview

G4MF allows meshes to be deformed using skins controlled by skeletons, also known as rigging, armatures, or skeletal meshes.

A skinned mesh is defined as being used by a skeleton if both of these conditions are met:

- The mesh is a direct child G4MF node with the `"skeleton"` property defined.
- The mesh has the `"skin"` property defined.

## Example

The following example defines.

## Mesh Skin Properties

| Property       | Type       | Description                                                                          | Default               |
| -------------- | ---------- | ------------------------------------------------------------------------------------ | --------------------- |
| **groupNames** | `string[]` | An optional array of names for the groups in the `groups` array.                     | `[]` (empty array)    |
| **groups**     | `integer`  | The index of the accessor that contains the group indices influencing the vertices.  | Required, no default. |
| **vertices**   | `integer`  | The index of the accessor that contains the indices of skinned vertices.             | Required, no default. |
| **weights**    | `integer`  | The index of the accessor that contains the weights for how strong the influence is. | Required, no default. |

The `"groups"`, `"vertices"`, and `"weights"` properties are all required and the arrays in these accessors have the same size as each other.

### Group Names

The `"groupNames"` property is an optional array of strings that defines the names of the vertex groups used for bones in this skin. If not defined, the groups are not named.

Group names are useful to facilitate editing of skinned meshes in DCC applications. When parenting both meshes to the same skeleton, the DCC application would need to unify the names and numbering of the groups to match with each other, and ensure this data remains consistent with all skeletons using the mesh. Some example cases:

- A character's body mesh may have a group name of "Hips" for its index 0, and have a total of 50 groups, while a separate hair mesh may have a group name of "Hair" for its index 0. When parenting both meshes to the same skeleton, the DCC application would need to renumber the second mesh's "Hair" group to index 50, and similarly renumbering all other groups in the second mesh.

- A character's body mesh may have a group name of "LeftArm" for its index 20, while a separate clothing mesh may have a group name of "LeftArm" for its index 10. When parenting both meshes to the same skeleton, the DCC application would need to converge these matching names to the same index, such as renumbering the clothing mesh's "LeftArm" group to index 20, and similarly renumbering all other groups in the clothing mesh with matching names. Alternatively, if the groups are intended to be kept separate, the clothing mesh's "LeftArm" group could be renamed to "ClothingLeftArm" before parenting.

- In either of the above cases, if instead of parenting to a skeleton, the meshes are merged together into a single mesh, the same rules apply. The merge operation MUST ensure that the group names are unique, renumbered correctly as needed, and that this remains consistent with the bones array of any and all skeletons using the mesh.

Group names MUST be unique within the skin, MUST NOT be empty strings, and MUST match the group names of other skinned meshes using the same skeleton. If the `"groupNames"` property is missing, but names are required by an application, importers SHOULD infer group names from bone node names of skeleton joint bone nodes, if available. Applications MAY choose to omit writing group names when exactly one skeleton is using the skinned mesh and the names are identical to the skeleton joint bone node names, allowing the names to be inferred, which avoids storing redundant data in the G4MF file.

### Groups

The `"groups"` property is an integer that defines the index of the accessor that contains the vertex group indices influencing the vertices. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an unsigned integer primitive type, and MUST have the `"vectorSize"` property undefined or set to its default value of 1. Each index in this accessor is a group index, and the corresponding items in the `"vertices"` and `"weights"` accessors define a vertex that is influenced by that group by that weight.

Each group may be listed multiple times in this accessor, allowing for a group to influence multiple vertices, or be listed only once if it influences a single vertex, or not at all if it does not influence any vertex. If a skeleton bone index is not present in this accessor, those bones are not used for skinning this mesh. If the maximum value of items in this accessor exceeds the number of bones in the skeleton, those groups do nothing. If the maximum value of items in this accessor is greater than the amount of group names, then those groups are not named.

### Vertices

The `"vertices"` property is an integer that defines the index of the accessor that contains the indices of skinned vertices. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an unsigned integer primitive type, and MUST have the `"vectorSize"` property undefined or set to its default value of 1. Each index in this accessor corresponds to a vertex in the mesh, and the corresponding items in the `"groups"` and `"weights"` accessors define which groups influence that vertex and by how much.

Each vertex may be listed multiple times in this accessor, allowing for multiple groups to influence the same vertex, or be listed only once if it is influenced by a single group, or not at all if it is not influenced by any group. The maximum value of items in this accessor MUST NOT exceed the number of vertices in the mesh. The values in this accessor MUST be sorted in ascending order, and MUST NOT decrease.

### Weights

The `"weights"` property is an integer that defines the index of the accessor that contains the weights for how strongly each group influences the corresponding vertex. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of a floating-point primitive type, and MUST have the `"vectorSize"` property undefined or set to its default value of 1. Each value in this accessor corresponds to a weight for the group at the same index in the `"groups"` accessor, and the corresponding vertex at the same index in the `"vertices"` accessor.

Within the weights for a single vertex, the influences MUST be sorted in descending order, with the first value being the strongest influence. For example, if vertex 0 is influenced by only groups 0, 1, and 2, with weights of 0.5, 0.75, and 0.25 respectively, the first three values in this accessor would be 0.75, 0.5, and 0.25, the first three values in the `"vertices"` accessor would be 0, 0, and 0, and the first three values in the `"groups"` accessor would be 1, 0, and 2. This allows implementations with arbitrary limits on the number of groups influencing a vertex to only read the first N values, where N is the maximum number of groups that can influence a vertex.

## Node Properties

A full list of G4MF node properties is defined in [G4MF Node](../node.md). Important for skeletons are these two mutually exclusive properties:

| Property       | Type     | Description                                                     | Default                 |
| -------------- | -------- | --------------------------------------------------------------- | ----------------------- |
| **boneLength** | `number` | If this node is a skeleton bone, the length in meters along +Y. | `-1.0` (not a bone)     |
| **skeleton**   | `object` | If this node is a skeleton, the skeleton properties.            | `null` (not a skeleton) |

### Bone Length

The `"boneLength"` property is a number that defines the length of the bone in meters. This property is optional and defaults to `-1.0`, indicating that the node is not a bone.

All bones MUST have a non-negative `"boneLength"` property defined, even if it is zero, to indicate that the node is a bone. The length of the bone is used to determine how far the bone extends along the local Y axis of the bone node. The head of the bone is defined as the node's position, and the tail of the bone is offset from this position by `"boneLength"` in the local +Y direction. The final perceived bone length includes scale, so if the bone node has a `"boneLength"` property set to 0.1 and has a global scale of 3.0 along the local Y axis, the effective global bone length is 0.3 meters.

### Skeleton

The `"skeleton"` property is an object that defines the skeleton properties for this node. This property is optional and defaults to `null`, indicating that the node is not a skeleton.

All skeletons MUST have the `"skeleton"` property defined, even if it is an empty object, to indicate that the node is a skeleton. All descendant bone nodes of the skeleton, indicated by the `"boneLength"` property, which form a contiguous chain of bone parenting to the skeleton node, are considered part of the skeleton. The `"skeleton"` property MAY have the `"joints"` property defined when it is used for skinned meshes, which defines the bones used for controlling the joints of skinned meshes. Additional properties MAY be added to skeletons by extensions.

## Node Skeleton Properties

| Property   | Type        | Description                                                                               | Default            |
| ---------- | ----------- | ----------------------------------------------------------------------------------------- | ------------------ |
| **joints** | `integer[]` | An array of G4MF node indices that represent the bones in the skeleton used for skinning. | `[]` (empty array) |

### Joints

The `"joints"` property is an array of integers that defines the indices of G4MF nodes that represent the bones in the skeleton used as joints for controlling vertex groups of skinned meshes. This property is optional and defaults to an empty array.

All joint nodes MUST also be bone nodes. Each and every bone node referred to in this array MUST have a non-negative `"boneLength"` property defined, even if it is zero, indicating that it is a bone. All indices in this array MUST refer to G4MF bone nodes that form a chain of bone descendants of the skeleton node. For example, if a bone node's parent does not have either the `"skeleton"` or `"boneLength"` properties defined, or any such node exists between itself and the skeleton, it cannot be included in the skeleton's `"joints"` array.

The existence of the `"joints"` property allows preserving information about specifically which bones are used for controlling the joints of skinned meshes, and in what order. It would also be possible to generate this information from the skeleton hierarchy, but such an operation may produce different results depending how the application chooses to traverse the hierarchy, and would unnecessarily include bones not used for skinning.

The existence of the `"joints"` property also allows adding new bones and other nodes to the skeleton without breaking existing skinned meshes that use the skeleton. For example, without the `"joints"` property, if a new bone were added to the skeleton, existing bones may end up with different joint indices, which would break existing skinned meshes that use the skeleton if they were not updated to match the new joint indices, and would break if two different skeletons with different bone structures were used with the same skinned mesh. With the `"joints"` property, the skeleton can explicitly specify which bones map to the joint indices in skinned meshes.

If the same skeleton bone is desired to control multiple joints in a skinned mesh, it MAY be listed multiple times in this array, allowing for a skeleton to effectively "merge" those bones while keeping the mesh data unchanged. For example, if a tail is desired to be stiff and controlled by a single bone with node index 40, but the mesh has multiple joints for the tail, the `"joints"` property may contain `... 40, 40, 40, 40, 40, ...` in those spots. If a joint in a skinned mesh is desired to not be controlled by any bone, `-1` MAY be used in the `"joints"` array at that index, indicating that the joint is not controlled by any bone in the skeleton, and any vertex weights for that joint are treated as untransformed.
