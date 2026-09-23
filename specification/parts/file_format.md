# G4MF File Format

There is no such thing as a `.g4mf` file. The name "G4MF" describes the overall specification and contents, not a specific storage layout. G4MF files can be stored either in the JSON-based text format with the `.g4tf` extension, or in the binary format with the `.g4b` extension.

## Text File Format

G4MF files may be stored in a JSON-based text format with the `.g4tf` file extension, known as "text G4MF" or "G4MF Text File Format".

With the text format, buffers may only refer to their data with the `"uri"` property. This data may be stored in the form of a base64-encoded data URI within the JSON, referenced as external files via a relative path, or any other URI scheme supported by the software.

Text G4MF files MUST NOT contain a byte-order mark (BOM), NUL bytes, or carriage returns (CR). Text G4MF files MUST NOT contain any other control characters, including but not limited to Unicode `0x00` through `0x1F`, and `0x7F` through `0x9F`, except for tab `0x09` and line feed `0x0A`. These only apply to the final encoding, individual strings may contain escaped versions of these.

Text G4MF files MUST end in a single line feed (LF) character, with no extra trailing blank lines. Text G4MF files MUST NOT contain trailing whitespace on any line, meaning that a LF character may not be preceded by a space or a tab.

A text G4MF file MUST be simultaneously a valid JSON file, a valid UTF-8 text file, and a valid POSIX-compliant text file (see note on `{LINE_MAX}` below). This is unlike the text version of glTF™ which only needs to be valid JSON and UTF-8, and is otherwise a byte stream, with no guarantees of being readable as a text file. Text G4MF files are required to be POSIX-compliant text files.

### Line Length Compliance

Various standards and transmission protocols impose limits on line lengths in text files. POSIX limits text file line lengths to a system-defined maximum, `{LINE_MAX}`. Since this varies by system, for the purposes of validating text G4MF files, `{LINE_MAX}` should be considered to be infinite or endless, and therefore ignored.

IANA-compliant text files (7-bit or 8-bit encoding) are limited to 998 octets per line, ready for transport via text protocols that impose 998 octet limits. If a file has lines exceeding this limit, IANA would consider the file to be binary, not text.

Text G4MF files are RECOMMENDED to follow the IANA line length restriction, with one exception: Long strings may cause lines to exceed the 998-octet line length limit. Otherwise, it would not be possible to encode long strings, particularly important for large base64-encoded data URIs. Exporters SHOULD insert line breaks between JSON tokens to try and keep lines within 998 octets.

Additionally, IANA defines text files as having lines delimited by CRLF, while the line endings of G4MF are LF (`0x0A`) only. Carriage returns may need to be inserted when transmitting over protocols that expect CRLF line endings. This is a trivial and lossless transformation, which can be performed automatically on each end, in order to support IANA-compliant text file transmission.

Following the line length recommendation ensures that text G4MF files without long strings remain IANA-compliant text files except for the line endings. In files with large data URIs, keeping line lengths low for most of the file allows the file to be converted into a compliant form by replacing the data URIs with external file paths, assuming all other strings are already within the recommended limit.

Furthermore, limiting line lengths makes it easier to view and edit text G4MF files in text editors, a nice benefit even without considering specific hard limits required for compliance with standards. A text G4MF file SHOULD NOT be a several-megabyte blob of JSON shoved onto one line.

## Binary File Format

G4MF files may be stored in a binary format with the `.g4b` file extension, known as "binary G4MF" or "G4MF Binary File Format".

With the binary format, binary blobs of data may be stored in the same ways as in text G4MF, a `"uri"` property with a data URI or path to external file. Additionally, the binary format allows for buffer data to be stored in chunks, and referenced by buffers using the `"chunk"` property. Chunk-stored data is a much more compact representation of the same data, and is highly recommended. Binary G4MF files with base64-encoded data URIs are valid, but strongly discouraged.

The binary format begins with a 16-byte file header, which contains the following fields:

- A 4-byte magic number.
  - This MUST be equal to the byte sequence `0x47 0x34 0x4D 0x46`, or ASCII string "G4MF".
  - When interpreted as a little-endian unsigned 32-bit integer, this is `0x464D3447`.
- A 4-byte version integer.
  - This MUST be equal to the byte sequence `0x00 0x00 0x00 0x00`, or zero.
  - This value is only 0 for the draft version of the specification. The final version will have a different value.
