# G4MF Data

## Overview

G4MF stores blobs of data with a combination of buffers, buffer views, and accessors. As an analogy with computer storage drives, a buffer is a disk, a buffer view is a partition, and an accessor is a file system.

## Example

The following example defines.

## Buffers

Buffers are the top-level data storage unit in G4MF. They are used to store many binary blobs of data together in a single file. For example, a buffer may contain vertices for several meshes, normal vectors for several meshes, edge or cell indices for several meshes, or all at once.

For text-based G4MF, this often takes the form of a `.bin` file next to the `.g4tf` file, or embedded base64-encoded data. For binary G4MF, this is usually the binary chunk of data at the end of the file, but this may also be a separate file. Most files only need one buffer for all the binary blob data in the file, but multiple buffers are allowed if the file is needed to be split into multiple files, such as if there is a file size limit.

For binary `.g4b` G4MF files, buffers usually have their data stored in binary blob chunks at the end of the file, after the G4MF JSON. For such buffers, the `"uri"` property is not used and should be omitted. The `"byteLength"` property is the uncompressed size of the data in bytes, while the chunk's data size includes any compression, if the chunk is compressed. See [G4MF Binary File Format](binary_file_format.md) for more details.

### Properties

| Property       | Type    | Description                                                       | Default                                          |
| -------------- | ------- | ----------------------------------------------------------------- | ------------------------------------------------ |
| **byteLength** | integer | The length of the buffer in bytes.                                | Required, no default.                            |
| **uri**        | string  | The relative URI to an external file, or a base64-encoded string. | Required except G4B buffers with data in chunks. |

#### Byte Length

The `"byteLength"` property is an integer number defining the length of the buffer in bytes. This property is required.

This property MUST NOT be negative. The actual size of the buffer data MAY be a few bytes larger than the declared length, in which case the extra bytes are unused, but the actual size MUST NOT be smaller than the declared length.

#### URI

The `"uri"` property is a string that may either be a relative URI to an external file, or a base64-encoded string. This property is required, except for buffer index 0 in binary G4MF files, which refers to the binary blob data chunk at the end of the file.

If using a base64-encoded string, it MUST be a data URI, which starts with the MIME type data prefix `data:application/octet-stream;base64,` and is followed by the base64-encoded data.

For binary `.g4b` G4MF files, `"uri"` MUST NOT be defined for the buffer at index 0, which is special and always refers to the binary blob data chunk at the end of the file. For all other buffers in a binary G4MF, `"uri"` SHOULD NOT contain base64-encoded data, since that would be less efficient than just storing the same data in the binary blob data chunk in buffer 0.

## Buffer Views

Buffer views define a subset of a buffer as a slice or view. They are the intended way to read data from a buffer. A single buffer view SHOULD be one type of data, such as serialized arrays of numbers, or the bytes of an image. Buffer views are often further given types by accessors, which define how to interpret the data in the buffer view, but may also be used directly without an accessor, such as when the buffer view contains the bytes of an image.

### Properties

| Property       | Type    | Description                                                          | Default               |
| -------------- | ------- | -------------------------------------------------------------------- | --------------------- |
| **buffer**     | integer | The index of the buffer that contains the data for this buffer view. | Required, no default. |
| **byteLength** | integer | The length of the buffer view in bytes.                              | Required, no default. |
| **byteOffset** | integer | The start offset of the buffer view in bytes.                        | `0`                   |

#### Buffer

The `"buffer"` property is an integer index that references a buffer in the G4MF file's document-level buffers array which contains the data for this buffer view. This property is required.

#### Byte Length

The `"byteLength"` property is an integer number defining the length of the buffer view in bytes. This property is required.

#### Byte Offset

The `"byteOffset"` property is an integer number defining the start offset of the buffer view in bytes. This property is optional and defaults to 0.

The byte offset is relative to the start of the buffer. For example, if the byte offset is 100, then byte 0 of the buffer view is byte 100 of the buffer. The declared byte offset plus the declared byte length MUST NOT exceed the buffer's `"byteLength"`.

## Accessors

Accessors provide a typed interpretation of the data in a buffer view. Accessors define the primitive data type and define the number of primitives in each element of the accessor. They are the intended way to handle numeric data, such as arrays of vertices, normals, colors, or texture coordinates.

### Properties

| Property          | Type    | Description                                                                | Default               |
| ----------------- | ------- | -------------------------------------------------------------------------- | --------------------- |
| **bufferView**    | integer | The index of the buffer view that contains the data for this accessor.     | Required, no default. |
| **primitiveType** | string  | The primitive data type used for each primitive component in the accessor. | Required, no default. |
| **vectorSize**    | integer | The number of primitives in each element of the accessor.                  | `1`                   |

#### Buffer View

The `"bufferView"` property is an integer index that references a buffer view in the G4MF file that contains the data for this accessor. This property is required.

