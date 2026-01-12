# G4MF Mesh

## Overview

G4MF stores the visible geometry of objects inside of meshes. Each mesh is made of multiple surfaces, each of which may have a separate material. Mesh surfaces have vertices, and may contain edge indices, simplex cell indices, and more, each of which points to an accessor that encodes the data (see [G4MF Data Storage](../data.md)).

Meshes may be instanced by nodes in the scene hierarchy to provide visible geometry for those nodes. See [G4MF Node Mesh Instances](node_mesh_instance.md) for more information about mesh instances on nodes.

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

See [G4MF Skeleton Skinned Mesh Deformation](skeleton.md) for more information about skinning.

### Surfaces

The `"surfaces"` property is an array of objects, each of which defines a surface in the mesh. This property is required and has no default value.

Surfaces define the visible geometry of the mesh. They may be wireframe-only, may have simplex cells defined, or may have more complex geometry data defined. Each surface may have its own material. Surfaces are known as "Material Slots" in Unity and Blender, and are known as "Mesh Primitives" in glTF™.

All surfaces in a mesh share the same vertices, which are defined by the `"vertices"` property. This allows for deduplication of vertex data across surfaces. This also allows for mesh deforming operations such as skeletal skinning and blend shapes (morph targets) to operate on a single shared set of vertices.

### Vertices

The `"vertices"` property is an integer index that references an accessor containing the vertex data for this mesh. This property is required and has no default value.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor SHOULD be of a floating-point component type, and SHOULD have the `"vectorSize"` property set to the dimension of the model. Vertices may be used by surface edges, surface simplex cells (simplexes), surface extensions, mesh extensions, material extensions, physics shapes, and anything else that wishes to use them.

## Mesh Surface Properties

| Property              | Type      | Description                                                                             | Default            |
| --------------------- | --------- | --------------------------------------------------------------------------------------- | ------------------ |
| **simplexes**         | `integer` | The index of the accessor that contains the simplex indices for this surface.           | No simplexes       |
| **edges**             | `integer` | The index of the accessor that contains the edge indices for this surface.              | No edges           |
| **material**          | `integer` | The index of the material to use for this surface.                                      | No material        |
| **normals**           | `integer` | The index of the accessor that contains per-vertex-instance normals for this surface.   | Flat normals       |
| **polytopeSimplexes** | `boolean` | If `true`, allow importing the simplexes as complex polytopes instead of simplexes.     | `false`            |
| **textureMap**        | `integer` | The texture space coordinates of the surface's vertex instances (usually simplexes).    | No texture mapping |
| **topology**          | `object`  | Optional extended topology data for this surface.                                       | No topology data   |

### Simplexes

The `"simplexes"` property is an integer index that references an accessor containing the simplex cell indices for this surface. If not defined, the surface does not have explicit simplex cells, and may be a wireframe-only surface, or simplexes may be calculated from the `"topology"` data if needed (simplexes not explicitly defined in the G4MF file MUST NOT be used to determine vertex instances for normals, texture mapping, or other per-vertex data).

This property defines only ready-to-render simplex cell data. Each component in the accessor is an integer that refers to a vertex in the mesh's vertices accessor of the surface. The number of vertices per simplex is determined by the dimension of the model: 3D models have triangular simplex cells (3 vertices per simplex), 4D models have tetrahedral simplex cells (4 vertices per simplex), and so on. The only exception to this pattern is 2D models, which use triangular simplex cells. Simplexes are not defined for dimensions below 2. Optionally, multiple simplexes may be combined into larger star-shaped polytopes by setting the `"polytopeSimplexes"` property to `true`, enabling applications to treat multiple simplexes as part of the same polytope if needed without adding additional data.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an integer component type, and MUST have the `"vectorSize"` property set to the number of vertices per simplex cell as determined by the dimension of the model. Each primitive number component in the accessor is an index of a vertex in the mesh's vertices accessor, and each index MUST NOT exceed the bounds of the mesh's vertices accessor.

This property is not used to represent general hierarchical geometry. For example, in a 4D model, if two 3D simplexes share a 2D face, this simplex data does not contain information about this sharing, making it difficult to perform operations that require knowledge of the topological structure of the mesh, such as subdivision or smoothing. Such information could be reconstructed from these simplexes, but it would be computationally expensive to do so, and potentially lossy. For the purposes of interchange between DCC applications, consider defining the `"topology"` property in addition to the `"simplexes"` property, which allows for more complex hierarchical geometry data to be defined, and also defining boundary normals and seams. See [G4MF Mesh Topology](topology.md) for more information.

### Edges