- A 8-byte size integer.
  - This MUST be equal to the total size in bytes of the entire file, including the file header, all chunks, all JSON data, and all binary blobs of data.
  - This value is a little-endian unsigned 64-bit integer, with the most significant bit set to zero. The maximum file size of a binary G4MF file is 2^63 - 1 bytes.

After the file header, the file consists of a series of one or more chunks. Each chunk begins with its own 16-byte chunk header, with a similar format to the file header:

- A 4-byte chunk type indicator.
  - In the base specification, this MUST be one of the following:
    - The byte sequence `0x4A 0x53 0x4F 0x4E`, the ASCII string "JSON". This indicates the chunk contains JSON data.
      - When interpreted as a little-endian unsigned 32-bit integer, this is `0x4E4F534A`.
      - JSON chunks MUST be UTF-8 encoded without a BOM, MUST NOT contain control characters (including but not limited to Unicode `0x00` through `0x1F`, and `0x7F` through `0x9F`) except for optionally tab `0x09` and line feed `0x0A`, and MUST be a valid JSON object. These requirements also apply to the text format.
    - The byte sequence `0x42 0x4C 0x4F 0x42`, the ASCII string "BLOB". This indicates the chunk contains binary blob data, usually the data of a buffer.
      - When interpreted as a little-endian unsigned 32-bit integer, this is `0x424F4C42`.
  - Implementations MAY define additional chunk types, but this is usually not needed. The byte sequence selected SHOULD be a somewhat-human-readable magic sequence of printable ASCII characters, but may be any value. Note: This does not need to match the magic number used by the data format itself, if any.
- A 4-byte chunk encoding indicator.
  - In the base specification, this MUST be one of the following:
    - The byte sequence `0x00 0x00 0x00 0x00`, or zero. This indicates the chunk is plainly encoded, meaning not compressed or encrypted.
    - The byte sequence `0x5A 0x73 0x74 0x64`, the ASCII string "Zstd". This indicates the chunk is compressed using the Zstandard compression format.
      - When interpreted as a little-endian unsigned 32-bit integer, this is `0x6474735A`.
      - The chunk data MUST also include Zstd's own magic number `0x28 0xB5 0x2F 0xFD` at the start of the data, it cannot be omitted.
  - The byte sequence `0xFF 0xFF 0xFF 0xFF` is reserved as an error value, and MUST NOT be used as an encoding indicator, or else the file is invalid.
  - If the chunk represents the data of a buffer, this MUST match the `"encoding"` property in the G4MF JSON data for that buffer, with the property undefined for plainly encoded data.
  - Implementations MUST support the plainly encoded format. Implementations MAY choose to implement any or none of the other encoding formats, refusing to load any files with unsupported encodings, such as compression or encryption.
  - Implementations MAY define additional encoding formats. The byte sequence selected SHOULD be a somewhat-human-readable magic sequence of printable ASCII characters, but may be any value. Note: This does not need to match the magic number used by the encoding format itself, if any.
- A 8-byte chunk data size integer.
  - This MUST be equal to the size in bytes of the chunk data, excluding the chunk header, and excluding any padding after the chunk data.
  - This value is a little-endian unsigned 64-bit integer, with the most significant bit set to zero. The maximum chunk data size is 2^63 - 33 bytes (an additional 32 bytes are subtracted for the file and chunk headers).
  - If the chunk is encoded differently, such as compressed or encrypted, this value is the size of the encoding data, not the plain data within. However, the `"byteLength"` field in the JSON data refers to the plainly encoded size of the data after decoding, such as decompression or decryption.
- The data in each chunk immediately follows the chunk header, and is of the size in bytes indicated by the chunk data size number.

Every chunk header MUST be aligned to a 16-byte boundary. This means that whenever a chunk has another chunk after it, the preceding chunk MUST have padding placed after the data (not necessarily included in the chunk data size) to the next 16-byte boundary (if already at the boundary, there is no padding). The final chunk in the file does not need padding after it. Padding is usually null `0x00` bytes for binary blobs or non-plainly-encoded chunks, but space `0x20` characters SHOULD be used for padding plainly encoded JSON data. The 8-byte chunk data size number MUST NOT include this padding, it only includes the used bytes of the chunk data.

