# Good 4D Model Format (G4MF) Specification

## Summary

Good 4D Model Format, or G4MF for short, is a JSON-based 4D-focused multi-dimensional model format inspired by Khronos's [glTF™](https://github.com/KhronosGroup/glTF), allowing for transmission, interchange, and interoperability of higher dimensional content between applications.

## Properties

The top-level G4MF document defines the following properties:

| Property        | Type       | Description                                                                     | Default               |
| --------------- | ---------- | ------------------------------------------------------------------------------- | --------------------- |
| **asset**       | `object`   | The asset header, which contains metadata about the file.                       | Required, no default. |
| **accessors**   | `object[]` | An array of accessors, which provide a typed view of the data in a buffer view. | `[]` (empty array)    |
| **buffers**     | `object[]` | An array of buffers, which contain raw binary data.                             | `[]` (empty array)    |
| **bufferViews** | `object[]` | An array of buffer views, which define slices of buffers.                       | `[]` (empty array)    |
| **lights**      | `object[]` | An array of lights, which can be attached to nodes to add lights to the model.  | `[]` (empty array)    |
| **materials**   | `object[]` | An array of materials, which define the appearance of surfaces.                 | `[]` (empty array)    |
| **meshes**      | `object[]` | An array of meshes, which define the geometry of objects.                       | `[]` (empty array)    |
| **nodes**       | `object[]` | An array of nodes, which define the hierarchy of the scene.                     | `[]` (empty array)    |
| **shapes**      | `object[]` | An array of shapes, which define mathematical shapes used for physics.          | `[]` (empty array)    |
| **textures**    | `object[]` | An array of textures, which provide visual data for materials.                  | `[]` (empty array)    |

The details of how these properties work are described in the below sections.

In addition to these properties, all G4MF objects, including the top-level G4MF document, MAY contain `"extensions"`, `"extras"`, and `"name"` properties.

## Asset Header

At a minimum, the G4MF JSON data MUST contain `"asset"` with `"dimension"` defining the dimension of the model. This example defines an empty 4D G4MF file:

```json
{
	"asset": {
		"dimension": 4
	}
}
```

If `"dimension"` is not defined or is not an integer, the file is not a valid G4MF file. The G4MF format is designed to be extensible as an N-dimensional format, but most of the use cases and documentation will focus on 4D files. Implementations MAY only support any subset of dimensions, such as only 4D, only 5D, or even only 3D. Implementations MAY choose to entirely ignore files with unsupported dimensions, or read them discarding the unsupported dimensions.

For convenience, the details of the asset header are in a separate file: [G4MF Asset](parts/asset.md).

## Scene Hierarchy

The core building block of a G4MF scene is a hierarchy of zero or more nodes. Each node defines an object in the scene with a transform, and defines child nodes that are attached to it.

The node at index 0 is the root node. All other nodes in the file are either descendants of the root node, or are not used. Nodes not used in the core scene hierarchy MAY be used by extensions. G4MF files may also contain zero nodes, in which case the file is not a scene, but a collection of data, such as a 4D mesh.

For convenience, the details of how nodes work are described in a separate file: [G4MF Node](parts/node.md).

## Coordinate System

Generally speaking, G4MF defines a coordinate system that is a superset of the right-handed 3D coordinate system found in OpenGL™, glTF™, and other 3D software and formats. For a camera, the +X axis points to the right, the +Y axis points up, the +Z axis points out of the screen towards the viewer and is used for depth, and any additional axes are perpendicular to these. Distance is measured in meters, angles are measured in radians, and all units are SI metric units whenever possible.

For convenience, the details of how the coordinate system works are described in a separate file: [G4MF Coordinate System](parts/coordinate_system.md).

## Data Storage

G4MF stores data with a combination of buffers, buffer views, and accessors. As an analogy with computer storage drives, a buffer is a disk, a buffer view is a partition, and an accessor is a file system.

For convenience, the details of how these work are described in a separate file: [G4MF Data](parts/data.md).

## Lights

G4MF lights define the light sources in the scene. Each light object defines the properties of a light, such as the type, color, intensity, and other properties. Lights may be referenced by nodes to instance them in the scene.

