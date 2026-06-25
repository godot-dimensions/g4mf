# G4MF Data Storage

## Overview

G4MF stores blobs of data with a combination of buffers, buffer views, and accessors. As an analogy with computer storage drives, a buffer is a disk, a buffer view is a partition, and an accessor is a file system.

## Example

The following example defines.

## Buffers

Buffers are the top-level data storage unit in G4MF. They are used to store many binary blobs of data together in a single file. For example, a buffer may contain vertices for several meshes, edge or simplex indices for several meshes, normal vectors for several meshes, the bytes of an image, or all at once. The `"byteLength"` property is required for all buffers, and contains the decoded size of the data in bytes.

For text-based G4MF (`.g4tf`), these often take the form of `.bin` files pointed to by `"uri"` from the `.g4tf` file, or may be embedded base64-encoded data in the `"uri"` property. In text-based G4MF files, the `"chunk"` property MUST NOT be defined for any buffers, and the `"uri"` property MUST be defined for each buffer. A buffer in a text-based G4MF file is invalid if the `"uri"` property is not defined.

For binary G4MF (`.g4b`), these are usually binary chunks of data pointed to by the `"chunk"` property. However, binary G4MF files may also have buffer data stored in the `"uri"` property in the same ways available to text-based G4MF files, either with a separate `.bin` file or embedded base64-encoded data. One of `"chunk"` or `"uri"` MUST be defined for each buffer. A buffer is invalid if neither is defined, and invalid if both are defined. The chunk's data size is the encoded size of the data, which may not match the buffer's `"byteLength"` property if the chunk has non-plain encoding (such as compression or encryption). See [G4MF Binary File Format](binary_file_format.md) for more details.

Most files only need one buffer for all the binary blob data in the file. Multiple buffers are allowed, for cases of splitting up data. Data may be split into multiple `.bin` files, which may be useful to keep the file size under the limits of any platform, environment, or file system. Data may also be split into multiple binary blob chunks in a binary G4MF file, which may be useful to keep the chunk size smaller for easier streaming.

Non-normative implementation note: Some languages, such as C#, JavaScript, and others, have limits on the size of managed memory like byte arrays. These limits are often less than 2 GiB. G4MF does not limit the size of buffers, but in practice, exporters and asset authors may wish to split up data into multiple buffers when the size of a buffer would otherwise approach 2 GiB. For a safety margin, consider limiting buffers to about 2 billion bytes to avoid approaching the limits of managed memory languages.

### Properties

| Property        | Type      | Description                                                       | Default                                              |
| --------------- | --------- | ----------------------------------------------------------------- | ---------------------------------------------------- |
| **byteLength**  | `integer` | The decoded length of the buffer in bytes.                        | Required, no default.                                |
| **chunk**       | `integer` | The index of the chunk containing the buffer data.                | Required for G4B buffers with data in chunks.        |
| **encoding**    | `string`  | The encoding used for the buffer data.                            | Plainly encoded if not specified.                    |
| **uri**         | `string`  | The relative URI to an external file, or a base64-encoded string. | Required except for G4B buffers with data in chunks. |

#### Byte Length

The `"byteLength"` property is an integer number defining the decoded length of the buffer in bytes. This property is required.

This property MUST NOT be negative. The actual size of the buffer data MAY be a few bytes larger than the declared length, in which case the extra bytes are unused, but the actual size MUST NOT be smaller than the declared length.

When data is encoded differently, such as compressed or encrypted, this property refers to the decoded size of the data. The encoded size of the data is determined by the chunk size in binary G4MF files, the file length of external buffer files, or the string content of base64-encoded data URIs.

#### Chunk

The `"chunk"` property is an integer index that references a chunk in a binary G4MF file that contains the buffer data.

This property is only applicable for binary G4MF files (`.g4b`) where the buffer data is stored in chunks. This property MUST NOT be defined for buffers in text-based G4MF files (`.g4tf`). If this property is defined in text-based G4MF files, the file is invalid. If both `"chunk"` and `"uri"` are defined for a buffer, the file is invalid. If neither `"chunk"` nor `"uri"` are defined for a buffer, the file is invalid.