The buffer view's `"byteLength"` MUST be a multiple of the size of each element, which is the size of the primitive type multiplied by the vector size. The amount of elements in the accessor is equal to the buffer view's `"byteLength"` divided by the size of each element. Additionally, the buffer view's `"byteOffset"` MUST be a multiple of the size of the primitive type, to ensure that the start of the data is aligned correctly.

#### Primitive Type

The `"primitiveType"` property is a string that defines the primitive data type used for each primitive component in the accessor. This property is required.

The primitive type SHOULD be some kind of primitive data type, such as float, int, or uint, and indicate the size. The enum is unbounded, allowing for future extensions, but the base specification defines a very wide range of types from 8-bit to 128-bit that should cover nearly all use cases. The following primitive types are DEFINED:

- `"float8"`: 8-bit or 1-byte IEEE-like quarter-precision floating point number with 1 sign bit, 4 exponent bits, 3 mantissa bits, max finite value 240.
- `"float16"`: 16-bit or 2-byte IEEE 754 half-precision floating point number.
- `"float32"`: 32-bit or 4-byte IEEE 754 single-precision floating point number. This MUST be supported.
- `"float64"`: 64-bit or 8-byte IEEE 754 double-precision floating point number.
- `"float128"`: 128-bit or 16-byte IEEE 754 quadruple-precision floating point number.
- `"int8"`: 8-bit or 1-byte two's compliment signed integer.
- `"int16"`: 16-bit or 2-byte two's compliment signed integer.
- `"int32"`: 32-bit or 4-byte two's compliment signed integer. This MUST be supported.
- `"int64"`: 64-bit or 8-byte two's compliment signed integer.
- `"int128"`: 128-bit or 16-byte two's compliment signed integer.
- `"uint8"`: 8-bit or 1-byte unsigned integer.
- `"uint16"`: 16-bit or 2-byte unsigned integer.
- `"uint32"`: 32-bit or 4-byte unsigned integer. This MUST be supported.
- `"uint64"`: 64-bit or 8-byte unsigned integer.
- `"uint128"`: 128-bit or 16-byte unsigned integer.

Support for reading `"float32"`, `"int32"`, and `"uint32"` is REQUIRED, due to how common they are. For the remaining types, they are defined, but not required. 8-bit integers, 16-bit integers, and all 64-bit types are highly recommended. Implementations MAY support only a subset of these types. If an implementation does not want to support `"float8"`, `"float128"`, `"int128"`, or any other type, the implementation MAY skip this accessor, failing to load any objects that use it, or MAY refuse to load the entire file.

Implementations MAY truncate or round types to fit into a supported type. For example, it is allowed to read `"float64` primitives which get converted to `"float32"` at import time, rounding the values to fit into the smaller type.

Inside of the buffer view the accessor refers to, the `"byteOffset"` and `"byteLength"` properties MUST be a multiple of the size of the primitive type, to ensure that the start of the data is aligned correctly, and ensure there are a whole number of primitives available in the accessor. For example, if the primitive type is `"float32"`, which requires 4 bytes each, then the `"byteOffset"` and `"byteLength"` properties MUST be a multiple of 4, and the number of primitives in the accessor is equal to the buffer view's `"byteLength"` divided by 4. For accessors with a `"vectorSize"` greater than 1, there are additional requirements for `"byteLength"` aligning to a whole number of elements, which is a superset of this requirement.

#### Vector Size

The `"vectorSize"` property is a positive integer number defining the number of primitives in each element of the accessor. This property is optional and defaults to 1.

For scalars this is 1, for 2D vectors this is 2, for 3D vectors this is 3, for 4D vectors this is 4, and so on. Matrices can be encoded as many-dimensional vectors, such as a 4x4 matrix with this property set to 16. Note that this is the number of primitives, not the number of bytes. This number MUST be a positive integer. If not specified, the vector size is 1, meaning each primitive is its own scalar element.

Inside of the buffer view the accessor refers to, the `"byteLength"` property MUST be a multiple of the size of each element, which is the size of the primitive type multiplied by the vector size. The amount of elements in the accessor is equal to the buffer view's `"byteLength"` divided by the size of each element.

For example, if encoding an array of Vector3 structs made of 32-bit floating-point numbers, the primitive type would be `"float32"` and the vector size would be `3`. Each of those accessor elements then takes up 12 bytes. The buffer view's `"byteLength"` then MUST be a multiple of 12, such as 120 bytes encoding 10 elements. Additionally, the buffer view's `"byteOffset"` MUST be a multiple of 4, since the primitive type has a size of 4 bytes, as described above.

## JSON Schema

See these files for the JSON schema of the data properties:

- Buffers: [g4mf.buffer.schema.json](../schema/g4mf.buffer.schema.json)
- Buffer Views: [g4mf.bufferView.schema.json](../schema/g4mf.bufferView.schema.json)
- Accessors: [g4mf.accessor.schema.json](../schema/g4mf.accessor.schema.json)
