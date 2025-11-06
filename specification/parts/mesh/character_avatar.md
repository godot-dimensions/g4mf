# G4MF Characters/Avatars

## Overview

G4MF is a general-purpose model format, which includes the ability to be used as a character or avatar. When used in this way, there are standards that should be followed to ensure it can be used correctly by runtimes without needing to be configured after import.

For example, a character animation needs to know which bones are used for the arms, legs, and head. For example, lip syncing needs to know which visemes are available. This information is specified by using specific naming conventions.

A complete character/avatar standard would include more than what is defined here, such as eye look angle limits, cartoony facial expressions, node constraints, spring bones, and more. However, those features are intentionally excluded from the base G4MF specification, and instead may be introduced as extensions. The base G4MF specification's definition of characters/avatars ends at providing guidance on how to use its general non-character-specific G4MF features to represent characters/avatars in a way that is interoperable, including G4MF meshes, nodes, skeletons, and blend shapes.

## Bipedal Humanoid Skeleton Bone Hierarchy

Most characters/avatars are bipedal, with a humanoid skeleton. When animating such characters, applications need to know which bones correspond to which body parts. Many importers allow specifying a bone mapping manually, but in G4MF, standardized bone names are used to provide this mapping, not a separate data structure.

Bipedal humanoid skeletons are commonly needed even for non-bipedal characters/avatars, since they often need to work with bipedal humanoid animations, or be controlled by a human in VR, and real-life humans unavoidably have bipedal humanoid skeletons. Therefore, bipedal humanoid skeletons are defined in the base G4MF specification, and other skeleton types may be defined separately as extensions, or adapted from the bipedal humanoid skeleton. For example, a taur character may have extension-defined constraints that copy the front leg rotation to the rear legs, with the front legs using the bipedal humanoid skeleton. For example, a blob character may exclude most of these bones to discard their animation, or have "dummy" bones with no mesh vertices weighted to them to keep the animation such that descendants of those bones move correctly.

The following tree structure is the bipedal humanoid bone structure defined by G4MF (all bones are optional):

- `Hips` (child of skeleton)
  - `LeftUpperLeg`
    - `LeftLowerLeg`
      - `LeftFoot`
        - `LeftToes`
  - `RightUpperLeg`
    - `RightLowerLeg`
      - `RightFoot`
        - `RightToes`
  - `Spine`, `Spine1`, etc.
    - `Chest`, `Chest1`, etc.
      - `Neck`
        - `Head`
          - `Jaw`
          - `LeftEye`
          - `RightEye`
      - `LeftShoulder`
        - `LeftUpperArm`
          - `LeftLowerArm`
            - `LeftHand`
              - `LeftThumbMetacarpal`, `LeftThumbProximal`, `LeftThumbDistal`, etc.
              - `LeftIndexMetacarpal` (optional), `LeftIndexProximal`, `LeftIndexIntermediate`, `LeftIndexDistal`, etc.
              - `LeftMiddleMetacarpal` (optional), `LeftMiddleProximal`, `LeftMiddleIntermediate`, `LeftMiddleDistal`, etc.
              - `LeftRingMetacarpal` (optional), `LeftRingProximal`, `LeftRingIntermediate`, `LeftRingDistal`, etc.
              - `LeftLittleMetacarpal` (optional), `LeftLittleProximal`, `LeftLittleIntermediate`, `LeftLittleDistal`, etc.
      - `RightShoulder`
        - `RightUpperArm`
          - `RightLowerArm`
            - `RightHand`
              - `RightThumbMetacarpal`, `RightThumbProximal`, `RightThumbDistal`, etc.
              - `RightIndexMetacarpal` (optional), `RightIndexProximal`, `RightIndexIntermediate`, `RightIndexDistal`, etc.
              - `RightMiddleMetacarpal` (optional), `RightMiddleProximal`, `RightMiddleIntermediate`, `RightMiddleDistal`, etc.
              - `RightRingMetacarpal` (optional), `RightRingProximal`, `RightRingIntermediate`, `RightRingDistal`, etc.
              - `RightLittleMetacarpal` (optional), `RightLittleProximal`, `RightLittleIntermediate`, `RightLittleDistal`, etc.