The `"edges"` property is an integer index that references an accessor containing the edge indices for this surface. If not defined, the surface does not have explicit edges, but edges may be calculated from the simplexes if needed for visibility.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of an integer component type, and MUST have the `"vectorSize"` property set to 2. Each primitive number component in the accessor is an index of a vertex in the mesh's vertices accessor, and MUST NOT exceed the bounds of the mesh's vertices accessor. Every two primitive number components in the accessor form an edge, so the accessor MUST have an even number of components, as already enforced by the `"vectorSize"` property being set to 2.

### Material

The `"material"` property is an integer index that references a material in the document-level `"materials"` array. If not defined, the surface does not have a material.

This is a reference to a material in the G4MF file's document-level `"materials"` array. The material MUST be defined in the array, and the index MUST NOT exceed the bounds of the materials array. If not defined and not overridden by mesh instances, the surface does not have a material, and should be rendered with a default material.

See [G4MF Material](material.md) for more information about materials.

### Normals

The `"normals"` property is an integer index that references an accessor containing per-vertex-instance normals for this surface. If not defined, the surface has flat normals.

Normals can be used to define the surface's shading, such as smooth shading or flat shading. The default behavior is to use flat normals, meaning that all vertex instances in a simplex cell have the same normal as the simplex cell itself. See [Calculating Cell Normals](#calculating-cell-normals) for more information about how to calculate normals for simplex cells.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST be of a floating-point component type, and MUST have the `"vectorSize"` property set to the same value as the `"vectorSize"` of the mesh's vertices accessor. The amount of vectors in the accessor MUST be equal to the amount of vertex instances in the simplexes of this surface, which is the amount of component integers in the `"simplexes"` accessor. For example, for 3D meshes, this is the amount of triangular simplex cells multiplied by 3. For 4D meshes, this is the amount of tetrahedral simplex cells multiplied by 4, and so on. If the surface does not have simplexes, but has edges, then the amount of vectors in the accessor MUST be equal to the amount of component integers in the `"edges"` accessor, which is the amount of edges multiplied by 2. See [Vertex Instances](#vertex-instances) for more information about vertex instances, which are used by normals.

### Polytope Simplexes

The `"polytopeSimplexes"` property is a boolean that indicates if the `"simplexes"` should be imported as complex polytopes instead of individual simplexes. If not specified, the default is `false`.

If `true`, allow importing the simplex data as complex polytope cells instead of individual simplex cells. Each polytope is defined by a set of consecutive simplex cells that share the same starting vertex index. All simplexes belonging to the same polytope MUST have their vertices ordered such that computed simplex cell normals point in the same direction as each other, within the margin of floating-point precision errors.

For example, in 3D, a square polytope can be encoded as two triangular simplexes sharing the same starting vertex, and this flag marks those triangles as part of the square. Similarly, in 4D, a cube polytope can be encoded as set of 6 tetrahedral simplexes sharing the same starting vertex.

Applications may ignore this flag to always import as individual simplexes, or may read it to combine the simplexes into polytopes on import. To separate polytopes, choose a different starting vertex for each consecutive polytope, or duplicate the starting vertex to give it a new index.

Note: This only supports star-shaped polytopes with a simply connected topology where there exists a point on or within the polytope from which all vertices can be seen. See the Wikipedia article on star-shaped polygons: https://en.wikipedia.org/wiki/Star-shaped_polygon

### Texture Map

The `"textureMap"` property is an integer index that references an accessor containing the per-vertex-instance texture map data for the mesh surface's vertex instances. If not defined, the surface does not have per-vertex-instance texture mapping.

A texture map, also known as a UV map, UVW map, or texture coordinate map, is a mapping from the indices of the vertex instances to the texture space coordinates. Per vertex data applies to a surface's vertex instances, which depend on the surface's `"simplexes"` and `"edges"` properties. See [Vertex Instances](#vertex-instances) for more information on how vertex instances are defined.

The texture coordinates are usually on a range of 0.0 to 1.0. For 3D meshes, the texture coordinates usually refer to a 2D texture. For 4D meshes, the texture coordinates usually refer to a 3D texture. However, any dimension of texture coordinates is allowed. A 4D mesh may use a 2D texture, though this is discouraged and not very useful because it will look untextured from certain angles, or a 4D texture, mapping the 4D vertices in the same dimension as the texture coordinates. This property is intended to be used together with the `"texture"` property, but may be used without it, such as when defining a texture map for an untextured surface.

Texture map transforms, such as those supplied by `KHR_texture_transform` in glTF™, are not supported in G4MF. Instead, any texture transforms present in an application, such as scaling or translation, MUST be baked into the texture coordinates in the accessor when exporting the G4MF file. If dynamic texture transforms are required, such as for animation purposes, they may be defined by an extension, as long as the actual texture coordinates in the texture map properties have the current transforms baked in at export time.

This is a reference to an accessor in the G4MF file's document-level `"accessors"` array. The accessor MUST have a floating-point component type, and values are usually on a range of 0.0 to 1.0. The accessor MUST have its `"vectorSize"` property set to the dimension of the texture space. The amount of vector elements in the accessor MUST match or exceed the amount of vertex instances in the surface.

### Topology

The `"topology"` property is an object that contains optional extended topology data, which defines how the mesh surface is hierarchically structured in terms of its geometry and connectivity. If not defined, the surface does not have this data available.

See [G4MF Mesh Topology](topology.md) for more information about this property.

## Vertex Instances

Each mesh surface has a set of simplex vertex instances, implicitly defined how the surface's simplex properties use the vertices. Vertex instances may be used to define normal vectors, and may be used by materials to define per-vertex-instance data, such as colors or texture coordinates, for a mesh surface. Blender calls vertex instances "corners".

Mesh surface simplex vertex instances are defined as the following:

- If a mesh surface has the `"simplexes"` property defined, then the vertex instances are the usages of the vertices in the simplexes. For example, in a 4D model with tetrahedral simplex cells, each simplex cell has 4 vertex instances.
- If a mesh surface does not have the `"simplexes"` property defined, but does have the `"edges"` property defined, then the vertex instances are the usages of the vertices in the edges. Each edge always has 2 vertex instances, one for each end of the edge.
- If a mesh surface does not have the `"simplexes"` or `"edges"` properties defined, then the vertex instances are the mesh vertices themselves, allowing for point cloud materials to be used on meshes without any defined geometry.
- The `"topology"` property cannot be used to determine the vertex instances for a mesh surface's simplexes. Items inside `"topology"` have their own separate definition of topology vertex instances defined by boundary geometry items.
- Extensions may define other ways to determine the vertex instances for a mesh surface.

## Calculating Cell Normals

In 3D rendering, winding order is used to determine which side of a triangle is the front or back. This is then used to decide if the triangle should be rendered or culled. The typical convention in right-handed coordinate systems like with OpenGL™ and glTF™ is to use a counter-clockwise winding order for meshes whose global basis has a positive determinant, and a clockwise winding order for meshes whose global basis has a negative determinant.

For dimensions other than 3D, we need to generalize this concept. Instead of referring to a visual winding order, we need to define orientation mathematically. The 3D rule is generalized by calculating the vector from vertex 0 to vertex 1, and the vector from vertex 0 to vertex 2, then taking the cross product of those two vectors. The resulting vector can have the dot product calculated with the camera's local Z axis to determine if the triangle is facing the camera or not. For meshes attacehed to nodes with positive determinant transforms, the resulting vector should point towards the viewer in the same direction as the camera's local Z axis, and for negative determinants, the resulting vector should point away from the viewer in the opposite direction as the camera's local Z axis.

To generalize this to 4D, we need three vectors. For a simplex cell, use the vectors from vertex 0 to vertex 1, from vertex 0 to vertex 2, and from vertex 0 to vertex 3. Then we need to pass these vectors into a function that returns a unique 4D vector that is perpendicular to all three of them. More generally, for N dimensions, we get N-1 vectors from vertex 0 to vertex N, then pass them into a function that returns a unique N-dimensional vector that is perpendicular to all of them. This is then used to calculate a dot product with the camera's local Z axis in the same way as in 3D (camera forward in G4MF is defined as -Z, like glTF™).

To calculate the perpendicular vector, you may use the functions defined in the [Calculating Perpendicular Vectors section of the G4MF Math specification](../math.md#calculating-perpendicular-vectors).

It is recommended to pre-compute the simplex cell normals before rendering and store them in memory, since calculating them can be expensive, especially for higher dimensions. However, since this information is recoverable from the simplexes, it would be redundant to store in G4MF.

For non-simplex polytope cells such as those defined in the `"topology"` property, the same calculation method applies, with the vertices sourced from boundary geometry items. However, the order of the vertices used to calculate the vectors is determined in a more complex way. See [G4MF Mesh Topology](topology.md) for more information about how to determine the order of vertices for boundary geometry items.

## JSON Schema

- See [g4mf.mesh.schema.json](../../schema/mesh/g4mf.mesh.schema.json) for the mesh properties JSON schema.
- See [g4mf.mesh.surface.schema.json](../../schema/mesh/g4mf.mesh.surface.schema.json) for the mesh surface properties JSON schema.