For convenience, the details of how lights work are described in a separate file: [G4MF Light](parts/light.md).

## Meshes

G4MF stores the visible geometry of objects inside of meshes. Each mesh is made of vertices and multiple surfaces, each of which may have a separate material. Mesh surfaces reference the shared mesh vertices, and may contain edge indices, cell indices, and more, each of which points to an accessor that encodes the data.

For convenience, the details of how meshes work are described in a separate file: [G4MF Mesh](parts/mesh/mesh.md).

### Materials

G4MF uses materials to define the appearance of surfaces. Each material is made of multiple channels, each of which may have a separate color, texture, and more. Materials are referenced by mesh surfaces, which are contained in meshes. Material channels may have per-cell colors, per-edge colors, per-vertex colors, and/or texture mapping, each of which points to an accessor that encodes the data.

For convenience, the details of how materials work are described in a separate file: [G4MF Material](parts/mesh/material.md).

### Deformation

G4MF meshes may be deformed by skeletons and blend shapes.

Skeletons are made of joints that are attached to bone nodes in the scene hierarchy, where mesh vertices are weighted to them, as detailed in [G4MF Skeleton Skinned Mesh Deformation](parts/mesh/skeleton.md).

Blend shapes allow for per-vertex deformations to be applied to meshes, as well as per-vertex-instance deformations for normals and texture coordinates, as detailed in [G4MF Blend Shape Mesh Deformation](parts/mesh/blend.md).

Skeletons and blend shapes may be used to represent rigs and facial expressions of characters/avatars, as detailed in [G4MF Characters/Avatars](parts/mesh/character_avatar.md).

## Physics

G4MF physics defines the physical properties of objects in the scene. It allows using shapes to define solid colliders or non-solid triggers, and allows defining the motion properties of objects, including mass, inertia, and more. Physics properties are not needed for loading the mesh geometry of the scene, and may be ignored if the file is only used for visual purposes, or if loading into an application that does not support physics and only needs the mesh geometry.

For convenience, the details of how physics work are described in a separate file: [G4MF Node Physics](parts/physics/node_physics.md).

### Shapes

G4MF shapes define mathematical shapes used for physics and other use cases. Each shape has a type and many size parameters which define the bounds of the shape. Most shapes are implicit surfaces, meaning that they are defined by a mathematical function and have a well-defined inside and outside. Shapes may be referenced on nodes to be used as physics colliders. If shapes are not referenced by node physics or by an extension, they are not used and may be ignored.

For convenience, the details of how shapes work are described in a separate file: [G4MF Shape](parts/physics/shape.md).

## Extensions

G4MF is designed to be extensible. All G4MF JSON objects inherit the `g4mf_item.schema.json` schema, which allows for `"extensions"`, `"extras"`, and `"name"` properties.

- The `"extensions"` property is an object, where each key is the name of an extension, and the value is a JSON object containing the extension data. Extensions are used when a formal specification exists, and the data inside conforms to a well-defined schema outside of the core G4MF specification.
  - Each extension name MUST be in the form of a registered prefix assigned to a group or organization, followed by an underscore, followed by the name of the extension. This ensures that extension names are unique, and avoids conflicts with other extensions.
- The `"extras"` property is an object, where each key may be any string, and each value may be any JSON value. Extras are used when a formal specification does not exist, such as for custom application-specific data. Users may use any keys and values they want, with no restrictions, and no guarantees of data consistency, interoperability, or conflict avoidance.

## Binary File Format

G4MF files may be stored in a JSON-based text format (`.g4tf`) or a binary format (`.g4b`). With the text format, binary blobs of data may either be base64-encoded within the JSON, or referenced as external files. The binary format is a more compact representation of the same data, which appends binary blobs of data to the end of the JSON.

For convenience, the details of how the binary format works are described in a separate file: [G4MF Binary File Format](parts/binary_file_format.md).

## JSON Schema

See [g4mf.schema.json](schema/g4mf.schema.json) for the G4MF main document JSON schema, and other files for all the other JSON schemas.