**Important note:** G4MF requires that all names are unique within the file, including node names. Therefore, nodes may be named either exactly as above, or with a prefix of the character name. For example, if two characters "Alice" and "Bob" exist in the same file, "Alice" would have `AliceHips`, `AliceSpine`, etc, and "Bob" would have `BobHips`, `BobSpine`, etc. This ensures that names are always both predictable and unique. If only "Alice" exists in the file, its bones may either be named `Hips` or `AliceHips`, and so on for the other bones. Each of the above names is unique enough to allow for implementations to use `String.endsWith()` or similar to identify the bones, regardless of the presence of a prefix.

Usage rules:

- All of the defined bones are optional. A character/avatar may have only a subset of these bones, in which case any runtime application animating those bones will simply have that part of the animation discarded. For example, a character may not have any finger bones, in which case finger animation will be discarded.

- Extra bones may exist, both added onto the tree, or added between defined bones. For example, a character may have extra bones existing between `Neck` and `Head`, or between `LeftUpperLeg` and `LeftLowerLeg`, and the hierarchy is still considered valid. However, defined bones MUST be descendants of their defined parent bones. For example, if both `Head` and `Neck` exist, `Head` MUST be a descendant of `Neck`, even if there are extra bones in between.

- If a skeleton bone exists for one of these listed bones, it MUST have its name set to the corresponding name from the tree above (or that name with a prefix) in order to be used as that bone in an application's skeletal animations. The names are case-sensitive. This ensures that applications can reliably identify and use the bones by their names.

- If a skeleton bone is needed that is not defined here, they may still be added to the hierarchy, however, not all runtime applications will recognize or use them. This standard is not intended to limit future expansion with new skeleton bones for advanced character rigs, but rather to ensure a common baseline for compatibility.

- The camera position is defined as the midpoint of the `LeftEye` and `RightEye` bones, if they exist. If they do not exist, it is assumed to be at nearest ancestor, meaning: the `Head` bone position if `Head` exists (or checking for numbered variants), else the `Neck` bone position if `Neck` exists (or checking for numbered variants), and so on. This applies both to first-person cameras, and the orbited point of third-person cameras. To avoid undesired camera shake, for third-person cameras, this position is RECOMMENDED to be determined once when the character/avatar is loaded, and kept at that same position relative to the character/avatar, ignoring any subsequent animation of the hips/spine/chest/neck/head/eye bones.

- The `Jaw` bone is unused if the avatar includes viseme blend shapes, AND the application supports visemes. A character/avatar may include both a `Jaw` bone and viseme blend shapes to support applications that only support one or the other, but runtime applications MUST pick one or the other, not both.

- If a skeleton bone exists but is not supported by an application or format, it may be safely ignored. For example, an application which does not animate fingers may ignore finger bones. For example, if a character includes `Spine1` and `Spine2`, but an application only supports a single `Spine` bone, it may ignore `Spine1` and `Spine2`, and animate only `Spine`.

- When a bone has no siblings, it SHOULD have its local position set to a vector with its Y component equal to the length of the parent bone, and all other axes set to `0.0`, when possible, or close to that value. This ensures that the start of each bone is at the end of its parent bone, since all bones point in their local +Y direction with the specified bone length. For example, if `RightUpperArm` has a length of `0.3`, the local position of `RightLowerArm` is RECOMMENDED to have its Y component set to `0.3`, and other components set to 0. However, this is NOT required; bones may be positioned arbitrarily. This recommendation does not apply to bones with siblings, since the upper leg bones, shoulder bones, and finger bones are often not connected to the end of their parents. Remember that, like all G4MF nodes, bone transforms are defined relative to their parent's transform, not relative to the end of the parent bone, therefore changing the length of a bone does not affect the position of its children.

- The metacarpal finger bones are used to connect the hand to the fingers, and are optional for the non-thumb fingers. They may be rotated slightly in detailed realistic hand simulations, but in most applications, they SHOULD usually be left alone. For example, in a VR game with finger tracking, `LeftIndexProximal` SHOULD be animated, but `LeftIndexMetacarpal` SHOULD NOT be animated. For the thumb, the metacarpal bone is important, it SHOULD be included in the hands of realistic characters, and SHOULD be animated in all applications with finger tracking and/or finger animations.

