# G4MF Mesh

## Overview

G4MF stores the visible geometry of objects inside of meshes. Each mesh is made of multiple surfaces, each of which may have a separate material. Mesh surfaces have vertices, and may contain edge indices, cell indices, and more, each of which points to an accessor that encodes the data (see [G4MF Data](data.md)).

## Example

The following example defines.

## Mesh Properties

| Property     | Type       | Description                                                            | Default               |
| ------------ | ---------- | ---------------------------------------------------------------------- | --------------------- |
| **blend**    | `object`   | An object that defines the blend shape morph targets for this mesh.    | No blend shapes       |
| **skin**     | `object`   | An object that defines the skinning information used for skeletons.    | No skinning           |
| **surfaces** | `object[]` | An array of surfaces that make up the mesh.                            | Required, no default. |
| **vertices** | `integer`  | The index of the accessor that contains the vertex data for this mesh. | Required, no default. |

### Blend

The `"blend"` property is an object that defines the blend shape morph targets for this mesh. This property is optional and defaults to no blend shapes.

See [G4MF Blend Shape Mesh Deformation](blend.md) for more information about blend shapes.

### Skin

The `"skin"` property is an object that defines the skinning information used for skeletons. This property is optional and defaults to no skinning.

See [G4MF Skinning Mesh Deformation](skin.md) for more information about skinning.

### Surfaces

The `"surfaces"` property is an array of objects, each of which defines a surface in the mesh. This property is required and has no default value.

Surfaces define the visible geometry of the mesh. They may be wireframe-only, may have cells defined, or may have more complex geometry data defined. Each surface may have its own material.

All surfaces in a mesh share the same vertices, which are defined by the `"vertices"` property. This allows for deduplication of vertex data across surfaces. This also allows for mesh deforming operations such as skeletal skinning and blend shapes (morph targets) to operate on a single shared set of vertices.

### Vertices

The `"vertices"` property is an integer index that references an accessor containing the vertex data for this mesh. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor SHOULD be of a floating-point primitive type, and SHOULD have the `"vectorSize"` property set to the dimension of the model. Vertices may be used by surface edges, cells, geometry, surface extensions, mesh extensions, and anything else that wishes to use them.

## Mesh Surface Properties

| Property          | Type      | Description                                                                           | Default            |
| ----------------- | --------- | ------------------------------------------------------------------------------------- | ------------------ |
| **cells**         | `integer` | The index of the accessor that contains the cell indices for this surface.            | No cells           |
| **edges**         | `integer` | The index of the accessor that contains the edge indices for this surface.            | No edges           |
| **material**      | `integer` | The index of the material to use for this surface.                                    | No material        |
| **normals**       | `integer` | The index of the accessor that contains per-vertex-instance normals for this surface. | Flat normals       |
| **polytopeCells** | `boolean` | If `true`, allow importing the cells as complex polytopes instead of simplexes.       | `false`            |
| **textureMap**    | `integer` | The texture space coordinates of the surface's vertex instances (usually cells).      | No texture mapping |
| **topology**      | `object`  | Optional extended topology data for this surface.                                     | No topology data   |

### Cells

The `"cells"` property is an integer index that references an accessor containing the cell indices for this surface. If not defined, the surface does not have explicit cells, and may be a wireframe-only surface, or cells may be calculated from the `"topology"` data if needed (cells not explicitly defined in the G4MF file MUST NOT be used to determine vertex instances for normals, texture mapping, or other per-vertex data).

This property defines only ready-to-render simplex cells. Each primitive number in the array refers to a vertex in the mesh's vertices array of the surface. The number of vertices per cell is determined by the dimension of the model: 3D models have triangular cells (3 vertices per cell), 4D models have tetrahedral cells (4 vertices per cell), and so on. The only exception to this pattern is 2D models, which use triangular cells. Cells are not defined for dimensions below 2. Optionally, multiple simplex cells may be combined into larger star-shaped polytopes by setting the `"polytopeCells"` property to `true`, enabling applications to treat these cells as part of the same polytope if needed without adding additional data.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an integer primitive type, and MUST have the `"vectorSize"` property set to the number of vertices in a cell as determined by the dimension of the model. Each primitive number in the array is an index of a vertex in the mesh's vertices array, and each item MUST NOT exceed the bounds of the mesh's vertices array.

