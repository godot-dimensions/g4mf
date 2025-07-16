# G4MF Core

## Overview

This file describes the core foundational data schemas underlying the Good 4D Model Format (G4MF). These structures are used generally everywhere in G4MF files, not just in specific parts.

## IDs

The G4MF ID schema defines an integer used to refer to other items in the G4MF file by index in an array. Which array is being referenced is defined by the context in which the ID is used. For example, a node's `"mesh"` property is defined as referring to a mesh in the G4MF file's `"meshes"` array, so the ID is an index into that array.

If defined, the ID MUST be a valid index in the array it is referencing. The ID MUST NOT be out of bounds of the target array. The ID MUST be an integer, with no fractional part; values such as `1.5` are not valid IDs. The ID of `-1` is reserved as a placeholder value when the relevant field not defined, indicating the lack of pointing to anything, and may be thought of as equivalent to a `null` value. If an array of IDs is defined, sensitive to what slot the ID is in, and the schema allows it, the value `-1` MAY be used as a placeholder for that slot, indicating that the slot does not point to anything. However, in all other cases, such as for standalone properties like `"mesh"`, negative IDs MUST NOT be written to G4MF files. Valid IDs written into standalone properties in G4MF files MUST be integers greater than or equal to `0` and less than the length of the array they are referencing.

## Items

Items are the base schema for all JSON objects in G4MF. All G4MF schemas of type `object` inherit the G4MF Item schema, or inherit a descendant schema. This includes the root object of the G4MF file itself, which is also an item. The only G4MF schema which does not inherit from the G4MF Item schema is G4MF ID, which is not an `object`, but rather an `integer`. Similarly, all valid user-defined G4MF extensions with schemas of type `object` MUST have G4MF Item schema as a base class, inheriting from it or a descendant schema.

### Properties

| Property       | Type     | Description                                                        | Default                  |
| -------------- | -------- | ------------------------------------------------------------------ | ------------------------ |
| **comment**    | `string` | A comment or description of the item.                              | `""` (empty string)      |
| **extensions** | `object` | A dictionary of extension objects.                                 | `{}` (no extension data) |
| **extras**     | `object` | Application-specific data without a standardized extension schema. | `{}` (no extra data)     |
| **name**       | `string` | The file-unique name of the item.                                  | `""` (empty string)      |

#### Comment

The `"comment"` property is a string that allows for human-readable comments or descriptions of the item.

This property MUST NOT be used for any functional purpose software that processes G4MF files, and is only allowed to be used for the purpose of annotating an example G4MF file with additional information when reading the raw text of the file manually, like a comment in a programming language.

#### Extensions

The `"extensions"` property is an object that allows for defining extensions to the G4MF format.

Each key is the name of the extension, in the format of `"PREFIX_extension_name"`, where `PREFIX` is a reserved prefix registered with G4MF, and `extension_name` is the snake_case name of the extension. Extension names SHOULD further comply to `"PREFIX_subject_name"`, where `subject` is a category, often the name of an existing G4MF data structure being extended, or may be more general like `"audio"`, but may use any name followed by the prefix and an underscore.

Each value is the extension data, which is a JSON object that conforms to the schema defined by the extension. Valid G4MF extensions MUST have schemas defined for any data they define, and those schemas MUST extend the G4MF Item schema whenever they are of type `object`. Note that, in niche use cases, it is possible for a G4MF extension to define no data and be used nowhere in any `"extensions"` property, in which case the extension's only behavior is a boolean flag that may or may not exist in `"extensionsUsed"`.

#### Extras

The `"extras"` property is an object that allows for application-specific data without a standardized extension schema.

This property is useful for storing additional data for a specific application's own use case when there is no desire to define a full extension schema for the data. The keys may be any string, and the values may be any value. There are no guarantees about naming conflicts or the structure of the data.

#### Name

The `"name"` property is a string that defines the file-unique name of the item.

If defined, this MUST be unique within the G4MF file, across all items, including all nodes, meshes, materials, textures, and other items. For example, if a G4MF node is named `"Crate"`, then the mesh data cannot also be named `"Crate"`, it must be named something else, such as `"CrateMesh"`, or be left unnamed by not defining the `"name"` property. If two or more items in the same G4Mf file have the same name, the G4MF file is invalid. If the `"name"` property is not defined, it is considered equivalent to an empty string. Empty or non-existent names are the only cases where more than one item may have that name, since it is not always useful for every item to have a name.

The name uniqueness requirement exists for all items within a file, but does not apply for names between files. Two G4MF files may have up to two nodes with the same name between them, such as a each having a node named `"Crate"`. If a G4MF file uses another G4MF file as a model (see [G4MF Model](model.md)), this means that there may be multiple nodes or other items with the same name in the overall scene graph. Therefore, names are not guaranteed to be globally unique across the entire scene graph, but they are guaranteed to be unique within a single G4MF file.

## File References

When G4MF files need to reference data that could be found in an external file, such as an image file, model file, audio file, or any other file, they use a G4MF File Reference. All file references are required to define the file's MIME type, and may refer to stored data either in a buffer view or an external file URI.

The only case where a G4MF File Reference is not used for referencing external data is in [G4MF Buffers](data.md#buffers) themselves. All G4MF File References are allowed to store data in buffer views, but buffer views reference data stored in buffers, therefore it would be a circular reference. Additionally, the `"mimeType"` property is not useful for buffers, since they are by definition unstructured blobs of binary data, which only have structure defined by the buffer views and accessors using them.

### Properties

| Property       | Type      | Description                                                        | Default               |
| -------------- | --------- | ------------------------------------------------------------------ | --------------------- |
| **bufferView** | `integer` | The index of the buffer view that contains the data for this file. | `-1` (no buffer view) |
| **uri**        | `string`  | The relative URI of the file (recommended).                        | `""` (no URI)         |
| **mimeType**   | `string`  | The file's media type, as registered with IANA, if registered.     | Required, no default. |

#### Buffer View

The `"bufferView"` property is an integer index of a G4MF buffer view. If not specified, the default value is `-1`, meaning there is no buffer view.

Only one of `"bufferView"` or `"uri"` MUST be defined. Both properties SHOULD NOT be defined at the same time. If both are defined, the `"uri"` property takes precedence, and the `"bufferView"` may be used as a fallback if the file at the URI cannot be loaded.

#### URI

The `"uri"` property is a string that defines the URI of the file, relative to the G4MF file's location. If not specified, the default value is an empty string, meaning there is no URI.

Only one of `"bufferView"` or `"uri"` MUST be defined. Both properties SHOULD NOT be defined at the same time. If both are defined, the `"uri"` property takes precedence, and the `"bufferView"` may be used as a fallback if the file at the URI cannot be loaded.

#### MIME Type

The `"mimeType"` property is a string that defines the media type of the file. This property is required and MUST be defined.

The MIME type is not limited to a specific set of values, but may be any valid MIME type. When a file format's media type is registered with IANA, this MUST match the media type string as registered with IANA. When a file format's media type is not registered with IANA, any placeholder name may be used pending registration. For example, a PNG image file would be referenced with `"mimeType"` set to `"image/png"`, matching the IANA registration for PNG files.

For more information, see the list of IANA media types: https://www.iana.org/assignments/media-types/media-types.xhtml#model

## JSON Schema

- See [g4mf_item.schema.json](../schema/g4mf_item.schema.json) for the G4MF Item properties JSON schema.
- See [g4mf_file_ref.schema.json](../schema/g4mf_file_ref.schema.json) for the G4MF File Reference properties JSON schema.