- If a skeleton bone is intended to optionally provide more precision or detail to a defined bone, it SHOULD be named with a numbered suffix of the defined bone name, it MUST be a descendant of that defined bone, and any defined child bones MUST be descendants of all such bones. These are defined to allow for more detailed spine rigs, while this hierarchy ensures that if an application only supports a single bone of that type, such as `Spine` and/or `Chest`, it may simply ignore the numbered variants, since they will move together with their parent bone. The bones explicitly listed in the tree above are commonly needed, and additional numbered bones are less commonly needed, but still allowed. The base bones themselves, such as `Spine` and `Chest`, may be thought of as `0` like "Spine0" and "Chest0", but this MUST NOT be explicitly written in the file, as only `Spine` and `Chest` are recognized names. For example, instead of an "UpperChest" bone, G4MF defines an optional `Chest1` bone which, if present, MUST be a child of `Chest`. Optionally, if further numbered bones are present (not commonly needed), they MUST be a child of the previous number, like `Chest2` as a child of `Chest1`. Then the `Neck`, `LeftShoulder`, and `RightShoulder` bones MUST be descendants of the last `Chest` bone, whether that is `Chest` or `Chest1` or further numbered variants. For example, a character with a long flexible neck may have `Neck`, `Neck1`, `Neck2`, and so on bones, with `Head` being a child of the last `Neck` bone, while applications which only support a single `Neck` bone may ignore the numbered variants.

- The inverse bind matrix of each bone is defined by the bone's position when the character/avatar is loaded. Therefore, the pose of the bone nodes saved in the file MUST match the pose of the mesh, such as T-pose bones on a T-pose mesh, or A-pose bones on an A-pose mesh. Non-baked poses are not supported by the base G4MF specification, but may be defined in extensions by overriding the transforms of the bones _after_ the character/avatar is loaded and the inverse bind matrices are calculated, so long as the transforms of the bones in the file are in a rest pose matching the mesh, to ensure that the calculated inverse bind matrices are correct.

The G4MF bipedal humanoid skeleton is designed to be minimally different from other existing standards, however since the existing standards differ from each other, some differences are unavoidable. For convenience, here are some other standards and how to convert them to G4MF, with names from those standards quoted in `"`, and the names from G4MF in backticks:

- To convert from a VRM humanoid rig: Replace "upperChest" with `Chest1` if present. The rest of the bones have the same names, but you must capitalize the first letter of each bone name to use PascalCase instead of camelCase, so "leftUpperLeg" becomes `LeftUpperLeg`, and so on.

- To convert from a Godot humanoid skeleton: Replace "UpperChest" with `Chest1` if present. The rest of the bones have the same names, with the same capitalization.

- To convert from a Unity humanoid rig: Replace the "Proximal", "Intermediate", and "Distal" suffixes with absent or numbered suffixes as described above. Replace "Upper Chest" with `Chest1` if present. The rest of the bones have the same names, but you must removes spaces from the names.

- To convert from a Mixamo rig: Replace "Spine2" with `Chest`, replace "LeftUpLeg" with `LeftUpperLeg`, replace "LeftLeg" with `LeftLowerLeg`, replace "LeftArm" with `LeftUpperArm`, replace "LeftForeArm" with `LeftLowerArm`, and the same for the right side. Replace the numbered finger bones with the explicit names defined above. The rest of the bones have the same names, with the same capitalization.

// TODO: Collaborate with Khronos, Metaverse Standards Forum, and more to define an industry-wide standard. Existing standards vary, let's try not to fragment further.

// TODO: Define bone roll orientation. For example, if the spine's +Y axis points up, should its +Z axis point to the front of the character, or what? Existing standards vary on this. This is important to define, otherwise animations may not work correctly in simple implementations that cannot retarget the animation to match the bone roll orientation.

### Skeleton References

- Unity Avatar Mapping https://docs.unity3d.com/6000.2/Documentation/Manual/class-Avatar.html
- Godot SkeletonProfileHumanoid https://docs.godotengine.org/en/stable/classes/class_skeletonprofilehumanoid.html
- VRM Humanoid Bones https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/humanoid.md#list-of-humanoid-bones
  - Schema https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/schema/VRMC_vrm.humanoid.humanBones.schema.json

## Viseme Blend Shape Naming

Visemes, short for "visual phonemes", are blend shapes that represent the visual aspect of phonemes during human speech. They are used for lip syncing, the process of matching a character's mouth movements to spoken words.

