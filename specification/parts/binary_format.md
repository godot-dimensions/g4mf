# G4MF Binary Format

G4MF files may be stored in a JSON-based text format (`.g4tf`) or a binary format (`.g4b`). With the text format, binary blobs of data may either be base64-encoded within the JSON, or referenced as external files. The binary format is a more compact representation of the same data, which appends binary blobs of data to the end of the JSON.

The binary format begins with a 16-byte file header, which contains the following fields:

- A 4-byte magic number, which MUST be equal to the byte sequence `0x47 0x34 0x4D 0x46`, or ASCII string "G4MF".
  - When interpreted as a little-endian unsigned 32-bit integer, this is `0x464D3447`.
- A 4-byte version number, which MUST be equal to the byte sequence `0x00 0x00 0x00 0x00`, or zero.
  - This value is only 0 for the draft version of the specification. The final version will have a different value.
- A 8-byte size number, which MUST be equal to the total size in bytes of the entire file, including the file header, all chunks, all JSON data, and all binary blobs of data.
  - This value is a little-endian unsigned 64-bit integer, meaning the maximum file size of a binary G4MF file is 2^64 - 1 bytes.

After the file header, the file consists of a series of one or more chunks. Each chunk begins with its own 16-byte chunk header, with a similar format to the file header:

- A 4-byte chunk type. In the base specification, this MUST be one of the following:
  - The byte sequence `0x4A 0x53 0x4F 0x4E`, the ASCII string "JSON". This indicates the chunk contains JSON data.
    - When interpreted as a little-endian unsigned 32-bit integer, this is `0x4E4F534A`.
    - JSON chunks MUST be UTF-8 encoded without a BOM, MUST NOT contain control characters `0x7F` or `0x00` through `0x1F` except for optionally tab `0x09` and line feed `0x0A`, and MUST be a valid JSON object. These requirements also apply to the text format.
  - The byte sequence `0x42 0x4C 0x4F 0x42`, the ASCII string "BLOB". This indicates the chunk contains binary blob data, usually the data of a buffer.
    - When interpreted as a little-endian unsigned 32-bit integer, this is `0x424F4C42`.
  - Implementations MAY define additional chunk types, but this is usually not needed. The byte sequence selected SHOULD be a somewhat-human-readable magic sequence of printable ASCII characters, but may be any value.
- A 4-byte chunk compression format indicator. In the base specification, this MUST be one of the following:
  - The byte sequence `0x00 0x00 0x00 0x00`, or zero. This indicates the chunk is not compressed.
  - The byte sequence `0x5A 0x73 0x74 0x64`, the ASCII string "Zstd". This indicates the chunk is compressed using the Zstandard compression format.
    - When interpreted as a little-endian unsigned 32-bit integer, this is `0x6474735A`.
    - The chunk data MUST also include Zstd's own magic number `0x28 0xB5 0x2F 0xFD` at the start of the data, it cannot be omitted.
  - Implementations MAY define additional compression formats. The byte sequence selected SHOULD be a somewhat-human-readable magic sequence of printable ASCII characters, but may be any value. Note: This does not need to match the magic number used by the compression format itself.
- A 8-byte chunk data size number, which MUST be equal to the size in bytes of the chunk data, excluding the chunk header, and excluding any padding after the chunk data.
  - This value is a little-endian unsigned 64-bit integer. The maximum chunk data size is 2^64 - 33 bytes (an additional 32 bytes are subtracted for the file and chunk headers).
  - If the chunk is compressed, this value is the size of the compressed data, not the uncompressed data. However, the `"byteLength"` field in the JSON data refers to the uncompressed size of the data.
- The data in each chunk immediately follows the chunk header, and is of the size in bytes indicated by the chunk data size number.

Every chunk header MUST be aligned to a 16-byte boundary. This means that whenever a chunk has another chunk after it, the chunk on the left MUST have padding placed after the data (not included in the chunk data size) to the next 16-byte boundary (if already at the boundary, there is no padding). The final chunk in the file does not need padding after it. Padding is usually null `0x00` bytes for binary blobs or compressed chunks, but space `0x20` characters SHOULD be used for padding uncompressed JSON data. The 8-byte chunk data size number MUST NOT include this padding, it only includes the used bytes of the chunk data.

The first chunk in the file MUST be a JSON chunk containing the G4MF JSON data that conforms to the main G4MF schema `g4mf.schema.json`. If the file has binary blob chunks containing G4MF buffers, they MUST be the following chunks in the file. The G4MF JSON data's buffers array refer to these chunks, such that the buffer at index 0 uses the second chunk if `"uri"` is not defined in that buffer, the buffer at index 1 uses the third chunk if `"uri"` is not defined in that buffer, and so on. This means the `"uri"` property takes precedence over the chunk, so it should be absent in order to use the chunk's bytes. The G4MF JSON buffer's `"byteLength"` always refers to the uncompressed size of the data, but the chunk's data size refers to the compressed size of the data if the chunk is compressed. The behavior of additional chunks not used by buffers is undefined, and may be used for any purpose.

Binary G4MF files smaller than 32 bytes are invalid, because that is the minimum size of the file header and the first chunk header. The minimum possible size of a valid uncompressed G4MF binary file is 57 bytes, which is 32 bytes for the headers and 25 bytes for the minimal JSON data of `{"asset":{"dimension":4}}`. However, such a file contains no data, and is not useful.

Following all of the above rules, the data layout of a G4MF binary file can be summarized as follows:

| Offset in bytes | Size in bytes | Description                                       | Valid values                                     |
| --------------- | ------------- | ------------------------------------------------- | ------------------------------------------------ |
| 0               | 4             | The G4MF file header's magic number.              | Constant `G4MF` or `0x47 0x34 0x4D 0x46`         |
| 4               | 4             | The G4MF file header's version number.            | Constant based on the spec version               |
| 8               | 8             | The G4MF file header's size in bytes.             | Between 32 and 2^64 - 1                          |
| 16              | 4             | The first chunk's chunk type.                     | Constant `JSON` or `0x4A 0x53 0x4F 0x4E`         |
| 20              | 4             | The first chunk's compression format.             | Constant `0x00000000` for uncompressed           |
| 24              | 8             | The first chunk's size in bytes.                  | Between 0 and 2^64 - 33                          |
| 32              | N             | The first chunk's data, the G4MF JSON data.       | UTF-8 encoded JSON excluding control characters  |
| 32 + N          | P1            | (optional) Padding if a second chunk exists.      | 0 to 15 null bytes or spaces to 16-byte boundary |
| 32 + N + P1     | 4             | (optional) The second chunk's type.               | Constant `BLOB` or `0x42 0x4C 0x4F 0x42`         |
| 36 + N + P1     | 4             | (optional) The second chunk's compression format. | Constant `0x00000000` for uncompressed           |
| 40 + N + P1     | 8             | (optional) The second chunk's size in bytes.      | Between 0 and 2^64 - (48 + N + P1)               |
| 48 + N + P1     | M             | (optional) The second chunk's data.               | Binary blob data                                 |
| 48 + N + M + P1 | P2            | (optional) Padding if a third chunk exists.       | 0 to 15 null bytes or spaces to 16-byte boundary |

More chunks may follow the second chunk, including additional BLOB chunks for buffers, or any other chunk type.