The most common case of a binary G4MF (`.g4b`) layout has the G4MF JSON chunk at index `0`, and one additional chunk containing a blob of buffer data at index `1`. Such a case will have the `"chunk"` property of the first buffer set to `1`, such that the G4MF JSON will contain `{ "buffers": [ { "byteLength": 12345, "chunk": 1 } ] }`, where `12345` should be replaced with the decoded size of the buffer data in bytes.

#### Encoding

The `"encoding"` property is a string that defines the encoding format used for the buffer data. This property is optional and defaults to plainly encoded if not specified.

Valid encoding values are strings representing [FourCC](https://en.wikipedia.org/wiki/FourCC) codes. This allows for easy identification of the headers if a human inspects the file in a hex editor. Implementations MAY choose to display these values to the user as plain text, such as by showing the encoding in an error message when the encoding format is unsupported.

This value MUST be a string matching the binary encoding indicator, as defined in [G4MF Binary File Format](binary_file_format.md). Each string MUST be 4 characters after any escaping, convertible to a sequence of 4 numbers between `0x00` and `0xFF` (4 bytes). All control characters MUST be escaped to comply with the JSON specification for strings, and all non-ASCII characters MUST also be escaped, including those below `0x20` or above `0x7E` (other characters may also optionally be escaped, but these are required to be escaped). However, the string is RECOMMENDED to be a string of 4 ASCII characters, so long as the binary G4MF file's chunk encoding indicator matches the string, if the buffer data is stored in a chunk.

For example, the string `"Zstd"` indicates Zstandard compression. This corresponds to the byte sequence `0x5A 0x73 0x74 0x64`, or `0x6474735A` as a little-endian unsigned 32-bit integer, in the chunk encoding indicator of a binary G4MF (`.g4b`) file. Plainly encoded data MUST NOT have this property set, and for buffers in binary blob chunks, the encoding indicator of plainly encoded chunks MUST be set to `0x00000000` (four zero bytes).

When encoded data is stored in a separate file or a data URI, `"encoding"` is the only way to indicate that the data is encoded, and the file size or data URI string content determines the encoding size of the data, including any compression or encryption. When encoded data is stored in a binary blob chunk at the end of the file, both `"encoding"` and the binary file's encoding indicator MUST be set to the same value, and the binary file's chunk size is the encoded size of the data, including any compression or encryption. If there is a mismatch between the `"encoding"` property and the binary file's encoding indicator, the file is invalid. In both cases, the `"byteLength"` property is the decoded size of the data in bytes, excluding any compression or encryption.

#### URI

The `"uri"` property is a string that may either be a URI to an external file, or a base64-encoded string. This property is required, except for buffers in binary G4MF files whose data is stored in binary blob chunks via the `"chunk"` property.

The URI may be relative to the G4MF file's location, or alternatively, may be a web address, or any other valid URI format. If the URI starts with `https://`, it is treated as a web address and indicates the buffer file is located there. Implementations may cache and reuse downloaded buffer files as they see fit. If the URI starts with any other scheme, it uses that protocol. If using a base64-encoded string, it MUST be a data URI, which starts with the MIME type data prefix `data:application/octet-stream;base64,` and is followed by the base64-encoded data. If the URI does not contain `://` and is not a data URI, it is treated as a relative path to the G4MF file's location.

For binary G4MF (`.g4b`) files, if `"chunk"` is defined for a buffer, then `"uri"` MUST NOT be defined on the same buffer. If both `"chunk"` and `"uri"` are defined for a buffer, the file is invalid. If neither `"chunk"` nor `"uri"` are defined for a buffer, the file is invalid.

For all other buffers in binary G4MF (`.g4b`) files, `"uri"` SHOULD NOT contain base64-encoded data, since that would be less efficient than just storing the same data in the binary blob data chunks. Binary G4MF files SHOULD either have buffer data stored in binary blob chunks at the end of the file, or store buffer data in external files, or a mix, but not store buffer data in base64-encoded data URIs.

## Buffer Views

Buffer views define a subset of a buffer as a slice or view. They are the intended way to read data from a buffer. A single buffer view SHOULD be one type of data, such as serialized arrays of numbers, or the bytes of an image. Buffer views are often further given types by accessors, which define how to interpret the data in the buffer view, but may also be used directly without an accessor, such as when the buffer view contains the bytes of an image.

### Properties

| Property       | Type      | Description                                                          | Default               |
| -------------- | --------- | -------------------------------------------------------------------- | --------------------- |
| **buffer**     | `integer` | The index of the buffer that contains the data for this buffer view. | `0`                   |
| **byteLength** | `integer` | The length of the buffer view in bytes.                              | Required, no default. |
| **byteOffset** | `integer` | The start offset of the buffer view in bytes.                        | `0`                   |

#### Buffer

The `"buffer"` property is an integer index that references a buffer in the G4MF file's document-level buffers array which contains the data for this buffer view. This property is optional, if not specified, the buffer view refers to buffer index 0.

#### Byte Length

The `"byteLength"` property is an integer number defining the length of the buffer view in bytes. This property is required.

#### Byte Offset

The `"byteOffset"` property is an integer number defining the start offset of the buffer view in bytes. This property is optional and defaults to 0.

The byte offset is relative to the start of the buffer. For example, if the byte offset is 100, then byte 0 of the buffer view is byte 100 of the buffer. The declared byte offset plus the declared byte length MUST NOT exceed the buffer's `"byteLength"`.

## Accessors

Accessors provide a typed interpretation of the data in a buffer view. Accessors define the component data type and define the number of components in each element of the accessor (1 for scalar elements, more for vector elements). They are the intended way to handle numeric data, such as arrays of vertices, normals, colors, or texture coordinates.

### Properties

| Property          | Type      | Description                                                                | Default               |
| ----------------- | --------- | -------------------------------------------------------------------------- | --------------------- |
| **bufferView**    | `integer` | The index of the buffer view that contains the data for this accessor.     | Required, no default. |
| **componentType** | `string`  | The component data type used for each component component in the accessor. | Required, no default. |
| **vectorSize**    | `integer` | The number of components in each element of the accessor.                  | `1`                   |

#### Buffer View

The `"bufferView"` property is an integer index that references a buffer view in the G4MF file that contains the data for this accessor. This property is required.

The buffer view's `"byteLength"` MUST be a multiple of the size of each element, which is the size of the component type multiplied by the vector size. The amount of elements in the accessor is equal to the buffer view's `"byteLength"` divided by the size of each element. Additionally, the buffer view's `"byteOffset"` MUST be a multiple of the size of the component type, to ensure that the start of the data is aligned correctly.

#### Component Type

The `"componentType"` property is a string that defines the component data type used for each primitive component in the accessor. This property is required.

The component type SHOULD be some kind of primitive numeric data type, such as float, int, or uint, and indicate the size. The enum is unbounded, allowing for future extensions, but the base specification defines a very wide range of types from 8-bit to 128-bit that should cover nearly all use cases. The following component types are DEFINED:

- `"float8"`: 8-bit or 1-byte IEEE-like quarter-precision floating point number with 1 sign bit, 4 exponent bits, 3 mantissa bits, max finite value 240.
- `"float16"`: 16-bit or 2-byte IEEE 754 half-precision floating point number.
- `"float32"`: 32-bit or 4-byte IEEE 754 single-precision floating point number. This MUST be supported.
- `"float64"`: 64-bit or 8-byte IEEE 754 double-precision floating point number.
- `"float128"`: 128-bit or 16-byte IEEE 754 quadruple-precision floating point number.
- `"int8"`: 8-bit or 1-byte two's complement signed integer.
- `"int16"`: 16-bit or 2-byte two's complement signed integer.
- `"int32"`: 32-bit or 4-byte two's complement signed integer. This MUST be supported.
- `"int64"`: 64-bit or 8-byte two's complement signed integer.
- `"int128"`: 128-bit or 16-byte two's complement signed integer.
- `"uint8"`: 8-bit or 1-byte unsigned integer.
- `"uint16"`: 16-bit or 2-byte unsigned integer.
- `"uint32"`: 32-bit or 4-byte unsigned integer. This MUST be supported.
- `"uint64"`: 64-bit or 8-byte unsigned integer.
- `"uint128"`: 128-bit or 16-byte unsigned integer.

Support for reading `"float32"`, `"int32"`, and `"uint32"` is REQUIRED, due to how common they are. For the remaining types, they are defined, but not required. 8-bit integers and 16-bit integers are very highly recommended, 16-bit floats are highly recommended, and all 64-bit types are recommended. Implementations MAY support only a subset of these types. If an implementation does not want to support `"float8"`, `"float128"`, `"int128"`, or any other type, the implementation MAY skip this accessor, failing to load any objects that use it, or MAY refuse to load the entire file.

Implementations MAY truncate or round types to fit into a supported type. For example, it is allowed to read `"float64"` components which get converted to `"float32"` at import time, rounding the values to fit into the smaller type. Accessor component types only define how the data is stored in the file, not how it is represented in memory at runtime, and do not impose restrictions on mathematical operations or other usage.

If the data in the accessor is always of type `"uint8"` with a vector size always set to 1, consider using a buffer view directly instead of an accessor, since the accessor is not providing any additional information beyond the slice of the buffer already provided by the buffer view. For example, do not use `"uint8"` to store the data of a PNG image, or any accessor type at all for that matter. The `"uint8"` type is intended to be used when users of this accessor need to interpret the data as numbers, and other accessor types are also allowed, simplifying usages, which can always point to an accessor instead of conditionally pointing to an accessor or a buffer view.

Inside of the buffer view the accessor refers to, the `"byteOffset"` and `"byteLength"` properties MUST be a multiple of the size of the component type, to ensure that the start of the data is aligned correctly, and ensure there are a whole number of components available in the accessor. For example, if the component type is `"float32"`, which requires 4 bytes each, then the `"byteOffset"` and `"byteLength"` properties MUST be a multiple of 4, and the number of components in the accessor is equal to the buffer view's `"byteLength"` divided by 4. For accessors with a `"vectorSize"` greater than 1, there are additional requirements for `"byteLength"` aligning to a whole number of elements, which is a superset of this requirement.

#### Vector Size

The `"vectorSize"` property is a positive integer number defining the number of components in each element of the accessor. This property is optional and defaults to 1.

For scalars this is 1, for 2D vectors this is 2, for 3D vectors this is 3, for 4D vectors this is 4, and so on. Matrices can be encoded as many-dimensional vectors, such as a 4x4 matrix with this property set to 16. Note that this is the number of components, not the number of bytes. This number MUST be a positive integer. If not specified, the vector size is 1, meaning each component is its own scalar element.

Inside of the buffer view the accessor refers to, the `"byteLength"` property MUST be a multiple of the size of each element, which is the size of the component type multiplied by the vector size. The amount of elements in the accessor is equal to the buffer view's `"byteLength"` divided by the size of each element.

For example, if encoding an array of Vector3 structs made of 32-bit floating-point numbers, the component type would be `"float32"` and the vector size would be `3`. Each of those accessor elements then takes up 12 bytes. The buffer view's `"byteLength"` then MUST be a multiple of 12, such as 120 bytes encoding 10 elements. Additionally, the buffer view's `"byteOffset"` MUST be a multiple of 4, since the component type has a size of 4 bytes, as described above.

## JSON Schema

See these files for the JSON schema of the data properties:

- Buffers: [g4mf.buffer.schema.json](../schema/g4mf.buffer.schema.json)
- Buffer Views: [g4mf.bufferView.schema.json](../schema/g4mf.bufferView.schema.json)
- Accessors: [g4mf.accessor.schema.json](../schema/g4mf.accessor.schema.json)