The following viseme names are defined by G4MF, as a superset of common viseme sets found in other standards linked below:

| Viseme Name | IPA Phonemes    | Example Words                                              | Description                         |
| ----------- | --------------- | ---------------------------------------------------------- | ----------------------------------- |
| `VisemeSIL` | (silence)       | (silence)                                                  | Neutral, lips closed and relaxed    |
| `VisemePP`  | p, b, m         | **p**at, **b**at, **m**at                                  | Lips fully closed, bilabial closure |
| `VisemeFF`  | f, v            | **f**at, **v**at                                           | Lower lip touches upper teeth       |
| `VisemeTH`  | ð, θ            | **th**is, **th**in                                         | Tongue between teeth                |
| `VisemeDD`  | t, d            | **t**ip, **d**ip                                           | Tongue tip touches alveolar ridge   |
| `VisemeKK`  | k, ɡ            | **k**id, **g**o                                            | Back of tongue touches soft palate  |
| `VisemeCH`  | t͡ʃ d͡ʒ ʃ ʒ t͡s d͡z | **ch**at, **j**am, **sh**e, vi**s**ion, ca**ts**, ki**ds** | Lips rounded, jaw lowered slightly  |
| `VisemeSS`  | s, z            | **s**it, **z**oom                                          | Teeth almost together, lips wide    |
| `VisemeNN`  | n, l            | **n**ot, **l**ot                                           | Tongue presses ridge, lips apart    |
| `VisemeRR`  | ɹ, ɻ, r         | **r**ed (varies by accent)                                 | Lips slightly rounded, cheeks firm  |
| `VisemeWW`  | w, ʍ            | **w**hat, **hw**at (southern US accent)                    | Lips tightly rounded and protruded  |
| `VisemeYY`  | j, ʝ, ʎ         | **y**es, **j**a (Dutch), caba**ll**o (Spanish)             | Lips spread, tongue high front      |
| `VisemeAA`  | æ, ɑ, ɒ         | c**a**t, h**o**t, f**ou**ght (varies by accent)            | Oval mouth, jaw open                |
| `VisemeEE`  | ɛ, eɪ, e        | b**e**d, m**a**y, m**e**sa (Spanish)                       | Mouth wider, jaw open slightly      |
| `VisemeIH`  | ɪ, i            | t**i**p, t**ea**                                           | Lips spread, jaw high               |
| `VisemeOH`  | oʊ, o           | t**oe**, g**o** (Indian accent) or **eau** (French)        | Lips rounded, jaw open slightly     |
| `VisemeOU`  | u, ʊ            | b**oo**t, b**oo**k                                         | Lips rounded, slightly forward      |
| `VisemeUH`  | ə, ɜ, ʌ, ɐ      | **a**bout, b**i**rd, b**u**t, n**u**t (varies by accent)   | Mostly neutral, lips open slightly  |

Each example word corresponds to the listed phonemes in order. Some sounds may be merged in common English accents, in which cases a language or accent is specified in the table, otherwise the examples are based on General American English as spoken in the 21st century. For RR, those sounds are allophonic in English and most languages, therefore only one example word is provided, but the specific choice may vary by accent.

Usage rules:

- If a blend shape (morph target) exists for one of these listed visemes, it MUST have its name set to the corresponding name from the table above in order to be used as that viseme in an application's lip syncing. The names are case-sensitive. This ensures that applications can reliably identify and use the visemes by their names.

- If a viseme is needed that is not defined here, they may still be added as blend shapes, however, not all runtime applications will recognize or use them. This standard is not intended to limit future expansion with new visemes for new mouth shapes, but rather to ensure a common baseline for compatibility.

- If a runtime needs a viseme that is unavailable or missing, it may fall back to another viseme, or blend existing visemes, at the application's discretion. This includes the possibility of applications supporting custom visemes, with a fallback to this base definition to support characters/avatars without that custom viseme, and also allows applications to handle cases of missing visemes gracefully.

- If a viseme exists but is not supported by an application or format, it may be safely ignored. For example, VRM only defines AA, EE, IH, OH, and OU, so other visemes would not be used when converting a G4MF model to VRM.

- Visemes may be used for purposes other than lip syncing. For example, "VisemeWW" may be used as part of a "pog champ" facial expression.

