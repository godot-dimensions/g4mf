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

| Property     | Type     | Description                                           | Default                      |
| ------------ | -------- | ----------------------------------------------------- | ---------------------------- |
| **bone**     | `object` | If this node is a skeleton bone, the bone properties. | `undefined` (not a bone)     |
| **skeleton** | `object` | If this node is a skeleton, the skeleton properties.  | `undefined` (not a skeleton) |

### Bone

The `"bone"` property is an object that defines the bone properties for this node. If not specified, the default value is `undefined`, meaning that the node is not a bone.

All skeleton bones MUST have the `"bone"` property defined, even if it is an empty object. A node is a bone if and only if the `"bone"` property is defined; the absence of the `"bone"` property indicates that the node is not a bone. A bone MUST be a descendant of a skeleton, and MUST belong to exactly one skeleton, as indicated by the `"skeleton"` property. The parent node of a bone MUST either be another bone or the skeleton node itself, meaing that all bones MUST have a contiguous chain of bone parenting leading up to a skeleton node. Additional properties MAY be added to bones by extensions.

### Skeleton

The `"skeleton"` property is an object that defines the skeleton properties for this node. If not specified, the default value is `undefined`, meaning that the node is not a skeleton.

All skeletons MUST have the `"skeleton"` property defined, even if it is an empty object. A node is a skeleton if and only if the `"skeleton"` property is defined; the absence of the `"skeleton"` property indicates that the node is not a skeleton. All descendant bone nodes of the skeleton, which form a contiguous chain of bone parenting to the skeleton node, are considered part of the skeleton. The `"skeleton"` property MAY have the `"joints"` property defined when it is used for skinned meshes, which defines the bones used for controlling the joints of skinned meshes. Additional properties MAY be added to skeletons by extensions.

## Node Bone Properties

| Property   | Type      | Description                                                             | Default            |
| ---------- | --------- | ----------------------------------------------------------------------- | ------------------ |
| **length** | `number`  | The length of the bone in meters in the local +Y direction, if defined. | No defined length. |
| **mass**   | `number`  | The mass of the bone in kilograms, if defined.                          | No defined mass.   |
| **shape**  | `integer` | The index of the shape referenced by this bone, if defined.             | No defined shape.  |

### Length

The `"length"` property is a number that defines the length of the bone in meters. This property is optional, and if not defined, the bone does not have a defined length.

If a bone has the `"length"` property defined, it MUST NOT be negative. The value `-1.0` is reserved as an in-memory value for undefined lengths, and MUST NOT be written into G4MF files. The length of the bone is used to determine how far the bone extends along the local Y axis of the bone node. The head of the bone is defined as the node's position, and the tail of the bone is offset from this position by `"length"` in the local +Y direction. The final perceived bone length includes scale, so if the bone node has a `"length"` property set to 0.1 and has a global scale of 3.0 along the local Y axis, the effective global bone length is 0.3 meters.

### Mass

The `"mass"` property is a number that defines the mass of the bone in kilograms. This property is optional, and if not defined, the bone does not have a defined mass.

The mass of the bone MAY be used for physics simulations, such as ragdoll physics, or for other purposes. If an application does not support per-bone masses, it MAY safely ignore this property.

If a bone has the `"mass"` property defined, it MUST NOT be negative. If the mass is set to exactly `0.0`, it indicates that the bone is not meant to be simulated on its own, and rather provides shapes for its first ancestor bone that has a non-zero mass. If the mass is undefined or negative, the application MAY choose to infer the mass of the bone using any heuristic it desires. The value `-1.0` is reserved as an in-memory value for undefined masses, and MUST NOT be written into G4MF files.

If all bones in a skeleton have their `"mass"` property defined, and the skeleton has a physics motion parent, the total of all bone masses SHOULD add up to the mass of the physics body defined by the parent node's physics motion properties, within the margin of floating-point error. If some or no bones have their `"mass"` property defined, the application MAY choose to infer the masses of the undefined bones by distributing the remaining mass to them. If the shapes of bones are defined, the volume of each bone's shape is recommended to be the heuristic used for this distribution.

