# G4MF Mesh

## Overview

G4MF stores the visible geometry of objects inside of meshes. Each mesh is made of multiple surfaces, each of which may have a separate material. Mesh surfaces have vertices, and may contain edge indices, cell indices, and more, each of which points to an accessor that encodes the data (see [G4MF Data](data.md)).

## Example

The following example defines.

## Mesh Properties

| Property     | Type       | Description                                 | Default               |
| ------------ | ---------- | ------------------------------------------- | --------------------- |
| **surfaces** | `object[]` | An array of surfaces that make up the mesh. | Required, no default. |

## Mesh Surface Properties

| Property          | Type      | Description                                                                        | Default               |
| ----------------- | --------- | ---------------------------------------------------------------------------------- | --------------------- |
| **cells**         | `integer` | The index of the accessor that contains the cell indices for this surface.         | No cells.             |
| **edges**         | `integer` | The index of the accessor that contains the edge indices for this surface.         | No edges.             |
| **material**      | `integer` | The index of the material to use for this surface.                                 | No material.          |
| **polytopeCells** | `boolean` | If `true`, allow importing the cells as complex polytopes instead of simplexes.    | `false`               |
| **vertices**      | `integer` | The index of the accessor that contains the vertex data for this surface.          | Required, no default. |

### Cells

The `"cells"` property is an integer index that references an accessor containing the cell indices for this surface. If not defined, the surface does not have explicit cells, and may be a wireframe-only surface.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an integer primitive type, and MUST have the `"vectorSize"` property set to the number of vertices in a cell as determined by the dimension of the model: 3D models have triangular cells (3 vertices per cell), 4D models have tetrahedral cells (4 vertices per cell), and so on. Each primitive number in the array is an index of a vertex in the vertices array, and MUST NOT exceed the bounds of the vertices array.

### Edges

The `"edges"` property is an integer index that references an accessor containing the edge indices for this surface. If not defined, the surface does not have explicit edges, but edges may be calculated from the cells if needed.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an integer primitive type, and MUST have the `"vectorSize"` property set to 2. Each primitive number in the array is an index of a vertex in the vertices array, and MUST NOT exceed the bounds of the vertices array. Every two primitive numbers in the array form an edge, so the array MUST have an even number of primitives.

### Material

The `"material"` property is an integer index that references a material in the document-level `"materials"` array. If not defined, the surface does not have a material.

This is a reference to a material in the G4MF file's document-level `"materials"` array. The material MUST be defined in the array, and the index MUST NOT exceed the bounds of the materials array. If not defined, the surface does not have a material, and should be rendered with a default material.

See [G4MF Material](material.md) for more information about materials.

### Polytope Cells

The `"polytopeCells"` property is a boolean that indicates if cells should be imported as complex polytopes instead of simplexes. If not specified, the default is `false`.

If `true`, allow importing the cells as complex polytopes instead of simplexes. Each polytope is defined by a set of consecutive cells that share the same starting vertex. For example, in 3D a square polytope can be encoded as two triangle cells sharing the same starting vertex, and this flag marks those triangles as part of the square. Similarly, in 4D, a cube polytope can be encoded as set of 6 tetrahedral cells sharing the same starting vertex. Applications may ignore this flag to always import as simplexes, or use it to combine the cells as polytopes. To separate polytopes, choose a different starting vertex for each polytope.

Note: This only supports shar-shaped polytopes with a simply connected topology where there exists a point on or within the polytope from which all vertices can be seen. See the Wikipedia article on star-shaped polygons: https://en.wikipedia.org/wiki/Star-shaped_polygon

### Vertices

The `"vertices"` property is an integer index that references an accessor containing the vertex data for this surface. This property is required.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor SHOULD be of a floating-point primitive type, and MUST have the `"vectorSize"` property set to the dimension of the model. Vertices may be used by edges, cells, and anything else that wishes to use them.

## Calculating Cell Normals

In 3D rendering, winding order is used to determine which side of a triangle is the front or back. This is then used to decide if the triangle should be rendered or culled. The typical convention in right-handed coordinate systems like with OpenGL™ and glTF™ is to use a counter-clockwise winding order for meshes whose global basis has a positive determinant, and a clockwise winding order for meshes whose global basis has a negative determinant.

For dimensions other than 3D, we need to generalize this concept. Instead of referring to a visual winding order, we need to define orientation mathematically. The 3D rule is generalized by calculating the vector from vertex 0 to vertex 1, and the vector from vertex 0 to vertex 2, then taking the cross product of those two vectors. The resulting vector can have the dot product calculated with the camera's local Z axis to determine if the triangle is facing the camera or not. For meshes with positive determinants, the resulting vector should point towards the viewer in the same direction as the camera's local Z axis, and for meshes with negative determinants, the resulting vector should point away from the viewer in the opposite direction as the camera's local Z axis.

To generalize this to 4D, we need three vectors, from vertex 0 to vertex 1, from vertex 0 to vertex 2, and from vertex 0 to vertex 3. Then we need to pass these vectors into a function that returns a unique 4D vector that is perpendicular to all three of them. More generally, for N dimensions, we get N-1 vectors from vertex 0 to vertex N, then pass them into a function that returns a unique N-dimensional vector that is perpendicular to all of them. This is then used to calculate a dot product with the camera's local Z axis in the same way as in 3D (camera forward in G4MF is defined as -Z, like glTF™).

To calculate the perpendicular vector, you may use the functions defined in the [Calculating Perpendicular Vectors section of the G4MF Math specification](math.md#calculating-perpendicular-vectors).

It is recommended to pre-compute the cell normals before rendering and store them in memory, since calculating them can be expensive, especially for higher dimensions. However, since this information is recoverable from the cells, it would be redundant to store in G4MF.

## JSON Schema

See [g4mf.mesh.schema.json](../schema/g4mf.mesh.schema.json) for the mesh properties JSON schema, and [g4mf.mesh.surface.schema.json](../schema/g4mf.mesh.surface.schema.json) for the mesh surface properties JSON schema.
