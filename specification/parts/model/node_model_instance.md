# G4MF Node Model Instance

## Overview

G4MF allows referencing external model files. These model files may then be instanced on 0 or more nodes in the scene hierarchy using the `"modelInstance"` property on nodes. Each model instance MAY specify overrides for nodes and materials within the referenced model, allowing for per-instance customization.

See [G4MF Model File Reference](model_file_ref.md) for the details of the data within each model.

## Example

The following example defines.

## Properties

| Property                   | Type      | Description                                                                      | Default                      |
| -------------------------- | --------- | -------------------------------------------------------------------------------- | ---------------------------- |
| **materialOverrides**      | `object`  | A map of unique material names to overrides for materials within the model.      | `{}` No material overrides.  |
| **model**                  | `integer` | The index of the model that this node references.                                | Required, no default.        |
| **nodeAdditionalChildren** | `object`  | A map of unique node names to arrays of host node indices to append as children. | `{}` No additional children. |
| **nodeOverrides**          | `object`  | A map of unique node names to overrides for nodes within the model.              | `{}` No node overrides.      |

### Material Overrides

The `"materialOverrides"` property is an object that allows per-instance customization of materials within the referenced model. If not defined, the model instance uses all materials from the source model without modification.

Each key in the `"materialOverrides"` object is the name of a material in the source model, and the value is an object containing properties that override or extend that material. Override properties are merged with the original material's properties, with the override values taking precedence.