The G4MF viseme blend shape naming is designed to be close to other existing standards. For convenience, here are some other standards and how to convert them to G4MF, with names from those standards quoted in `"`, and the names from G4MF in backticks:

- To convert from VRM lip sync visemes: Capitalize the viseme names, and add the `Viseme` prefix, then the names match.

- To convert from MPEG-4 FBA visemes: Replace "E" with `EE`, capitalize the viseme names, and add the `Viseme` prefix, then the names match.

- To convert from VRChat visemes: Replace "e" with `EE`, replace "i" with `IH`, replace "o" with `OH`, replace `u` with `OU`, capitalize the viseme names, and add the `Viseme` prefix, then the names match.

- To convert from Meta Horizon visemes: Replace "E" with `EE`, replace "I" with `IH`, replace "O" with `OH`, replace "U" with `OU`, capitalize the viseme names, and add the `Viseme` prefix, then the names match. Meta Horizon matches VRChat except for capitalization.

### Viseme References

- VRChat Visemes https://wiki.vrchat.com/wiki/Visemes and https://creators.vrchat.com/avatars/animator-parameters/#viseme-values
- MPEG-4 Face and Body Animation (FBA) https://visagetechnologies.com/uploads/2012/08/MPEG-4FBAOverview.pdf
- Meta Horizon Visemes https://developers.meta.com/horizon/documentation/unity/audio-ovrlipsync-viseme-reference/
- VRM Lip Sync https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md#lip-sync-procedural
- ARPAbet Phoneme Set https://en.wikipedia.org/wiki/ARPABET and http://www.speech.cs.cmu.edu/cgi-bin/cmudict

## Face Tracking Blend Shape Naming

Face tracking is the process of using a camera to track a person's facial movements, and applying those movements to a character/avatar's face. While visemes are used for lip syncing to audio, face tracking is used to mimic a much broader range of facial expressions. The `Face*` blend shapes defined by G4MF are intended to be used for this purpose, though they can also be used to adjust the mesh around the eyes when using eye tracking, or used for manual animation.

The standards for face tracking vary widely, unlike skeleton rigs and visemes which are relatively consistent. G4MF's face tracking blend shape names are designed to be a superset of all common face tracking standards. Since "Unified Expressions" is already a comprehensive standard that includes the functionality of all other common standards, G4MF's face tracking blend shape names are based on Unified Expressions, except with a `Face` prefix added to each name for clarity, and also the list of names has been alphabetized.

The following table includes columns for many common face tracking standards, and how they map to G4MF's face tracking blend shape names. `~` indicates an indirect non-1-to-1 mapping, which is described in the Unified Expressions documentation.

