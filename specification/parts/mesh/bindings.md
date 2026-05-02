# G4MF Mesh Surface Bindings

## Overview

Mesh surface bindings define how data is associated with mesh elements such as vertices, edges, and simplexes. For example, the tetrahedra of a 4D mesh surface may have texture map coordinates, normals, colors, or other data associated with each corner of the tetrahedra.

Bindings define an array of data stored in `"values"`. This array is then sampled by indices corresponding to specific mesh elements. For example, the `"simplexes"` property allows associating data with each corner of the simplex cells, the `"perSimplex"` property allows associating one value per entire simplex cell, the `"geometry"` property allows associating data with polytope elements or their decompositions, and so on. The binding may contain any combination of these index properties, including one or multiple at once. Having none of them would be useless, but this is allowed, in case an extension defines another way to index into the values.

## Example

The following example defines.

## Mesh Surface Binding Properties

| Property       | Type       | Description                                                                            | Default                 |
| -------------- | ---------- | -------------------------------------------------------------------------------------- | ----------------------- |
| **geometry**   | `object[]` | An array of geometry decomposition objects for associating values with geometry items. | No geometry indices.    |
| **perSimplex** | `integer`  | The index of the accessor for per-simplex indices into the binding's values.           | No per-simplex indices. |
| **simplexes**  | `integer`  | The index of the accessor for simplex indices into the binding's values.               | No simplex indices.     |
| **values**     | `integer`  | The index of the accessor that contains the values associated with this binding.       | Required, no default.   |

### Geometry

The `"geometry"` property is an array of geometry decomposition objects that define how binding values are associated with specific geometry's decomposed polytope elements of the mesh surface. For simplex-only meshes, this will usually not be defined. For polytope meshes, this will usually have one item referring to vertex instances of boundary geometry items, meaning for the 2D surface of a 3D mesh, `"geometryDimension"` will be set to 2 (the 2D faces), and for the 3D surface of a 4D mesh, `"geometryDimension"` will be set to 3 (the 3D cells).