See [G4MF Material](../mesh/material.md) for more information about materials, and see [Override Mechanism](#override-mechanism) below for details on how overrides are applied.

### Model

The `"model"` property is an integer index that references a model in the document-level `"models"` array. This property is required and has no default value.

Each model is a [G4MF File Reference](../core.md#file-references) which points to a file containing the model data, with valid target files being anything that can be instantiated as a node or hierarchy of nodes, such as another G4MF file. See [G4MF Model File Reference](model_file_ref.md) for the details of the properties found on each model, which are referred to by index in each model instance.

### Node Additional Children

The `"nodeAdditionalChildren"` property is an object that allows appending host nodes as children of specific nodes within the referenced model. If not defined, the model instance uses only the children defined by the source model.

Each key in the `"nodeAdditionalChildren"` object is the name of a node in the source model, and the value is an array of [G4MF Integer Index Identifiers](../core.md#integer-index-identifiers) indices referencing nodes in the host G4MF file. These nodes are appended to the end of the children list of the corresponding node during instantiation. This property is additive only and does not replace or remove the source model's children. To replace the children entirely, use `"nodeOverrides"` to set the `"children"` array. To remove only some child nodes from the instance, set that node's override to `null` in `"nodeOverrides"`.

### Node Overrides

The `"nodeOverrides"` property is an object that allows per-instance customization of nodes within the referenced model. If not defined, the model instance uses all nodes from the source model without modification.

Each key in the `"nodeOverrides"` object is the name of a node in the source model, and the value is an object containing properties that override or extend that node. Override properties are merged with the original node's properties, with the override values taking precedence.

The root node of the model MAY be included in `"nodeOverrides"` to override its component properties, but it MUST NOT be `null`, and it MUST NOT have its transform or visible properties overridden. The `"position"`, `"basis"`, `"rotor"`, `"scale"`, and `"visible"` properties of the model instance's root node are always determined by the model instance node itself; any such properties in the root node's override would be invalid. This is because the model instance node represents the root of the instantiated model in the scene hierarchy, with the children of the root node of the model placed as the children of the model instance node, since they are the same node. Note that the model instance node's children property effectively "concatenates" the set of children with those in the model, meaning that if it was desired to delete all of the children, an override would be needed. Furthermore, component properties like physics body mass would need to be specified via the root node override due to the rules of mutual exclusivity, where a node cannot have both the `"modelInstance"` and `"physics"` properties defined.

See [G4MF Node](../node.md) for more information about nodes, and see [Override Mechanism](#override-mechanism) below for details on how overrides are applied.

## Override Mechanism

The following rules apply to all overrides in model instances, including node overrides, and all other overrides.

### Keys: Unique Names

Overrides keys use names rather than indices for stability. Per the [G4MF Item Name](../core.md#name) specification, all names are unique within G4MF models. If referencing a non-G4MF model format such as glTF™, only items with unique names are valid targets for overrides. If a name in the override does not exist in the source model, implementations SHOULD produce a warning, and the override MAY be ignored, or MAY be salvaged in a "missing" object.

### Values: Override Properties

When override properties are merged, the resulting combined object MUST satisfy all requirements of all schemas, including mutual exclusivity rules.

- For example, a node that is a mesh instance cannot have camera properties added via overrides, since nodes cannot be both a mesh and a camera simultaneously, as indicated by the `"camera"` and `"meshInstance"` properties being mutually exclusive in the node schema.
- For example, if a model contains a node with `"bone": {}`, and a model instance contains an override with `"bone": { "shape": 0 }`, then this is invalid, because the `"shape"` requires the `"length"` property to also be defined, which is not present in either the original node or the override; to make this valid, either the model or the override would need to define the `"length"` property as well.

When merging override properties, the following rules apply:

- All [G4MF Integer Index Identifiers](../core.md#integer-index-identifiers) (indices) in override properties refer to the document-level arrays of the host G4MF file, not the referenced model file. For example, if a model contains a mesh instance node, and the model instance overrides the material to use index `0`, then that refers to the first material in the host G4MF file's `"materials"` array, not the model file's materials.

- All non-null object types have their items merged recursively. This includes the overridden object itself, implying that partial overrides are valid and expected. For example, if a model contains a node with `"physics": { "motion": { "type": "dynamic" } }`, and a model instance contains an override with `"physics": { "motion": { "mass": 5.0 } }`, then the resulting node will have `"physics": { "motion": { "type": "dynamic", "mass": 5.0 } }`.

- All object types that are `null` in the override MUST be treated as removing that object, as if the property was never defined. This includes the overridden object itself. For example, if a model contains a node with `"physics": { "motion": { "type": "dynamic" } }`, and a model instance contains an override with `"physics": null`, then that node in the model instance will have no physics properties at all. If those were the only properties defined on that node, the resulting node will just be `{}`. For example, if a model instance contains an override of `null`, then that node in the model will be excluded entirely from the model instance, removing/deleting that node from the resulting scene hierarchy.

- All other property types (strings, numbers, booleans, arrays, etc) are replaced with the override value. For example, if a model contains a node with `"visible": true`, and a model instance contains an override with `"visible": false`, then that node in the model instance will be invisible. For example, if a model contains a node with `"position": [1, 2, 3, 4]`, or any other position value, and a model instance contains an override with `"position": [5, 6, 7, 8]`, then that node's position will be `[5, 6, 7, 8]`, ignoring the original position defined by the model's own content.

  - Note that if the arrays contain IDs, these are indices in the host G4MF file. For example, if a model contains a node with `"children": [1, 2]`, and a model instance contains an override with `"children": [3]`, then that node will only have node 3 from the host G4MF file as its child. In order to add node 3 as an additional child, rather than replacing the entire children array, use the `nodeAdditionalChildren` property instead. In order to delete only some nodes from the resulting scene hierarchy, override the unwanted nodes with `null` in the `nodeOverrides` property.

When the target model is not a G4MF file, the override properties MUST still conform to the G4MF core schemas or G4MF extension schemas, and may need to be remapped or translated by implementations. For example, if a glTF™ model is instanced by a G4MF file, and a node override specifies the `"position"` property, this corresponds to the glTF™ node's `"translation"` property. Similarly, if a node override specifies the `"rotor"` property, the corresponding glTF™ property is `"rotation"`, but the components would need to be swizzled and negated to convert between G4MF's rotor format (scalar, xy, xz, yz, etc) and glTF™'s quaternion format (x, y, z, w) to match up at runtime, so long as the data in the host G4MF file's rotor is in the G4MF rotor format.

## JSON Schema

- See [g4mf.node.model_instance.schema.json](../../schema/g4mf.node.model_instance.schema.json) for the node model instance properties JSON schema.
- See [g4mf_file_ref.schema.json](../../schema/g4mf_file_ref.schema.json) for the file reference properties JSON schema.
