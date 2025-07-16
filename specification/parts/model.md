# G4MF Model

## Overview

Models are references to other self-contained files that can be used in the scene graph. They can be used to reference other G4MF files, [OFF](https://en.wikipedia.org/wiki/OFF_%28file_format%29) files, glTF™ files, [OCIF](https://github.com/ocwg/spec) files, or any other format. These models are then used by nodes, where each node using the model becomes a new instance of the model's nodes, and the host G4MF's node properties override the properties of the instantiated model's root node. This allows for modularity and reusability of models across different scenes and applications.

Critically, there is one requirement for models, regardless of format: they MUST be some kind of data that can be imported as a node or tree of nodes, and placed in the scene graph. This means that models cannot be arbitrary files, such as images or audio files. If there is a desire to have images visible in the scene, the node in the scene graph should be a mesh with the image applied as a texture, defining the size, shape, orientation, and other visual characteristics. If there is a desire to have audio files in the scene, an extension should be used to define an audio node with volume, spatialization, and other playback characteristics. Models MUST be things that can be imported as nodes, a tree of nodes, or directly used on a node, such as importing an OFF file as a standalone mesh and placing it on a mesh node.

Implementations may choose to support any formats they wish. Support for referencing other G4MF files is highly recommended. However, the ability to reference other files at all is a niche feature, so implementations may choose not to support it at all. If a given model format referenced by a G4MF file is not supported, implementations SHOULD show a warning when importing the G4MF file.

Note that G4MF requires that all named items in the file have unique names. This requirement does not exist for names between files, so a G4MF file imported into another G4MF file may have two nodes with the same name between them. Also, if a model with multiple nodes is instantiated multiple times, there will necessarily be multiple nodes in the overall scene graph which have the same name. Therefore, names are not guaranteed to be globally unique across the entire scene graph, but they are guaranteed to be unique within a single G4MF file.

## Properties

| Property       | Type      | Description                                                         | Default               |
| -------------- | --------- | ------------------------------------------------------------------- | --------------------- |
| **bufferView** | `integer` | The index of the buffer view that contains the data for this model. | `-1` (no buffer view) |
| **uri**        | `string`  | The relative URI of the model file (highly recommended).            | `""` (no URI)         |
| **mimeType**   | `string`  | The model's media type, as registered with IANA, if registered.     | Required, no default. |

### Buffer View

The `"bufferView"` property is an integer index of a G4MF buffer view. If not specified, the default value is `-1`, meaning there is no buffer view.

Only one of `"bufferView"` or `"uri"` MUST be defined. Both properties SHOULD NOT be defined at the same time. If both are defined, the `"uri"` property takes precedence, and the `"bufferView"` may be used as a fallback if the file at the URI cannot be loaded.

### URI

The `"uri"` property is a string that defines the URI of the model file, relative to the G4MF file's location. If not specified, the default value is an empty string, meaning there is no URI.

Specifying a URI is highly recommended, as it allows using an external file for the model, which is the main motivation for separating a tree of nodes into their own isolated models. However, storing model data in a buffer view may still be useful for deduplicating data in cases where the same tree of nodes is used many times in the same G4MF file.

Only one of `"bufferView"` or `"uri"` MUST be defined. Both properties SHOULD NOT be defined at the same time. If both are defined, the `"uri"` property takes precedence, and the `"bufferView"` may be used as a fallback if the file at the URI cannot be loaded.

### MIME Type

The `"mimeType"` property is a string that defines the media type of the model file. This property is required and MUST be defined.

Models may be used for any format that can be imported as a node or tree of nodes, so the MIME type is not limited to a specific set of values, but may be any valid MIME type. When a media type is registered with IANA, this MUST match the media type string as registered with IANA. When a media type is not registered with IANA, any placeholder name may be used pending registration. For example, here are some common MIME types that may sensibly be used for models:

| MIME Type               | File Extension     | Description                       | Import Considerations                                                                                                                                                           |
| ----------------------- | ------------------ | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model/g4mf-binary` ⚠️  | `.g4b`             | Good 4D model format Binary       | Can be directly imported as a tree of nodes.                                                                                                                                    |
| `model/g4mf+json` ⚠️    | `.g4tf`            | Good 4D model format Text File    | Can be directly imported as a tree of nodes.                                                                                                                                    |
| `model/gltf-binary`     | `.glb` & `.vrm`    | Khronos glTF™ Binary (or VRM)     | A single root node must be synthesized, unless using [GODOT_single_root](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Vendor/GODOT_single_root) (recommended). |
| `model/gltf+json`       | `.gltf`            | Khronos glTF™ Text / JSON         | A single root node must be synthesized, unless using [GODOT_single_root](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Vendor/GODOT_single_root) (recommended). |
| `model/off` ⚠️          | `.off`             | OFF geometry format               | Imports as a mesh, needs to have a mesh node synthesized to hold the mesh.                                                                                                      |
| `model/obj`             | `.obj`             | Wavefront OBJ file                | Imports as a mesh, needs to have a mesh node synthesized to hold the mesh.                                                                                                      |
| `model/stl`             | `.stl`             | Stereolithography file            | Imports as a mesh, needs to have a mesh node synthesized to hold the mesh.                                                                                                      |
| `model/ply`             | `.ply`             | Polygon File Format               | Imports as a mesh, needs to have a mesh node synthesized to hold the mesh.                                                                                                      |
| `model/3mf`             | `.3mf`             | 3D Manufacturing Format           | Supports multiple meshes, but no scene graph. May be imported as a mesh node or multiple mesh nodes.                                                                            |
| `model/fbx` ⚠️          | `.fbx`             | Autodesk FilmBox                  | Can be directly imported as a tree of nodes.                                                                                                                                    |
| `model/vnd.usda`        | `.usda`            | Universal Scene Description ASCII | Can be directly imported as a tree of nodes, contain a scene graph with a root "prim".                                                                                          |
| `model/vnd.usdc` ⚠️     | `.usdc`            | USD Compressed Binary             | Can be directly imported as a tree of nodes, contain a scene graph with a root "prim".                                                                                          |
| `model/vnd.usdz+zip`    | `.usdz`            | Universal Scene Description ZIP   | Can be directly imported as a tree of nodes, contain a scene graph with a root "prim".                                                                                          |
| `model/vnd.collada+xml` | `.dae`             | Khronos COLLADA™ XML              | Can be directly imported as a tree of nodes.                                                                                                                                    |
| `model/vrml`            | `.wrl` & `.wrz`    | Virtual Reality Modeling Language | Can be directly imported as a tree of nodes.                                                                                                                                    |
| `model/x3d+xml`         | `.x3d` & `.x3dz`   | X3D (Extensible 3D) XML           | Can be directly imported as a tree of nodes.                                                                                                                                    |
| `model/x3d+vrml`        | `.x3dv` & `.x3dvz` | X3D (Extensible 3D) VRML          | Can be directly imported as a tree of nodes.                                                                                                                                    |
| `model/x3d+binary`      | `.x3db` & `.x3dbz` | X3D (Extensible 3D) Binary        | Can be directly imported as a tree of nodes.                                                                                                                                    |
| `application/ocif+json` | `.ocif`            | Open Canvas Interchange Format    | Can be directly imported as a tree of nodes. Meant for canvases and GUIs.                                                                                                       |

⚠️ = Not registered with IANA, and may possibly change if registered in the future.

Implementations are not expected to support all of these MIME types, they may support some, one, or even none of them. This list is also not intended as suggestions for model formats to implement, since it includes deprecated formats such as COLLADA™ and VRML, and proprietary formats such as FBX. This list is intended as a non-comprehensive set of examples of formats that possibly make sense to be used as models due to their ability to have their scene graphs imported as a tree of nodes.

For more information, see the list of IANA media types: https://www.iana.org/assignments/media-types/media-types.xhtml#model

## JSON Schema

- See [g4mf.model.schema.json](../schema/g4mf.model.schema.json) for the model properties JSON schema.
- See [g4mf.node.schema.json](../schema/g4mf.node.schema.json) for how models are used on nodes.