For more information, see [Geometry Binding Properties](#geometry-binding-properties) below.

### Per Simplex

The `"perSimplex"` property is an integer index that references an accessor containing the bindings corresponding to each simplex cell of the mesh surface. If not defined, the surface does not have per-simplex bindings.

### Simplexes

The `"simplexes"` property is an integer index that references an accessor containing the bindings corresponding to the simplexes of the mesh surface. If not defined, the surface does not have simplex bindings.

### Values

The `"values"` property is an integer index that references an accessor containing the values associated with this binding. This property is required and has no default value.

The type and structure of the values depend on the specific use case of the binding. For example, the texture mapping of a 3D mesh surface would typically use a floating-point accessor with a `vectorSize` of 2 or 3, the texture mapping of a 4D mesh surface would typically use a floating-point accessor with a `vectorSize` of 3 or 4, the vertex normals of a 5D mesh would use a floating-point accessor with a `vectorSize` of 5, and so on.

## Geometry Binding Properties

The geometry bindings objects in the `"geometry"` property define how binding values are associated with specific geometry's polytope elements, decomposed into specific levels.

| Property               | Type      | Description                                                                          | Default               |
| ---------------------- | --------- | ------------------------------------------------------------------------------------ | --------------------- |
| **accessor**           | `integer` | The index of the accessor that contains indices into this binding's values.          | Required, no default. |
| **decomposeDimension** | `integer` | The dimensional level to decompose to. MUST NOT be greater than `geometryDimension`. | `0` (0D vertices)     |
| **geometryDimension**  | `integer` | The dimensional level into the mesh surface's geometry that this binding references. | Required, no default. |

### Accessor

The `"accessor"` property is an integer index that references an accessor containing indices into this binding's values. This property is required and has no default value.

The data in this accessor is structured in the following ways:

- Geometry bindings that are not decomposed, meaning `"decomposeDimension"` is equal to `geometryDimension`, are stored as a dense array of indices, where each index corresponds to a geometry item of the specified geometry dimension. There is no need to store an amount of members, because it is always 1.
- Geometry bindings referring to vertices of edges, meaning `"decomposeDimension"` is 0 and `"geometryDimension"` is 1, are stored as a dense array of indices, where every 2 indices correspond to the 2 vertices of each edge geometry item. There is no need to store an amount of members, because it is always 2.
- In all other cases, geometry binding accessor indices behave the same as the mesh surface's geometry items. Meaning, the first number is the amount of members in the first cell, followed by those members, then the amount of members in the second cell, followed by those members, and so on.
  - The amounts are technically redundant in that they can be reproduced from the geometry items, but this structure allows for much more efficient loading, and guards against malformed data.

The non-amount members of the arrays are indices into the binding's values, and each element corresponds to a decomposed element. See below for the details of the geometry decomposition.

### Decompose Dimension

The `"decomposeDimension"` property is an integer that defines the dimensional level to decompose to. This property is optional and defaults to 0.

When decompose dimension is set to 0, this means to decompose down to vertices (corners), and each item in the accessor corresponds to a corner of the geometry item. When decompose is set to 1, this means to decompose down to edges, and each item in the accessor corresponds to an edge of the geometry item. When decompose is set to 2, this means to decompose down to polygons, and each item in the accessor corresponds to a polygon of the geometry item, and so on.

The value MUST NOT be greater than `geometryDimension`, because a geometry item cannot be decomposed into elements of higher dimension than itself. For example, a 3D polyhedron (geometry dimension 3) can be decomposed into vertices (0), edges (1), polygons (2), or itself (3), but not into 4D polytopes. In other words, a cube contains vertices, edges, faces, and one volume (itself), but zero hypercubes or beyond.

For example, to store data for the corners of 2D faces of a 3D mesh, set `"geometryDimension"` to 2 and `"decomposeDimension"` to 0. To store one value per entire face, set `"geometryDimension"` to 2 and `"decomposeDimension"` to 2. For more detailed examples of geometry decomposition, see below.

### Geometry Dimension

The `"geometryDimension"` property is an integer that defines the dimension of geometry elements that this binding references. This property is required and has no default value.

This value may be 0 for vertices, 1 for edges, 2 for polygons, 3 for cells, 4 for hypervolumes, and so on. The `"geometryDimension"` MUST NOT be less than `"decomposeDimension"`, it must be greater than or equal to `"decomposeDimension"`. A geometry dimension of 2 or greater means this binding will bind to elements based on the mesh surface's geometry array at an index of this minus 2. A geometry dimension of 0 means this binding will bind to mesh vertices, and a geometry dimension of 1 means this binding will bind to mesh edges.

For example, if binding data to polygons, such as the boundary of a 3D mesh surface or the volume of a 2D mesh interior, `geometryDimension` would be set to 2. If binding data to polyhedra, such as the boundary of a 4D mesh surface or the volume of a 3D mesh interior, `geometryDimension` would be set to 3. If binding data to 4D polytopes, such as the boundary of a 5D mesh surface or the volume of a 4D mesh interior, `geometryDimension` would be set to 4, and so on. For more detailed examples of geometry decomposition, see below.

### Geometry Decomposition Examples

The combination of the `"geometryDimension"` and `"decomposeDimension"` properties define the specific geometry elements that the binding values are associated with. The `"decomposeDimension"` property MUST be less than or equal to the `"geometryDimension"` property, because you cannot decompose into elements of higher dimension than the geometry items themselves. For example:

- When `"geometryDimension"` is 0, the binding is based on 0D vertices.
  - The `"decomposeDimension"` property can only be 0, meaning the binding is per vertex.
- When `"geometryDimension"` is 1, the binding is based on 1D edges.
  - When `"decomposeDimension"` is 0, the binding is based on the vertices of those edges.
  - When `"decomposeDimension"` is 1, the binding is based on one value for each entire edge.
- When `"geometryDimension"` is 2, the binding is based on 2D faces.
  - When `"decomposeDimension"` is 0, the binding is based on the vertices of those faces.
  - When `"decomposeDimension"` is 1, the binding is based on the edges of those faces.
  - When `"decomposeDimension"` is 2, the binding is based on one value for each entire face.
- When `"geometryDimension"` is 3, the binding is based on 3D cells.
  - When `"decomposeDimension"` is 0, the binding is based on the vertices of those cells.
  - When `"decomposeDimension"` is 1, the binding is based on the edges of those cells.
  - When `"decomposeDimension"` is 2, the binding is based on the faces of those cells.
  - When `"decomposeDimension"` is 3, the binding is based on one value for each entire cell.
- When `"geometryDimension"` is 4, the binding is based on 4D hypervolumes.
  - When `"decomposeDimension"` is 0, the binding is based on the vertices of those hypervolumes.
  - When `"decomposeDimension"` is 1, the binding is based on the edges of those hypervolumes.
  - When `"decomposeDimension"` is 2, the binding is based on the faces of those hypervolumes.
  - When `"decomposeDimension"` is 3, the binding is based on the cells of those hypervolumes.
  - When `"decomposeDimension"` is 4, the binding is based on one value for each entire hypervolume.
- And so on for higher dimensions, where the decomposition dimension can be set anywhere from 0 to the geometry dimension, inclusive.

Note that these refer to the hierarchical geometry structure of the mesh surface. For example, with a 4D mesh, a `"geometryDimension"` of 3 refers to the polytope cells of the mesh surface geometry, NOT the simplexes. The data for simplexes is instead stored in separate accessors of the [main binding object](#mesh-surface-binding-properties), which can be [`"simplexes"`](#simplexes) for per-corner data, and/or [`"perSimplex"`](#per-simplex) for per-simplex data.

## JSON Schema

- See [g4mf.mesh.surface.binding.schema.json](../../schema/mesh/g4mf.mesh.surface.binding.schema.json) for the mesh surface binding properties JSON schema.
- See [g4mf.mesh.surface.binding.geometry.schema.json](../../schema/mesh/g4mf.mesh.surface.binding.geometry.schema.json) for the geometry decomposition properties JSON schema.
