# G4MF Asset

## Overview

G4MF files MUST have an `"asset"` property in their top-level JSON object which defines metadata about the file.

## Example

At a minimum, the G4MF JSON data MUST contain `"asset"` with `"dimension"` defining the dimension of the model. This example defines an empty 4D G4MF file:

```json
{
	"asset": {
		"dimension": 4
	}
}
```

## Properties

| Property               | Type       | Description                                                      | Default                      |
| ---------------------- | ---------- | ---------------------------------------------------------------- | ---------------------------- |
| **dimension**          | `integer`  | The dimension of the model as an integer.                        | Required, no default.        |
| **extensionsRequired** | `string[]` | An array of extensions required to load the file.                | `[]` No required extensions. |
| **extensionsUsed**     | `string[]` | An array of extensions used in the file.                         | `[]` No used extensions.     |
| **generator**          | `string`   | The name of the application that generated the file.             | `""` (empty string)          |
| **version**            | `string`   | The version of the G4MF specification used to generate the file. | `""` (empty string)          |

### Dimension

The `"dimension"` property is an integer that defines the dimension of the model. This property is required.

All data in the file MUST be in the same dimension as the model, such as node transforms, mesh vertices, and so on.

If `"dimension"` is not defined or is not an integer, the file is not a valid G4MF file. Implementations MAY only support any subset of dimensions, such as only 4D, only 5D, or even only 3D. Implementations MAY choose to entirely ignore files with unsupported dimensions, or read them discarding the unsupported dimensions.

### Extensions Required

The `"extensionsRequired"` property is an array of strings that defines the extensions required to load the file. This property is optional and defaults to an empty array.

If an extension is required and an implementation does not support that extension, the implementation MUST NOT load this file, and instead SHOULD return an error. If an extension is required, it MUST also be listed in the `"extensionsUsed"` array.

### Extensions Used

The `"extensionsUsed"` property is an array of strings that defines the extensions used in the file. This property is optional and defaults to an empty array.

If an extension is used in `"extensions"` anywhere in the file, or in `"extensionsRequired"`, it MUST be listed here.

### Generator

The `"generator"` property is a string that defines the name of the application that generated the file. This property is optional and defaults to an empty string.

This property is highly recommended to be set to a human-readable name of the application and any addons/plugins that were used to generate the file. It SHOULD also contain the version of the application and any addons/plugins, if possible.

### Version

The `"version"` property is a string that defines the version of the G4MF specification used to generate the file.

Since the specification is still a draft and in active development, this property may be omitted. In the future, this will be a required property.

## JSON Schema

See [g4mf.asset.schema.json](../schema/g4mf.asset.schema.json) for the asset properties JSON schema.