This property is not used to represent general hierarchical geometry. For example, in a 4D model, if two 3D cells share a 2D face, this array of cells does not contain information about this sharing, making it difficult to perform operations that require knowledge of the topological structure of the mesh, such as subdivision or smoothing. Such information could be reconstructed from these cells, but it would be computationally expensive to do so, and potentially lossy. For the purposes of interchange between DCC applications, consider defining the `"topology"` property in addition to the `"cells"` property, which allows for more complex hierarchical geometry data to be defined, and also defining boundary normals and seams. See [G4MF Mesh Topology](topology.md) for more information.

### Edges

The `"edges"` property is an integer index that references an accessor containing the edge indices for this surface. If not defined, the surface does not have explicit edges, but edges may be calculated from the cells if needed for visibility.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an integer primitive type, and MUST have the `"vectorSize"` property set to 2. Each primitive number in the array is an index of a vertex in the mesh's vertices array, and MUST NOT exceed the bounds of the mesh's vertices array. Every two primitive numbers in the array form an edge, so the array MUST have an even number of primitives.

### Material

The `"material"` property is an integer index that references a material in the document-level `"materials"` array. If not defined, the surface does not have a material.

This is a reference to a material in the G4MF file's document-level `"materials"` array. The material MUST be defined in the array, and the index MUST NOT exceed the bounds of the materials array. If not defined, the surface does not have a material, and should be rendered with a default material.

See [G4MF Material](material.md) for more information about materials.

### Normals

The `"normals"` property is an integer index that references an accessor containing per-vertex-instance normals for this surface. If not defined, the surface has flat normals.