| G4MF Blend Shape Names  | Unified Expressions | ARKit             | SRanipal                | Meta Movement (Quest Pro) |
| ----------------------- | ------------------- | ----------------- | ----------------------- | ------------------------- |
| FaceBrowDownLeft        | BrowDownLeft        | browDownLeft      | Eye_Left_squeeze        | BROW_LOWERER_L            |
| FaceBrowDownRight       | BrowDownRight       | browDownRight     | Eye_Right_squeeze       | BROW_LOWERER_R            |
| FaceBrowInnerUp         | BrowInnerUp         | browInnerUp       | Not supported           | ~                         |
| FaceBrowInnerUpLeft     | BrowInnerUpLeft     | ~                 | Not supported           | INNER_BROW_RAISER_L       |
| FaceBrowInnerUpRight    | BrowInnerUpRight    | ~                 | Not supported           | INNER_BROW_RAISER_R       |
| FaceBrowOuterUpLeft     | BrowOuterUpLeft     | browOuterUpLeft   | Not supported           | OUTER_BROW_RAISER_L       |
| FaceBrowOuterUpRight    | BrowOuterUpRight    | browOuterUpRight  | Not supported           | OUTER_BROW_RAISER_R       |
| FaceCheekPuff           | CheekPuff           | cheekPuff         | ~                       | ~                         |
| FaceCheekPuffLeft       | CheekPuffLeft       | ~                 | Cheek_Puff_Left         | CHEEK_PUFF_L              |
| FaceCheekPuffRight      | CheekPuffRight      | ~                 | Cheek_Puff_Right        | CHEEK_PUFF_R              |
| FaceCheekSquintLeft     | CheekSquintLeft     | cheekSquintLeft   | Eye_Left_squeeze        | CHEEK_RAISER_L            |
| FaceCheekSquintRight    | CheekSquintRight    | cheekSquintRight  | Eye_Right_squeeze       | CHEEK_RAISER_R            |
| FaceCheekSuck           | CheekSuck           | Not supported     | Cheek_Suck              | ~                         |
| FaceCheekSuckLeft       | CheekSuckLeft       | Not supported     | ~                       | CHEEK_SUCK_L              |
| FaceCheekSuckRight      | CheekSuckRight      | Not supported     | ~                       | CHEEK_SUCK_R              |
| FaceEyeClosedLeft       | EyeClosedLeft       | eyeBlinkLeft      | Eye_Left_Blink/squeeze  | EYES_CLOSED_L             |
| FaceEyeClosedRight      | EyeClosedRight      | eyeBlinkRight     | Eye_Right_Blink/squeeze | EYES_CLOSED_R             |
| FaceEyeConstrictLeft    | EyeConstrictLeft    | Not supported     | Eye_Left_Constrict      | Not supported             |
| FaceEyeConstrictRight   | EyeConstrictRight   | Not supported     | Eye_Right_Constrict     | Not supported             |
| FaceEyeDilationLeft     | EyeDilationLeft     | Not supported     | Eye_Left_Dilation       | Not supported             |
| FaceEyeDilationRight    | EyeDilationRight    | Not supported     | Eye_Right_Dilation      | Not supported             |
| FaceEyeLookDownLeft     | EyeLookDownLeft     | eyeLookDownLeft   | Eye_Left_Look_Down      | EYES_LOOK_DOWN_L          |
| FaceEyeLookDownRight    | EyeLookDownRight    | eyeLookDownRight  | Eye_Right_Look_Down     | EYES_LOOK_DOWN_R          |
| FaceEyeLookInLeft       | EyeLookInLeft       | eyeLookInLeft     | Eye_Left_Right          | EYES_LOOK_IN_L            |
| FaceEyeLookInRight      | EyeLookInRight      | eyeLookInRight    | Eye_Right_Left          | EYES_LOOK_IN_R            |
| FaceEyeLookOutLeft      | EyeLookOutLeft      | eyeLookOutLeft    | Eye_Left_Left           | EYES_LOOK_OUT_L           |
| FaceEyeLookOutRight     | EyeLookOutRight     | eyeLookOutRight   | Eye_Right_Right         | EYES_LOOK_OUT_R           |
| FaceEyeLookUpLeft       | EyeLookUpLeft       | eyeLookUpLeft     | Eye_Left_Look_Up        | EYES_LOOK_UP_L            |
| FaceEyeLookUpRight      | EyeLookUpRight      | eyeLookUpRight    | Eye_Right_Look_Up       | EYES_LOOK_UP_R            |
| FaceEyeSquintLeft       | EyeSquintLeft       | eyeSquintLeft     | Eye_Left_squeeze        | EYES_SQUINT_L             |
| FaceEyeSquintRight      | EyeSquintRight      | eyeSquintRight    | Eye_Right_squeeze       | EYES_SQUINT_R             |
| FaceEyeWideLeft         | EyeWideLeft         | eyeWideLeft       | Eye_Left_Wide           | EYES_WIDEN_L              |
| FaceEyeWideRight        | EyeWideRight        | eyeWideRight      | Eye_Right_Wide          | EYES_WIDEN_R              |
| FaceJawForward          | JawForward          | jawForward        | Jaw_Forward             | JAW_THRUST                |
| FaceJawLeft             | JawLeft             | jawLeft           | Jaw_Left                | JAW_SIDEWAYS_LEFT         |
| FaceJawOpen             | JawOpen             | jawOpen           | Jaw_Open                | JAW_DROP                  |
| FaceJawRight            | JawRight            | jawRight          | Jaw_Right               | JAW_SIDEWAYS_RIGHT        |
| FaceLipFunnel           | LipFunnel           | mouthFunnel       | ~                       | ~                         |
| FaceLipFunnelLower      | LipFunnelLower      | ~                 | Mouth_Lower_Overturn    | ~                         |
| FaceLipFunnelLowerLeft  | LipFunnelLowerLeft  | ~                 | ~                       | LIP_FUNNELER_LB           |
| FaceLipFunnelLowerRight | LipFunnelLowerRight | ~                 | ~                       | LIP_FUNNELER_RB           |
| FaceLipFunnelUpper      | LipFunnelUpper      | ~                 | Mouth_Upper_Overturn    | ~                         |
| FaceLipFunnelUpperLeft  | LipFunnelUpperLeft  | ~                 | ~                       | LIP_FUNNELER_LT           |
| FaceLipFunnelUpperRight | LipFunnelUpperRight | ~                 | ~                       | LIP_FUNNELER_RT           |
| FaceLipPucker           | LipPucker           | mouthPucker       | Mouth_Pout              |                           |
| FaceLipPuckerLowerLeft  | LipPuckerLowerLeft  | ~                 | ~                       | LIP_PUCKER_L              |
| FaceLipPuckerLowerRight | LipPuckerLowerRight | ~                 | ~                       | LIP_PUCKER_R              |
| FaceLipPuckerUpperLeft  | LipPuckerUpperLeft  | ~                 | ~                       | LIP_PUCKER_L              |
| FaceLipPuckerUpperRight | LipPuckerUpperRight | ~                 | ~                       | LIP_PUCKER_R              |
| FaceLipSuckLower        | LipSuckLower        | mouthRollLower    | Mouth_Lower_Inside      | ~                         |
| FaceLipSuckLowerLeft    | LipSuckLowerLeft    | ~                 | ~                       | LIP_SUCK_LB               |
| FaceLipSuckLowerRight   | LipSuckLowerRight   | ~                 | ~                       | LIP_SUCK_RB               |
| FaceLipSuckUpper        | LipSuckUpper        | mouthRollUpper    | Mouth_Upper_Inside      | ~                         |
| FaceLipSuckUpperLeft    | LipSuckUpperLeft    | ~                 | ~                       | LIP_SUCK_LT               |
| FaceLipSuckUpperRight   | LipSuckUpperRight   | ~                 | ~                       | LIP_SUCK_RT               |
| FaceMouthClosed         | MouthClosed         | mouthClose        | Mouth_Ape_Shape         | LIPS_TOWARD               |
| FaceMouthDimplerLeft    | MouthDimplerLeft    | mouthDimpleLeft   | ~                       | DIMPLER_L                 |
| FaceMouthDimplerRight   | MouthDimplerRight   | mouthDimpleRight  | ~                       | DIMPLER_R                 |
| FaceMouthFrownLeft      | MouthFrownLeft      | mouthFrownLeft    | ~                       | LIP_CORNER_DEPRESSOR_L    |
| FaceMouthFrownRight     | MouthFrownRight     | mouthFrownRight   | ~                       | LIP_CORNER_DEPRESSOR_R    |
| FaceMouthLowerDownLeft  | MouthLowerDownLeft  | mouthLowerUpLeft  | Mouth_Lower_Down_Left   | LOWER_LIP_DEPRESSER_L     |
| FaceMouthLowerDownRight | MouthLowerDownRight | mouthLowerUpRight | Mouth_Lower_Down_Right  | LOWER_LIP_DEPRESSOR_R     |
| FaceMouthPressLeft      | MouthPressLeft      | mouthPressLeft    | Not supported           | LIP_PRESSOR_L             |
| FaceMouthPressRight     | MouthPressRight     | mouthPressRight   | Not supported           | LIP_PRESSOR_R             |
| FaceMouthRaiserLower    | MouthRaiserLower    | mouthShrugLower   | Mouth_Lower_Overlay     | CHIN_RAISER_B             |
| FaceMouthRaiserUpper    | MouthRaiserUpper    | mouthShrugUpper   | Not supported           | CHIN_RAISER_T             |
| FaceMouthSadLeft        | MouthSadLeft        | ~                 | Mouth_Sad_Left          | ~                         |
| FaceMouthSadRight       | MouthSadRight       | ~                 | Mouth_Sad_Right         | ~                         |
| FaceMouthSmileLeft      | MouthSmileLeft      | mouthSmileLeft    | Mouth_Smile_Left        | LIP_CORNER_PULLER_L       |
| FaceMouthSmileRight     | MouthSmileRight     | mouthSmileRight   | Mouth_Smile_Right       | LIP_CORNER_PULLER_R       |
| FaceMouthStretchLeft    | MouthStretchLeft    | mouthStretchLeft  | ~                       | LIP_STRETCHER_L           |
| FaceMouthStretchRight   | MouthStretchRight   | mouthStretchRight | ~                       | LIP_STRETCHER_R           |
| FaceMouthTightenerLeft  | MouthTightenerLeft  | Not supported     | Not supported           | LIP_TIGHTENER_L           |
| FaceMouthTightenerRight | MouthTightenerRight | Not supported     | Not supported           | LIP_TIGHTENER_R           |
| FaceMouthUpperUpLeft    | MouthUpperUpLeft    | mouthUpperUpLeft  | Mouth_Upper_Up_Left     | UPPER_LIP_RAISER_L        |
| FaceMouthUpperUpRight   | MouthUpperUpRight   | mouthUpperUpRight | Mouth_Upper_Up_Right    | UPPER_LIP_RAISER_R        |
| FaceNoseSneerLeft       | NoseSneerLeft       | noseSneerLeft     | Not supported           | NOSE_WRINKLER_L           |
| FaceNoseSneerRight      | NoseSneerRight      | noseSneerRight    | Not supported           | NOSE_WRINKLER_R           |
| FaceTongueDown          | TongueDown          | Not supported     | Tongue_Down             | Not supported             |
| FaceTongueLeft          | TongueLeft          | Not supported     | Tongue_Left             | Not supported             |
| FaceTongueOut           | TongueOut           | tongueOut         | Tongue_LongStep1/2      | TONGUE_OUT                |
| FaceTongueRight         | TongueRight         | Not supported     | Tongue_Right            | Not supported             |
| FaceTongueRoll          | TongueRoll          | Not supported     | Tongue_Roll             | Not supported             |
| FaceTongueUp            | TongueUp            | Not supported     | Tongue_Up               | Not supported             |

