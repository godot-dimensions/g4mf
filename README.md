# Good 4D Model Format (G4MF)

Good 4D Model Format, or G4MF for short, is a JSON-based 4D-focused multi-dimensional model format inspired by Khronos's [glTF™](https://github.com/KhronosGroup/glTF), allowing for transmission, interchange, and interoperability of higher dimensional content between applications.

G4MF files can come in the following types:
- `.g4tf` stands for "Good 4D model Text File". It includes the JSON data in a purely text-based UTF-8 format, with binary blobs encoded as Base64 inside of a string. Valid G4TF files do not contain BOMs or carriage returns.
- `.g4b` stands for "Good 4D model Binary". It densely packs the binary data for size efficiency, at the cost of making it harder to inspect in a text editor.

Compared to glTF, G4MF adds a new required integer key `"dimension"` to `"asset"`, which MUST be defined or the file is invalid. This means that 4D models MUST have `{ "asset": { "dimension": 4 } }` in their JSON data. Aside from that, the overall structure is very similar to glTF™ with a few minor differences, such as only having one scene per file, only having one root node, node transforms using position and either basis or rotor+scale instead of translation+quaternion+scale or a matrix, and using a 64-bit integer for the size of `.g4b` files instead of a 32-bit integer like `.glb`.