### Shape

The `"shape"` property is an integer index of the shape referenced by this bone. This property is optional, and if not defined, the bone does not specify a shape.

This is a reference to a shape in the G4MF file's document-level `"shapes"` array. The value `-1` is reserved as an in-memory value for undefined shapes, and MUST NOT be written into G4MF files. If the `"shape"` property is not defined, the bone does not specify a shape, and any shape MAY be inferred by the application using any heuristic it desires. The shape MAY be used for visualization, hit registration, ragdoll physics, or any other use case.

The position of the shape is defined relative to the center of the bone's `"length"`, meaning that if a bone has a length of `L`, the shape's local origin is placed at an offset of `L / 2` in the local +Y direction from the bone's position. The shape uses the bone's local basis without additional rotations or scaling applied, meaning that the shape's local basis axes align with the bone's local basis axes.

The `"shape"` property depends on the `"length"` property. If `"shape"` is defined, `"length"` MUST also be defined. This is because the shape's local origin is positioned at the midpoint of the bone's length, which is ambiguous if the length is undefined or inferred. Therefore, shape placement is only valid when an explicit `"length"` value is provided. This requirement ensures that the position of a shape can always be determined correctly, without any ambiguity.

## Node Skeleton Properties

| Property   | Type        | Description                                                                               | Default            |
| ---------- | ----------- | ----------------------------------------------------------------------------------------- | ------------------ |
| **joints** | `integer[]` | An array of G4MF node indices that represent the bones in the skeleton used for skinning. | `[]` (empty array) |

### Joints

The `"joints"` property is an array of integers that defines the indices of G4MF nodes that represent the bones in the skeleton used as joints for controlling vertex groups of skinned meshes. This property is optional and defaults to an empty array.

All joint nodes MUST also be bone nodes. Each and every bone node referred to in this array MUST have the `"bone"` property defined, even if it is an empty object, which indicates that it is a bone. All indices in this array MUST refer to G4MF bone nodes that form a chain of bone descendants of the skeleton node. For example, if a bone node's parent does not have either the `"skeleton"` or `"bone"` properties defined, or any non-bone node exists between itself and the skeleton, it cannot be included in the skeleton's `"joints"` array.

All joint nodes MUST be listed in a strictly increasing order, and MUST be listed with parent bones before child bones. Usually, a skeleton representing a character will have a root bone named "Hips". If a skeleton has a single root bone, this MUST be the first child of the skeleton node, and if this bone is used for skinning, it MUST be the first item in the `"joints"` array. Skeletons MAY have multiple root bones, and MAY have bones not used for skinning, indicated by not being listed in the `"joints"` array.

The existence of the `"joints"` property allows preserving information about specifically which bones are used for controlling the joints of skinned meshes, and in what order. It would also be possible to generate this information from the skeleton hierarchy, but such an operation may produce different results depending how the application chooses to traverse the hierarchy, and would unnecessarily include bones not used for skinning, forcing skinned meshes to reserve an index for those unused bones.

The existence of the `"joints"` property also allows adding new bones and other nodes to the skeleton without breaking existing skinned meshes that use the skeleton. For example, without the `"joints"` property, if a new bone were added to the skeleton, existing bones may end up with different joint indices, which would break existing skinned meshes that use the skeleton if they were not updated to match the new joint indices, and would break if two different skeletons with different bone structures were used with the same skinned mesh. With the `"joints"` property, the skeleton can explicitly specify which bones map to the joint indices in skinned meshes.

If the same skeleton bone is desired to control multiple joints in a skinned mesh, it MAY be listed multiple times in this array, allowing for a skeleton to effectively "merge" those bones while keeping the mesh data unchanged. For example, if a tail is desired to be stiff and controlled by a single bone with node index 40, but the mesh has multiple joints for the tail, the `"joints"` property may contain `... 40, 40, 40, 40, 40, ...` in those spots. If a joint in a skinned mesh is desired to not be controlled by any bone, `-1` MAY be used in the `"joints"` array at that index, indicating that the joint is not controlled by any bone in the skeleton, and any vertex weights for that joint are treated as untransformed.
