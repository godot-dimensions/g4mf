# G4MF Mesh Topology

G4MF allows defining topology data for mesh surfaces, which defines how the mesh surface is hierarchically structured in terms of its geometry and connectivity.

This is useful for DCC applications, but not required for runtime applications like game engines. To save space, this data SHOULD be omitted when exporting an optimized model only intended to be consumed by a runtime application, rather than edited in a DCC application.

## Overview

G4MF stores the visible geometry of objects inside of meshes. Each mesh is made of multiple surfaces, each of which may have a separate material. Mesh surfaces have vertices, and may contain edge indices, cell indices, and more, each of which points to an accessor that encodes the data (see [G4MF Data Storage](data.md)).

## Example

The following example defines.

## Mesh Topology Properties

| Property       | Type        | Description                                                                       | Default            |
| -------------- | ----------- | --------------------------------------------------------------------------------- | ------------------ |
| **geometry**   | `integer[]` | Hierarchical geometry data for this surface.                                      | `[]` (empty array) |
| **normals**    | `integer`   | The per-vertex-instance normals of boundary geometry items.                       | Flat normals       |
| **seams**      | `integer`   | The list of which boundary geometry items are marked as seams.                    | No seams           |
| **textureMap** | `integer`   | The texture space coordinates of the vertex instances of boundary geometry items. | No texture mapping |

### Geometry

The `"geometry"` property is an array of integers, each of which is an index that references an accessor containing complex hierarchical geometry data for this surface. If not defined, the surface does not have any complex hierarchical geometry data.