This table lacks some of the nuances described in the Unified Expressions documentation for how these map to other standards. For more detailed documentation on each of these blend shapes, read the Unified Expressions documentation linked below.

Usage rules:

- If a blend shape (morph target) exists for one of these listed face tracking shapes, it MUST have its name set to the corresponding name from the table above in order to be used as that shape in an application's face tracking. The names are case-sensitive. This ensures that applications can reliably identify and use the face tracking shapes by their names.

- If a face tracking shape is needed that is not defined here, they may still be added as blend shapes, however, not all runtime applications will recognize or use them. This standard is not intended to limit future expansion with new face tracking shapes for new facial expressions, but rather to ensure a common baseline for compatibility.

- If a runtime needs a face tracking shape that is unavailable or missing, it may fall back to another shape, or blend existing shapes, at the application's discretion. This includes the possibility of applications supporting custom face tracking shapes, with a fallback to this base definition to support characters/avatars without that custom shape, and also allows applications to handle cases of missing shapes gracefully.

- If a face tracking shape exists but is not supported by an application or format, it may be safely ignored. For example, ARKit, SRanipal, and Meta Movement each do not support some of these shapes, so those shapes would not be used when converting a G4MF model to be used with those systems.

- Face tracking shapes may be used for purposes other than face tracking. For example, `FaceCheekPuff` may be used as part of a "blowing air" facial expression.

- For eye tracking purposes, use the `FaceEyeLook*` blend shapes to adjust the mesh in response to eye rotation, and use the `FaceEyeClosed*` blend shapes to adjust the mesh in response to eye blinking. If a runtime application requires fewer combined blend shapes instead of fine control, an importer MAY choose to combine blend shapes at import time in any way the importer sees fit, such as combining the two `FaceEyeClosed*` blend shapes into a single closed/blink blend shape.

### Face Tracking References

- Unified Expressions compatibility table https://docs.vrcft.io/docs/tutorial-avatars/tutorial-avatars-extras/compatibility/overview
- Unified Expressions shapes https://docs.vrcft.io/docs/tutorial-avatars/tutorial-avatars-extras/unified-blendshapes#ue-ref
- Apple ARKit blendShapes official documentation https://developer.apple.com/documentation/arkit/arfaceanchor/blendshapelocation
- ARKit Face Blendshapes unofficial documentation https://arkit-face-blendshapes.com/
- Meta Movement (Quest Pro) https://developers.meta.com/horizon/documentation/native/android/move-ref-blendshapes/
- Facial Action Coding System (FACS) Cheat Sheet https://melindaozel.com/arkit-to-facs-cheat-sheet/