Normals can be used to define the surface's shading, such as smooth shading or flat shading. The default behavior is to use flat normals, meaning that all vertex instances in a cell have the same normal as the cell itself. See [Calculating Cell Normals](#calculating-cell-normals) for more information about how to calculate normals for cells.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of a floating-point primitive type, and MUST have the `"vectorSize"` property set to the same value as the `"vectorSize"` of the mesh's vertices accessor. The amount of vectors in the accessor MUST be equal to the amount of vertex instances in the cells of this surface, which is the amount of primitive numbers in the `"cells"` accessor. For example, for 3D meshes, this is the amount of triangular cells multiplied by 3. For 4D meshes, this is the amount of tetrahedral cells multiplied by 4, and so on. If the surface does not have cells, but has edges, then the amount of vectors in the accessor MUST be equal to the amount of primitive numbers in the `"edges"` accessor, which is the amount of edges multiplied by 2. See [Vertex Instances](#vertex-instances) for more information about vertex instances, which are used by normals.

### Polytope Cells

The `"polytopeCells"` property is a boolean that indicates if cells should be imported as complex polytopes instead of simplexes. If not specified, the default is `false`.

If `true`, allow importing the cells as complex polytopes instead of simplexes. Each polytope is defined by a set of consecutive cells that share the same starting vertex. For example, in 3D a square polytope can be encoded as two triangle cells sharing the same starting vertex, and this flag marks those triangles as part of the square. Similarly, in 4D, a cube polytope can be encoded as set of 6 tetrahedral cells sharing the same starting vertex. Applications may ignore this flag to always import as simplexes, or use it to combine the cells as polytopes. To separate polytopes, choose a different starting vertex for each polytope.

Note: This only supports star-shaped polytopes with a simply connected topology where there exists a point on or within the polytope from which all vertices can be seen. See the Wikipedia article on star-shaped polygons: https://en.wikipedia.org/wiki/Star-shaped_polygon

### Texture Map

The `"textureMap"` property is an integer index that references an accessor containing the per-vertex-instance texture map data for the mesh surface's vertex instances. If not defined, the surface does not have per-vertex-instance texture mapping.

A texture map, also known as a UV map, UVW map, or texture coordinate map, is a mapping from the indices of the vertex instances to the texture space coordinates. Per vertex data applies to a surface's vertex instances, which depend on the surface's `"cells"` and `"edges"` properties. See [Vertex Instances](#vertex-instances) for more information on how vertex instances are defined.

The texture coordinates are usually on a range of 0.0 to 1.0. For 3D meshes, the texture coordinates usually refer to a 2D texture. For 4D meshes, the texture coordinates usually refer to a 3D texture. However, any dimension of texture coordinates is allowed. A 4D mesh may use a 2D texture, though this is discouraged and not very useful because it will look untextured from certain angles, or a 4D texture, mapping the 4D vertices in the same dimension as the texture coordinates. This property is intended to be used together with the `"texture"` property, but may be used without it, such as when defining a texture map for an untextured surface.

Texture map transforms, such as those supplied by `KHR_texture_transform` in glTF™, are not supported in G4MF. Instead, any texture transforms present in an application, such as scaling or translation, MUST be baked into the texture coordinates in the accessor when exporting the G4MF file. If dynamic texture transforms are required, such as for animation purposes, they may be defined by an extension, as long as the actual texture coordinates in the texture map properties have the current transforms baked in at export time.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point primitive type, and values are usually on a range of 0.0 to 1.0. The accessor MUST have its `"vectorSize"` property set to the dimension of the texture space. The amount of vector elements in the accessor MUST match or exceed the amount of vertex instances in the surface.

### Topology

The `"topology"` property is an object that contains optional extended topology data, which defines how the mesh surface is hierarchically structured in terms of its geometry and connectivity. If not defined, the surface does not have this data available.

See [G4MF Mesh Topology](topology.md) for more information about this property.

## Vertex Instances

Each mesh surface has a set of simplex vertex instances, implicitly defined how the surface's simplex properties use the vertices. Vertex instances may be used to define normal vectors, and may be used by materials to define per-vertex-instance data, such as colors or texture coordinates, for a mesh surface.

Mesh surface simplex vertex instances are defined as the following:

- If a mesh surface has the `"cells"` property defined, then the vertex instances are the usages of the vertices in the cells. For example, in a 4D model with tetarhedral cells, each cell has 4 vertex instances.
- If a mesh surface does not have the `"cells"` property defined, but does have the `"edges"` property defined, then the vertex instances are the usages of the vertices in the edges. Each edge always has 2 vertex instances, one for each end of the edge.
- If a mesh surface does not have the `"cells"` or `"edges"` properties defined, then the vertex instances are the mesh vertices themselves, allowing for point cloud materials.
- The `"topology"` property cannot be used to determine the vertex instances for a mesh surface's simplexes. Items inside `"topology"` have their own separate definition of topology vertex instances defined by boundary geometry items.
- Extensions may define other ways to determine the vertex instances for a mesh surface.

## Calculating Cell Normals

In 3D rendering, winding order is used to determine which side of a triangle is the front or back. This is then used to decide if the triangle should be rendered or culled. The typical convention in right-handed coordinate systems like with OpenGL™ and glTF™ is to use a counter-clockwise winding order for meshes whose global basis has a positive determinant, and a clockwise winding order for meshes whose global basis has a negative determinant.

For dimensions other than 3D, we need to generalize this concept. Instead of referring to a visual winding order, we need to define orientation mathematically. The 3D rule is generalized by calculating the vector from vertex 0 to vertex 1, and the vector from vertex 0 to vertex 2, then taking the cross product of those two vectors. The resulting vector can have the dot product calculated with the camera's local Z axis to determine if the triangle is facing the camera or not. For meshes with positive determinants, the resulting vector should point towards the viewer in the same direction as the camera's local Z axis, and for meshes with negative determinants, the resulting vector should point away from the viewer in the opposite direction as the camera's local Z axis.

To generalize this to 4D, we need three vectors, from vertex 0 to vertex 1, from vertex 0 to vertex 2, and from vertex 0 to vertex 3. Then we need to pass these vectors into a function that returns a unique 4D vector that is perpendicular to all three of them. More generally, for N dimensions, we get N-1 vectors from vertex 0 to vertex N, then pass them into a function that returns a unique N-dimensional vector that is perpendicular to all of them. This is then used to calculate a dot product with the camera's local Z axis in the same way as in 3D (camera forward in G4MF is defined as -Z, like glTF™).

To calculate the perpendicular vector, you may use the functions defined in the [Calculating Perpendicular Vectors section of the G4MF Math specification](math.md#calculating-perpendicular-vectors).

It is recommended to pre-compute the cell normals before rendering and store them in memory, since calculating them can be expensive, especially for higher dimensions. However, since this information is recoverable from the cells, it would be redundant to store in G4MF.

## JSON Schema

- See [g4mf.mesh.schema.json](../../schema/mesh/g4mf.mesh.schema.json) for the mesh properties JSON schema.
- See [g4mf.mesh.surface.schema.json](../../schema/mesh/g4mf.mesh.surface.schema.json) for the mesh surface properties JSON schema.