The G4MF file header magic number, chunk header type indicators, and chunk header encoding indicators are all [FourCC](https://en.wikipedia.org/wiki/FourCC) codes. This allows for easy identification of the headers if a human inspects the file in a hex editor. Implementations MAY choose to display these values to the user as plain text, such as by showing the encoding indicator in an error message when the encoding format is unsupported.

A G4MF file MUST contain one chunk for the G4MF JSON data that conforms to the main G4MF schema `g4mf.schema.json`. This chunk can be identified as the first chunk of type "JSON" in the file, which is not necessarily the first chunk overall. If the file has binary blob chunks containing G4MF buffers, they SHOULD be the following chunks in the file, but may occur in any order. The buffers in the G4MF JSON data's buffers array usually refer to these chunks explicitly using the `"chunk"` property, which implies that `"uri"` is not defined in that buffer. The buffer's `"byteLength"` always refers to the decoded size of the data, excluding any compression or encryption, but the binary chunk's data size refers to the encoded size of the data, including any compression or encryption.

The most common case of a binary G4MF (`.g4b`) layout has the G4MF JSON chunk at index `0`, and one additional chunk containing a blob of buffer data at index `1`. Such a case will have the `"chunk"` property of the first buffer set to `1`, such that the G4MF JSON will contain `{"buffers":[{"byteLength":12345,"chunk":1}]}`, where `12345` should be replaced with the decoded size of the buffer data in bytes. Multiple buffers may be included, which may use multiple chunks, and the chunks may be in any order. The behavior of additional custom chunks not used by buffers is undefined, and may be used for any purpose.

Binary G4MF files smaller than 32 bytes are invalid, because that is the minimum size of the file header and the first chunk header. The minimum possible size of a valid plainly encoded G4MF binary file is 57 bytes, which is 32 bytes for the headers and 25 bytes for the minimal JSON data of `{"asset":{"dimension":4}}`. However, such a file contains no data, and is not useful.

Following all of the above rules, the data layout of a typical G4MF binary file can be summarized as follows:

| Offset in bytes | Size in bytes | Description                                       | Valid values                                       |
| --------------- | ------------- | ------------------------------------------------- | -------------------------------------------------- |
| 0               | 4             | The binary G4MF file header's magic number.       | Constant `G4MF` or `0x47 0x34 0x4D 0x46`           |
| 4               | 4             | The binary G4MF file header's version number.     | Constant based on the spec version                 |
| 8               | 8             | The binary G4MF file size in bytes.               | Between 32 and 2^63 - 1                            |
| 16              | 4             | The first chunk's chunk type.                     | Constant `JSON` or `0x4A 0x53 0x4F 0x4E`           |
| 20              | 4             | The first chunk's encoding indicator.             | Constant `0x00000000` for plain, or another format |
| 24              | 8             | The first chunk's size in bytes.                  | Between 0 and 2^63 - 33                            |
| 32              | N             | The first chunk's data, the G4MF JSON data.       | UTF-8 encoded JSON excluding control characters    |
| 32 + N          | P1            | (optional) Padding if a second chunk exists.      | 0 to 15 null bytes or spaces to 16-byte boundary   |
| 32 + N + P1     | 4             | (optional) The second chunk's type.               | Constant `BLOB` or `0x42 0x4C 0x4F 0x42`           |
| 36 + N + P1     | 4             | (optional) The second chunk's encoding indicator. | Constant `0x00000000` for plain, or another format |
| 40 + N + P1     | 8             | (optional) The second chunk's size in bytes.      | Between 0 and 2^63 - (48 + N + P1)                 |
| 48 + N + P1     | M             | (optional) The second chunk's data.               | Binary blob data                                   |
| 48 + N + M + P1 | P2            | (optional) Padding if a third chunk exists.       | 0 to 15 null bytes or spaces to 16-byte boundary   |

More chunks may follow the second chunk, including additional BLOB chunks for buffers, or any other chunk type.

For the file size number, and the size of all chunks, the most significant bit is reserved for future use, and MUST be set to zero. Implementations MUST reject files or chunks where this bit is set to one. This allows for future expansion of the specification to support larger files, such as 128-bit file sizes or beyond, without breaking compatibility, in a similar manner to how UTF-8 extends ASCII. Restricting the file size to 63 bits also permits using signed 64-bit integers, which is important for many programming languages without unsigned integer types, and allows using -1 as a sentinel value for "unknown size" in code that processes G4MF files.
