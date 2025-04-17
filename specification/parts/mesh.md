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
| **cellNormals**   | `integer` | The index of the accessor that contains the per-cell normal data for this surface. | No cell normals.      |
| **edges**         | `integer` | The index of the accessor that contains the edge indices for this surface.         | No edges.             |
| **polytopeCells** | `boolean` | If `true`, allow importing the cells as complex polytopes instead of simplexes.    | `false`               |
| **vertices**      | `integer` | The index of the accessor that contains the vertex data for this surface.          | Required, no default. |

### Cells

The `"cells"` property is an integer index that references an accessor containing the cell indices for this surface. If not defined, the surface does not have explicit cells, and may be a wireframe-only surface.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an integer primitive type, and MUST have the `"vectorSize"` property set to the number of vertices in a cell as determined by the dimension of the model: 3D models have triangular cells (3 vertices per cell), 4D models have tetrahedral cells (4 vertices per cell), and so on. Each primitive number in the array is an index of a vertex in the vertices array, and MUST NOT exceed the bounds of the vertices array.

### Cell Normals

The `"cellNormals"` property is an integer index that references an accessor containing the per-cell normal data for this surface. If not defined, the surface does not have explicitly defined normals.

These are per-cell normals, which may be used for backface culling and flat shading, unlike vertex normals. This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor SHOULD be of a floating-point primitive type, and MUST have the `"vectorSize"` property set to the dimension of the model. Each normal is an N-dimensional vector, where N is the dimension of the model. If defined, the amount of normal vectors in the array MUST match the amount of cells in the cells array.

### Edges

The `"edges"` property is an integer index that references an accessor containing the edge indices for this surface. If not defined, the surface does not have explicit edges, but edges may be calculated from the cells if needed.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an integer primitive type, and MUST have the `"vectorSize"` property set to 2. Each primitive number in the array is an index of a vertex in the vertices array, and MUST NOT exceed the bounds of the vertices array. Every two primitive numbers in the array form an edge, so the array MUST have an even number of primitives.

### Polytope Cells

The `"polytopeCells"` property is a boolean that indicates if cells should be imported as complex polytopes instead of simplexes. If not specified, the default is `false`.

If `true`, allow importing the cells as complex polytopes instead of simplexes. Each polytope is defined by a set of consecutive cells that share the same starting vertex. For example, in 3D a square polytope can be encoded as two triangle cells sharing the same starting vertex, and this flag marks those triangles as part of the square. Similarly, in 4D, a cube polytope can be encoded as set of 6 tetrahedral cells sharing the same starting vertex. Applications may ignore this flag to always import as simplexes, or use it to combine the cells as polytopes. To separate polytopes, choose a different starting vertex for each polytope.

Note: This only supports shar-shaped polytopes with a simply connected topology where there exists a point on or within the polytope from which all vertices can be seen. See the Wikipedia article on star-shaped polygons: https://en.wikipedia.org/wiki/Star-shaped_polygon

### Vertices

The `"vertices"` property is an integer index that references an accessor containing the vertex data for this surface. This property is required.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor SHOULD be of a floating-point primitive type, and MUST have the `"vectorSize"` property set to the dimension of the model. Vertices may be used by edges, cells, and anything else that wishes to use them.