Hierarchical geometry data means that polytopes of successive dimensions are defined as combinations of polytopes from the previous dimension, providing structured topological data. This is similar to the data found within the [OFF file format](https://en.wikipedia.org/wiki/OFF_%28file_format%29), except that the first tier references edges, not points.

- The accessor at index 0 contains 2D faces. The first number is the amount of 1D edges on the boundary of the face, followed by the indices of the edges in the accessor referred to by the `"edges"` property. The next number after that is the amount of edges on the boundary of the second face, and so on.
- The accessor at index 1 contains 3D volumes. The first number is the amount of 2D faces on the boundary of the volume, followed by the indices of the faces just defined in the previous step. The next number after that is the amount of faces on the boundary of the second volume, and so on.
- The accessor at index 2 contains 4D hypervolumes. The first number is the amount of 3D volumes on the boundary of the hypervolume, followed by the indices of the volumes just defined in the previous step. The next number after that is the amount of volumes on the boundary of the second hypervolume, and so on.
- The accessor at index 3 contains 5D hypervolumes, which refer to 4D hypervolumes, and so on for 6D, 7D, and higher dimensional hypervolumes.

If defined, the array SHOULD have an amount of entries equivalent to the dimension of the model minus two, if defining only boundary geometry, or minus one, if filling the shape. For example, a 3D model may have geometry with index 0 for 2D faces, which define the boundary of the shape, in an array length of 1. Optionally, index 1 may be included, which would fill the shape solid using an array of length 2. For example, a 4D model may have geometry with index 0 for 2D faces and index 1 for 3D volumes, collectively defining the boundary of the shape, in an array length of 2. Optionally, index 2 may be included, which would fill the shape solid using an array of length 3.

This property allows preserving geometric information about polytopes and the connections between their parts. This is useful for DCC applications, and allows them to use G4MF as a save format. For example, Blender stores how faces connect to edges, therefore also storing how the faces connect to each other, preserving the topology of the mesh. Such information is useful for high-level operations like subdivision, smoothing, defining seams, and other operations that require knowledge of how the mesh topology is structured.

This property is not needed to render a cellular mesh if the `"cells"` property is defined, since the `"cells"` property contains ready-to-use simplex cells. If the `"cells"` property is not present, the simplex cells can be computed from the geometry data, however this may be computationally expensive, especially for higher dimensions. When exporting a model to a final destination such as a game engine or other runtime, it is recommended to define the `"cells"` property, and the `"geometry"` property may be omitted to reduce file size.

Since the geometry accessor 0 refers to edges, the `"edges"` property MUST be defined and set to a valid value if the `"geometry"` property is defined and non-empty. If `"edges"` is not defined, and edges are calculated from the cells, this calculated data CANNOT be used as the edges referenced by the `"geometry"` property.

### Normals

The `"normals"` property is an integer that references an accessor containing the per-boundary-vertex-instance normals for this surface. If not defined and the `"geometry"` property is defined, the geometry has flat normals.

For 3D meshes, this refers to vertex instances on 2D faces defined in the `"geometry"` property. For 4D meshes, this refers to vertex instances on 3D cells defined in the `"geometry"` property. For 5D meshes, this refers to vertex instances on 4D cells defined in the `"geometry"` property. See [Topology Vertex Instances](#topology-vertex-instances) for more details. Also, see [Orientation of Geometry Items](#orientation-of-geometry-items) for information about calculating normals of boundary geometry items for use cases like determining if a cell is facing towards or away from a camera.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of a floating-point primitive type, and MUST have the `"vectorSize"` property set to the same value as the `"vectorSize"` of the vertices accessor. The amount of vectors in the accessor MUST be equal to the amount of vertex instances in the corresponding geometry items.

### Seams

The `"seams"` property is an integer that references an accessor containing the list of which boundary geometry items are marked as seams. If not defined, the surface does not have seams.

Seams refer to the boundaries of boundary geometry items; this is the dimension of the mesh minus 2. For 3D meshes, seams refer to 1D edges defined in the mesh surface `"edges"`, which bound 2D faces, since 2D faces form the boundary of 3D meshes. For 4D meshes, seams refer to 2D faces defined in the `"geometry"` property, which bound 3D cells, since 3D cells form the boundary of 4D meshes. For 5D meshes, seams refer to 3D cells defined in the `"geometry"` property, which bound 4D cells, since 4D cells form the boundary of 5D meshes, and so on for higher dimensions. 2D meshes are an exception, they use 2D faces like 3D meshes, and so their seams refer to 1D edges like 3D meshes.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an unsigned integer primitive type, and MUST have the `"vectorSize"` property undefined or set to its default value of 1. Each primitive number in the array is an index of an item in either the `"edges"` accessor or one of the accessors in `"geometry"`, and MUST NOT exceed the amount of boundary geometry items in the referenced accessor. For example, for 3D meshes, the maximum value in the seams accessor MUST NOT exceed the amount of edges in the `"edges"` accessor. For 4D meshes, the maximum value in the seams accessor MUST NOT exceed the amount of faces in the first geometry accessor, and so on. The seams accessor MUST NOT contain duplicate values, and MUST be sorted in strictly ascending order.

### Texture Map

The `"textureMap"` property is an integer index that references an accessor containing the per-vertex-instance texture map data for the toplogy vertex instances. If not defined, the topology does not have per-vertex-instance texture mapping.

A texture map, also known as a UV map, UVW map, or texture coordinate map, is a mapping from the indices of the vertex instances to the texture space coordinates. This property is similar to the `"textureMap"` property in the mesh surface, but instead of mapping the mesh surface's vertex instances, it maps the topology vertex instances. See [Topology Vertex Instances](#topology-vertex-instances) for more information on how topology vertex instances are defined. See [G4MF Mesh Texture Map](mesh.md#texture-map) for more information on how texture maps are defined.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type, and values are usually on a range of 0.0 to 1.0. The accessor MUST have its `"vectorSize"` property set to the dimension of the texture space. The amount of vector elements in the accessor MUST match or exceed the amount of topology vertex instances.

## Topology Vertex Instances

In addition to each mesh surface having vertex instances defined by the `"cells"` or `"edges"` properties, the `"topology"` property contains its own set of vertex instances defined by boundary geometry items. Topology vertex instances may be used to define normal vectors, and may be used by materials to define per-vertex-instance data, such as colors or texture coordinates, for a mesh surface's topology.

Topology vertex instances are defined as the following:

- For 3D meshes, the topology vertex instances are those used by 2D faces defined in the `"geometry"` property.
- For 4D meshes, the topology vertex instances are those used by 3D cells defined in the `"geometry"` property.
- For 5D meshes, the topology vertex instances are those used by 4D cells defined in the `"geometry"` property.
- This pattern continues for higher dimensions. 2D meshes are an exception, they use 2D faces like 3D meshes.
- Extensions may define other ways to determine the topology vertex instances for a mesh surface's topology.

This defines the source of the vertices, but the order still needs to be specified. To find the vertex instances, iterate over each N-dimensional boundary geometry item, then iterate over its (N-1)-dimensional elements, recursively and in-order, until reaching the vertex instances. Append these to a unique array, skipping duplicates, again preserving order. The resulting array is the cell's topology vertex instances.

## Orientation of Geometry Items

Use cases like determining if a boundary geometry item is facing towards or away from a camera require having normal vectors which are perpendicular to the cell they describe. These normal vectors can be calculated, but then it is important to not only know how the geometry items are connected, but also their orientation. There are rules to uniquely determine the orientation of each geometry item based on its component parts. The rules mandated by G4MF follow the rules of Geometric Algebra extended from the right-hand rule.

Each 2D face has its orientation defined by its first 2 edges. The first 2 edges MUST share a vertex. Following edges MUST exist on the same plane spanned by the first 2 edges, MUST form a closed loop. For 2D faces only, the following edges MUST continue to share a vertex with the previous edge, until reaching the last edge, which MUST share a vertex with the first edge, closing the loop. The order of the first 2 edges defines the winding of the face. If the face's first 2 edges are swapped, the face's orientation is reversed. When a 2D face is used as the boundary of a 3D mesh, a counter-clockwise winding viewed by the camera means the face is facing towards the camera, while clockwise means it is facing away from the camera.

![2D Face Orientation](2d_face_orientation.png)

The face winding order is determined purely by the order of the edges, and does not consider the order of vertices within each edge. In this example image, if the arrows were pointing in the opposite direction, but the face still listed edge U before edge V, the face would still be considered to be facing towards the camera when interpreted as the boundary of a 3D mesh. To calculate the face normal, first find which vertex is shared between edge U and edge V. Find two vectors, one from the unshared vertex of edge U to the shared vertex, and one from the unshared vertex of edge U to the unshared vertex of edge V. Then, in 3D, the face normal is the cross product of these two vectors. Those three vertices, in that order, are also the first 3 vertices of the face as defined by G4MF's topology vertex instance rules.

Each 3D cell has its orientation defined by its first 2 faces. The first 2 faces MUST share an edge. Following faces MUST exist on the same 3D hyperplane spanned by the first 2 faces, and MUST form a closed 3D volume. For dimensions 3 and higher, the order of following elements is not constrained, since it is not trivially defined how to traverse a closed volume in higher dimensions. The order of the first 2 faces defines the oriented volume of the cell. If the cell's first 2 faces are swapped, the cell's orientation is reversed. When a 3D cell is used as the boundary of a 4D mesh, an orientation like the below image in the XYZ axes means the cell is facing in the +W direction.

![3D Cell Orientation](3d_cell_orientation.png)

To calculate the cell normal, first find which edge is shared between the first 2 faces. In this example, the first face is the bottom face, formed by U and V, and the second face is the right face, formed by V and W. Get the edge on the first face after the shared edge, and get the edge on the second face after the shared edge. From those edges, get 4 vertices: the unshared vertex of the edge from the first face, the start vertex of the shared edge, the end vertex of the shared edge (such that the shared edge direction matters), and the unshared vertex of the edge from the second face (which adds to the span of the first face). Then, find the perpendicular product of the three vectors formed by the first vertex to each of the other three vertices. A cell facing in the +W direction, when these vectors are viewed in the XYZ axes, appears like the vectors of a right-handed basis with a positive determinant. Those four vertices, in that order, are also the first 4 vertices of the cell as defined by G4MF's topology vertex instance rules.

For dimensions 5 and higher, it is still the case that each N-dimensional cell has its orientation defined by its first two (N-1)-dimensional elements, which MUST share an (N-2)-dimensional element. Following elements MUST exist on the same N-dimensional hyperplane spanned by the first two elements, and MUST form a closed N-dimensional volume.

For more information, see the "Exterior Algebra" article on Wikipedia: https://en.wikipedia.org/wiki/Exterior_algebra

<sub>Both of the above images were created by Maschen, licensed as CC0 via Wikimedia Commons https://commons.wikimedia.org/wiki/File:N_vector_positive.svg</sub>

## JSON Schema

- See [g4mf.mesh.surface.topology.schema.json](../../schema/mesh/g4mf.mesh.surface.topology.schema.json) for the mesh surface topology properties JSON schema.
- See [g4mf.mesh.surface.schema.json](../../schema/mesh/g4mf.mesh.surface.schema.json) for the mesh surface properties JSON schema.
- See [g4mf.mesh.schema.json](../../schema/mesh/g4mf.mesh.schema.json) for the mesh properties JSON schema.
