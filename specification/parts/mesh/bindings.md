# G4MF Mesh Surface Bindings

## Overview

Mesh surface bindings define how data is associated with mesh elements such as vertices, edges, and simplexes. For example, the tetrahedra of a 4D mesh surface may have texture map coordinates, normals, colors, or other data associated with each corner of the tetrahedra.

Bindings define an array of data stored in `"values"`. This array is then sampled by indices corresponding to specific mesh elements. For example, the `"simplexes"` property allows associating data with each corner of the simplex cells, the `"perSimplex"` property allows associating one value per entire simplex cell, the `"vertices"` property allows associating data with the shared vertices of the mesh, `"geometry"` allows associating data with polytope elements or their decompositions, and so on. The binding may contain any combination of these index properties, including one or multiple at once. Having none of them would be useless, but this is allowed, in case an extension defines another way to index into the values.

## Example

The following example defines.

## Mesh Surface Binding Properties

| Property       | Type       | Description                                                                            | Default                 |
| -------------- | ---------- | -------------------------------------------------------------------------------------- | ----------------------- |
| **edges**      | `integer`  | The index of the accessor for edge indices into the binding's values.                  | No edge indices.        |
| **geometry**   | `object[]` | An array of geometry decomposition objects for associating values with geometry items. | No geometry indices.    |
| **perEdge**    | `integer`  | The index of the accessor for per-edge indices into the binding's values.              | No per-edge indices.    |
| **perSimplex** | `integer`  | The index of the accessor for per-simplex indices into the binding's values.           | No per-simplex indices. |
| **simplexes**  | `integer`  | The index of the accessor for simplex indices into the binding's values.               | No simplex indices.     |
| **values**     | `integer`  | The index of the accessor that contains the values associated with this binding.       | Required, no default.   |
| **vertices**   | `integer`  | The index of the accessor for vertex indices into the binding's values.                | No vertex indices.      |

### Edges

The `"edges"` property is an integer index that references an accessor containing the bindings corresponding to edge indices for this surface. If not defined, the surface does not have explicit edges, but edges may be calculated from the simplexes if needed for visibility.

### Geometry

The `"geometry"` property is an array of geometry decomposition objects that define how binding values are associated with specific geometry's decomposed polytope elements of the mesh surface. Usually, this will have one item referring to the corners (vertices) of boundary geometry items, meaning for a 3D mesh surface, `index` will be set to 0 (the 2D faces), and for a 4D mesh surface, `index` will be set to 1 (the 3D cells).

For more information, see [Geometry Decomposition](#geometry-decomposition) below.

### Per Edge

The `"perEdge"` property is an integer index that references an accessor containing the bindings corresponding to each edge of the mesh surface. If not defined, the surface does not have per-edge bindings.

### Per Simplex

The `"perSimplex"` property is an integer index that references an accessor containing the bindings corresponding to each simplex cell of the mesh surface. If not defined, the surface does not have per-simplex bindings.

### Simplexes

The `"simplexes"` property is an integer index that references an accessor containing the bindings corresponding to the simplexes of the mesh surface. If not defined, the surface does not have simplex bindings.

### Values

The `"values"` property is an integer index that references an accessor containing the values associated with this binding. This property is required and has no default value.

The type and structure of the values depend on the specific use case of the binding. For example, the texture mapping of a 3D mesh surface would typically use a floating-point accessor with a `vectorSize` of 2 or 3, the texture mapping of a 4D mesh surface would typically use a floating-point accessor with a `vectorSize` of 3 or 4, the vertex normals of a 5D mesh would use a floating-point accessor with a `vectorSize` of 5, and so on.

### Vertices

The `"vertices"` property is an integer index that references an accessor containing the bindings corresponding to the vertices shared between all mesh surfaces. If not defined, the surface does not have per-vertex bindings.

## Geometry Decomposition

The geometry decomposition objects in the `"geometry"` property define how binding values are associated with specific geometry's decomposed polytope elements.

| Property      | Type      | Description                                                                    | Default               |
| ------------- | --------- | ------------------------------------------------------------------------------ | --------------------- |
| **accessor**  | `integer` | The index of the accessor that contains indices into this binding's values.    | Required, no default. |
| **dimension** | `integer` | The dimensional level to decompose to. MUST NOT be greater than `index` + 2.   | `0` (0D vertices)     |
| **index**     | `integer` | The index into the mesh surface's geometry array that this binding references. | Required, no default. |

### Accessor

The `"accessor"` property is an integer index that references an accessor containing indices into this binding's values. Each element corresponds to a decomposed element at the specified dimension. This property is required and has no default value.

### Dimension

The `"dimension"` property is an integer that defines the dimensional level to decompose to. This property is optional and defaults to 0.

When dimension is set to 0, this means to decompose down to vertices (corners), and each item in the accessor corresponds to a corner of the geometry item. When dimension is set to 1, this means to decompose down to edges, and each item in the accessor corresponds to an edge of the geometry item. When dimension is set to 2, this means to decompose down to polygons, and each item in the accessor corresponds to a polygon of the geometry item, and so on.

The value MUST NOT be greater than `index` + 2, because a geometry item at index N has dimension N+2, and it cannot be decomposed into elements of higher dimension than itself. For example, a 3D polyhedron (geometry index 1, dimension 3) can be decomposed into vertices (0), edges (1), polygons (2), or itself (3), but not into 4D polytopes. In other words, a cube contains vertices, edges, faces, and one volume (itself), but zero hypercubes or beyond.

For example, to store per-corner data for 3D mesh faces (geometry index 0), set `"index"` to 0 and `"dimension"` to 0. To store one value per entire face, set `"index"` to 0 and `"dimension"` to 2.

### Index

The `"index"` property is an integer that defines the index into the mesh surface's geometry array that this binding references. This property is required and has no default value.

For example, if binding data to the corners of polygons, such as the boundary of a 3D mesh surface or the volume of a 2D mesh interior, `index` would be set to 0. If binding data to the corners of polyhedra, such as the boundary of a 4D mesh surface or the volume of a 3D mesh interior, `index` would be set to 1. If binding data to the corners of 4D polytopes, such as the boundary of a 5D mesh surface or the volume of a 4D mesh interior, `index` would be set to 2, and so on.

## JSON Schema

- See [g4mf.mesh.surface.binding.schema.json](../../schema/mesh/g4mf.mesh.surface.binding.schema.json) for the mesh surface binding properties JSON schema.
- See [g4mf.mesh.surface.binding.geometry.schema.json](../../schema/mesh/g4mf.mesh.surface.binding.geometry.schema.json) for the geometry decomposition properties JSON schema.
