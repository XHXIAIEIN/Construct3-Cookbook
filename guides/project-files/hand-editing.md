# Hand-editing Construct project files

Read this before you write or change `eventSheets/*.json`, `layouts/*.json`,
`objectTypes/**/*.json`, `families/*.json`, `timelines/**/*.json`,
`3dmodels/**/*.json`, `project.c3proj` or clipboard payloads without the
editor. To put events into a sheet, use the `construct3-agent-plugin`
skill's `scripts/edit_sheet.py`. It takes the events as a plan, gives them
their sids and checks the result before it writes. This file says how to
write each entry of such a plan or of a hand edit. Clipboard payloads use
the same condition and action entries, and
`<Construct3-Clipboard>/docs/clipboard-format.md` documents their envelope.

## The project folder

Scirra's guide [Construct's project format](https://www.construct.net/en/tutorials/constructs-project-format-3275)
states what follows. The `llm-context.md` that the editor writes into every
project links to this guide. Construct3-RAG keeps a copy under the guide's
licence, CC BY 4.0, in `<Construct3-RAG>/data/c3-guides/constructs-project-format.md`.
The format has no published specification and changes between releases.
An invalid edit can leave a project that does not open, so end every hand
edit with the checks at the end of this file.

- `project.c3proj` lists every object type, family, layout, event sheet,
  timeline, flowchart, 3D model, script, sound, music, video, font, icon and
  file, in the folders of the Project Bar. The editor reads only the files
  it lists and ignores any other file. So if you write a file by hand, list
  it in the same change. Each JSON resource is in its folder
  (`objectTypes/`, `families/`, `layouts/`, `eventSheets/`, `timelines/`,
  `flowcharts/`, `3dmodels/`), under the subfolders that the listing names.
- An editor that has the folder project open keeps every file as it loaded
  it. It shows no notice when a file changes on disk, and it never shows
  the change. *Reload all from folder* (F9) re-reads script files, not
  event sheets or layouts. A save writes the editor's copy of each resource
  edited in the editor over any change made to its file on disk. A save
  with no edit in the editor still writes `project.c3proj` from the
  editor's copy when the file on disk differs. So a project property set
  by hand returns to the editor's value. A sheet added by hand loses its
  entry in the listing, and the editor then ignores its file. Before you
  change the files, ask the user to save and close the project in the
  editor. After the change, ask the user to open it again. If the project
  stayed open during the change, ask the user to close it there without
  saving. [manual: interface/keyboard-shortcuts.md "F9"; observed in a
  scratch project on a local disk, r506.3, 2026-10-24: opened with *Open
  local project folder*; a comment and a layout width written on disk were
  gone after a save that followed an edit of the same sheet or layout,
  also after F9; a comment on a sheet that the editor did not edit stayed;
  a property and an added sheet's entry in `project.c3proj` were gone after
  a save with no edit in the editor]
- Images are in `images/`, without subfolders, with names in lower case. A
  frame's file is `<object type>-<animation>-<frame>.png`. The frame number
  counts from 0 and is padded to three digits (`player-default-000.png`).
  An object with a single image, a Tiled Background or a 9-patch has
  `<object type>.png`. The editor takes an image's size from the file and
  ignores the `width` and `height` of its entry. So you can redraw an image
  at another size outside the editor. An image that was imported as JPEG or
  AVIF and not edited in the editor keeps that format, and its entry's
  `fileType` names the format.
- Sound and music are WebM Opus, `.webm`. Fonts are WOFF, the only format
  that browsers support consistently. The editor also takes TTF and OTF, as
  the official examples show. Icons and the loading logo are PNG. For
  video, MP4 with H.264 is a good default. A file in `files/` can be of any
  kind. Construct does not use it, but the project's logic reads it, for
  example through AJAX.
- For TypeScript, list either the `.ts` files alone or the `.js` files
  alone. Construct compiles the listed `.ts` files. Listed `.js` files are
  compiled outside Construct from `.ts` files that the project does not
  list. If both files of one script are listed, Construct runs the `.js`
  file [manual: scripting/using-scripting/typescript-construct.md].
- `*.uistate.json` files and `uistate` folders hold the state of the
  editor's interface, and deleting them loses nothing else. But a uistate
  file that exists and lacks a key the editor saves can stop the project
  from opening. A layout's uistate file without `grid` did this, with the
  error "Cannot read properties of undefined (reading 'show')". So copy a
  file that the editor saved, or write none. Palettes and tilemap brushes
  have folders of their own, `palettes/` and `tilemapBrushes/`. [observed
  in a game project, r505, 2026-10-14]
- The project property *Preview effects* (Project Properties, Editor) is
  saved in `project.uistate.json` as `"previewEffects"`, not in
  `project.c3proj`. When it is off, the Layout View draws every image
  without its effects and blend mode. To edit a 3D layout with depth
  effects such as Fog (exponential), turn it off. The editor's camera
  stands far from the layout, so the fog covers everything. The setting
  stays on the machine that saved it. [manual: project-primitives/projects.md
  "Preview effects"; observed in a game project, r505, 2026-10-08]
- A layout's `layouts/<name>.uistate.json` stores the view that its Layout
  View opens at. `view.viewMode` is `"2d"` or `"3d"`, and `view["3d"]`
  holds `cameraPosition` and `cameraLookAt`. To open a 3D layout at the
  angle that the preview shows, set `viewMode` to `"3d"`. Then set the two
  vectors to the position and target of the game's 3D Camera. The editor
  overwrites the file with the user's view at each save, so this sets the
  first view only. [observed in a game project, r505, 2026-10-14]

## Encodings

Each rule below comes from the editor's loaders, from files that the editor
saved or from the official examples
(`<Construct3-Agent-Skills>/docs/decisions/checker-editor-load-rules.md`).

### Every file

- A `sid` is a 15-digit random integer that is unique across the whole
  project, so content merges without renumbering. A `uid` is any value that
  is unique across all layouts and the single-global object types. A
  single-global type, such as the Timeline controller, keeps the `uid` of
  its one instance in `objectTypes/<Name>.json`. So if you number a layout
  instance from the highest layout uid alone, it can collide with that uid.
  If UID numbering is set to Random (`"uidAllocationMode": "random"`),
  Construct gives each instance it adds a six-digit random uid. This keeps
  the uids of instances added on two branches of a project under source
  control apart
  (`<Construct3-Agent-Skills>/docs/decisions/random-uid-allocation.md`).
- Files are UTF-8 with raw non-ASCII, tab indent, LF, no trailing newline
  and no byte order mark. Python
  `json.dumps(obj, indent="\t", ensure_ascii=False)` reproduces the
  editor's output byte for byte. A file that starts with a byte order mark
  still opens. [observed: the official examples carry none; an event
  sheet and a `project.c3proj` with one opened in the stable editor, October
  2026]
- A Save of a folder project writes the files of the resources that were
  edited, and `project.c3proj` when it differs from the editor's copy (see
  "The project folder"). So any other hand-written file keeps its form,
  including keys that the editor would rewrite, until something in it is
  edited in the editor.
  Save as project folder and Download a copy write every file. [observed in
  a game project, r504, October 2026: a Save after opening an unedited
  folder wrote no file; two folder saves rewrote only the edited layout and
  `project.c3proj`]
- The editor leaves empty lists out. An event without sub-events has no
  `children`, a function or custom action call without arguments has no
  `parameters`, and an animation frame without image points has no
  `imagePoints`. A `[]` loads, and the next save of its file drops it.
  [observed in a game project, r504, October 2026: each of these written
  back by hand into a saved project came back as described from Save as
  project folder]

### Event sheets

- Comparison parameters are integers: 0 `=`, 1 `≠`, 2 `<`, 3 `≤`, 4 `>`, 5 `≥`.
- String parameters keep their quotes: `"tag": "\"attack\""`. `layer` is an
  index string `"2"` or a quoted name `"\"Graphics\""`. `create-hierarchy`
  is a JSON boolean. Inverted conditions have `"isInverted": true`.
- Everything that is not an expression has no inner quotes: a combo item
  (`"mouse-button": "left"`, `"loop": "no"`), an object, a layout, a
  variable, an ease id (`"ease": "easeoutback"`, the ids under
  `ui/bars/timeline/eases` in `<Construct3-RAG>/data/c3-lang/en-US.json`).
  The editor loads a quoted combo value without an error and keeps the
  combo's default item. A key is its key code as a JSON number
  (`"key": 32`), and a string stops the load with `expected finite number`.
  A JSON string `"false"` in a boolean parameter reads as true.
- An event variable's `initialValue` is text, whatever its `type`: `"0"`,
  `"hello"` without inner quotes, and for a boolean `"true"` or `"false"`
  in lowercase. The editor reads a boolean by comparing the text to
  `"true"`. So a JSON `false` or `true`, a `"True"` and a `"1"` all read as
  false. A number text that does not parse reads as 0. A function
  parameter's `initialValue` can also be a JSON number. Any other value
  stops the load with `invalid type of initialValue`.
- A function call is
  `{"callFunction": "name", "sid": N, "parameters": ["expr", ...]}`. A
  function block has `functionCopyPicked` (boolean) and `functionParameters`
  entries with `name`, `type`, `initialValue`, `comment`, `sid`.
- A custom action block has `"eventType": "custom-ace-block"`,
  `"aceType": "action"`, `"aceName"`, `"objectClass"` (the declaring type
  or family), then the same `function*` keys as a function block. Its
  `functionCopyPicked` is *Copy all picked*. A call is
  `{"customAction": "name", "objectClass": "<row object>", "sid": N}`. It
  has `"parameters": ["expr", ...]` exactly when the block declares
  parameters. If the row object is a member type and the block is declared
  on the family and not on the member, the editor saves the call with
  `"customActionObjectClass": "<family>"`. A call that runs the member's own
  block is saved without it. A call written without the key still loads.
  [observed in a game project, r504, October 2026: 13 calls on two member
  types gained it on save, the calls of one member's own two blocks did not]
- A `projectfile` parameter is the bare file name for a file at the root
  (`"file": "DefaultProfile.json"`) and `"file": {"path": "data/enemy.json"}`
  for a file in a subfolder. A bare name for a file in a subfolder loads,
  and the save rewrites it to the object form.
- An `audiofile` parameter is the file's name without its extension. The
  editor matches it in any case against the sound and music files. The
  official examples write it as a string, `"audio-file": "Flash"`, and a
  project saved by r495 writes `"audio-file": {"path": "Flash"}`. Write the
  string, because the editor opens the examples that hold it and the
  checker reads both forms. Scirra's format guide does not describe the
  parameter.
- If an ACE gained parameters in a later release, you can omit them,
  because the editor fills in their defaults on load. For example,
  `pick-nearestfurthest` loads with `which`, `x` and `y` alone, although
  the schema also lists `z` and `pick-all-tied`.
- You can write a family instance variable through a member type:
  `"objectClass": "Bat"`, `"instance-variable": "hp"` with `hp` declared on
  family `EnemyGroup`.
- To use a behavior that a family declares, name a member type and the
  family's behavior name: `"objectClass": "DragonHead", "behaviorType":
  "Physics"` where only family `Parts` declares Physics. The member's layout
  instances hold the properties block of the family's behavior as if it
  were their own.

### Layouts

- A layout instance's `instanceVariables` map holds JSON values by type,
  with no quotes on a number or a boolean:
  `{"hp": 3, "dead": false, "label": "a"}`.
- An instance's `world.angle` is in radians: 270 degrees is `4.7124`. So a
  generator converts degrees with `math.radians`. `Angle` in events stays
  in degrees.
- An instance's `world` entry writes Z elevation as `"z"`, with a
  `"depth"` key. Layers write it as `zElevation`.
- An effect's color parameter on a layout instance is four numbers,
  `[1, 0.24, 0.27, 1]`. [observed in a project the editor r504 saved,
  2026-10-03]
- The editor saves every layout instance in one key order and one number
  form. So a hand edit in another form comes back changed in the diff of
  the next save. An instance's key order is `type`, `properties`, `uid`,
  `sid`, `tags`, `instanceVariables`, `behaviors`, `effects`,
  `materialSurfaceType`, `sceneGraphData`, `showing`, `locked`, `world`.
  The key order of `world` is `x`, `y`, `width`, `height`, `originX`,
  `originY`, `color`, `z`, `angle`, `blendMode`. `properties` follow the
  order that the plugin declares them in. The save gives a world instance
  without `materialSurfaceType` the value `"smooth"`, whatever its plugin
  and whether or not it has effects. A nonworld instance gets no
  `materialSurfaceType`. Numbers are saved in their shortest form: `284.0`
  becomes `284`, `215.250` becomes `215.25`, `-0.0` becomes `0`. So a
  generator writes a whole float as an int. [observed in a game project,
  r504, October 2026: Download a copy of a layout with `effects` and
  `sceneGraphData` after `world`, `materialSurfaceType` removed from
  Sprite, Tiled Background, 9-patch and Sprite Font instances, and
  `"y": 284.0` came back byte for byte as the editor had last saved it; a
  folder save made the same changes]
- If an instance has no hierarchy, leave `sceneGraphData` out, because the
  save writes a full `sceneGraphData` block for `"sceneGraphData": null`.
  The save writes a behavior property that an instance lacks with its
  default (`"rotation-type": "2d"` for Rotate). It writes an instance's
  `instanceVariables` with the family variables first, then the type's
  own, each in declaration order. [observed in a game project, r504,
  October 2026: each of these written back by hand into a saved project
  came back as described from Save as project folder]
- The save rewrites a layout instance's `world.originX` and `originY` to
  the origin of the first frame of its initial animation, so write the
  frame's values. An instance written with `"originY": 1` over a frame
  whose origin is 0.9929 is saved with 0.9929. [observed in a game project,
  r504, October 2026: instances whose `initial-frame` is 0, and a folder
  save]
- A glTF made with Y up imports on its side, with its height along the
  layout's Y axis. To turn it upright, set the model's default rotation in
  `3dmodels/<model>.json`: `"rotation": {"0": -90, "1": 0, "2": 0}`, where
  key `"0"` is the angle about X in degrees. The Layout View and the
  preview both apply it to every instance. A *Set transform* rotation in
  *On start of layout* or *On model loaded* runs in the preview only, so
  the Layout View still shows the model on its side. [manual:
  project-primitives/3d-model.md "Rotation"; observed in a game project,
  r505, 2026-10-14]
- A 3D model instance's `meshes` property maps each mesh name to a
  boolean: `"meshes": {"Body": true, "Glow": false}`. The instance draws
  the meshes set to true in the Layout View and from the start of the
  preview, and *Set mesh enabled* can show the others later. A string,
  whether empty or a mesh name, draws every mesh. An array stops the
  project from opening. [observed in a game project, r505, 2026-10-14]
- `animations` in `3dmodels/<model>.json` is a list of `[name, clip]`
  pairs. To add a copy of a clip, append a pair whose clip is the
  original's with a fresh UUID as its `id` and its own `name`. Use the same
  name in both places:
  `["Attack2", {"id": "<new UUID>", "name": "Attack2", "duration": ...,
  "tracks": [...]}]`. The tracks keep their `lookupUUID`, which names the
  bone they move. The project opens, and *Play* plays the copy. [observed
  in a game project, r505, 2026-10-14: a copy appended by a build script,
  the folder and its packed `.c3p` opened and previewed, and the copy
  played from the start on alternate attacks]
- An instance that is a template, or a replica of one (the *Template*
  section of the Properties Bar), carries a `template` block between
  `behaviors` and `effects`. Any other instance has no such key, and
  `project.c3proj` holds nothing about templates. The block's keys are, in
  order: `mode`, `templateName`, `sourceTemplateName`,
  `replicaHierarchyInSyncWithTemplate`, `templatePropagateHierarchyChanges`,
  `replicaIgnoreTemplateHierarchyChanges`, `components`, `replicasUIDs`. A
  template has `"mode": "template"` and its name in `templateName`. Its
  `sourceTemplateName` is `""`, or the name of the template it was made
  from (`Air1` from `Air0` from `Floor0`). A replica has
  `"mode": "replica"`, `templateName` `""` and the template's name in
  `sourceTemplateName`. `replicaHierarchyInSyncWithTemplate` and
  `replicaIgnoreTemplateHierarchyChanges` are `false` in every example.
  `templatePropagateHierarchyChanges` is `true` or `false`, and it is the
  manual's *Propagate hierarchy*. `replicaIgnoreTemplateHierarchyChanges`
  is the manual's *Ignore hierarchy propagation*. `replicasUIDs` is `null`
  in every example, on templates and replicas alike.
  `components` lists five entries by `id`: `plugin`,
  `instance-variable`, `behavior`, `effect` and `world-instance`. Each
  entry has `component`, a list of `{"key": ..., "state": [...]}`. For
  `plugin`, the one entry's key is `"plugin"`, and `state` holds
  `[name, boolean]` pairs over the plugin's property ids. For
  `world-instance`, the key is `"world-instance"`, and the pairs run over
  `x`, `y`, `z`, `w`, `h`, `a`, `o`, `c`, `sx`, `sy`, `bm`, `twpx`, `twpy`,
  `twpz`, `twpw`, `twph`, `twpa`, `dwp` and `ssm`. For `behavior` and
  `effect`, there is one entry per behavior or effect, keyed by its name,
  with pairs over its property ids (`["enabled", true]` for a behavior,
  `["<<effect-template-enable>>",
  true]` and the parameter names for an effect). An instance without
  behaviors or effects has `[]` there. For `instance-variable`, the state
  is a list of `{"iv": name, "state": boolean}` objects.
  `x` and `y` are `false` in every block, and the rest are mostly `true`.
  For example, a replica of `Tree1` has `z` `false`, and a template made
  from `Floor0` has `w`, `h`, `sx` and `sy` `false`. The manual says that
  a replica takes each property from its template until the replica's own
  value is edited, and that position stays the replica's own. So the
  boolean reads as whether the property follows the template. The editor
  was not watched doing this.
  Files that r288 to r290 saved have `"mode": "none"` blocks. These blocks
  hold the lists as JSON strings, without the booleans and `replicasUIDs`.
  A few example replicas have `sourceTemplateName` `""`, and a few
  templates have an empty `templateName`. What the editor shows for these,
  and for a replica whose template is gone, is not observed.
  The *Create object* and *Create object (by name)* actions name a
  template in `template-name`. This is an expression string with the name
  in inner quotes, `"\"Air1\""`, and `"\"\""` for none. If it is written as
  `""`, the project does not open. The manual says that a name that no
  template has is treated as none. The "template instance" that the
  checks and the pitfalls name is any instance of the object in a layout.
  A *Create object* without a template name copies it, and it needs no
  `template` block. [manual: project-primitives/objects/templates.md;
  examples airborne-explorer `ObjectRepository` and `GameEvents`, avalanche
  `ObjectRepository` and `MainMenu`, berry-harvester, arcane-express
  `Game`; the `"none"` blocks in animated-svg, html-element and html-menu]
- Every layer carries `overriden`, `0` or `1`, right after `name`. It also
  carries `global`, a boolean, near the end. The layer whose *Global*
  property is on has `"global": true` and `"overriden": 0`. A layer of the
  same name in another layout of the project has `"global": false` and
  `"overriden": 1`. If the global layer has sub-layers, each sub-layer of
  that same-named layer has these values too. In the examples, every layer
  with `overriden` 1 has a same-named global layer in another layout.
  The overriden layer keeps its own `sid`, the full set of layer
  properties, its `subLayers` and its own `instances` with their own uids.
  In the compared examples, its properties have the global layer's values.
  Its instances are, for example, the three HUD instances of each level of
  kiwi-story and the nine on the `UI` layer of each level of rat-purrsuit.
  The manual says that the editor and the runtime use the global layer's
  instances and properties in its place. That the kept instances never
  show is not observed here. Two more things are not observed: whether the
  editor sets `overriden` itself when a layer is made global or renamed,
  and what it does with a `1` whose global layer is gone. So write both
  sides in a hand edit. [manual: project-primitives/layers.md
  "Global layers"; examples fuji-leaper `Level6` (`Holder`, global, with
  sub-layers `Link` and `Mask`) and `Level1`, kiwi-story `GlobalLayers` and
  `1_Forest`, rat-purrsuit `Level1` and `Level2`, avalanche `Level1` and
  `Level2`]

### Object types, families and `project.c3proj`

- `plugin-id`, `behaviorId` and the `id` of a `usedAddons` entry use the
  editor's exact spelling, which is `originalId` in
  `<Construct3-RAG>/data/c3-schemas/_index.json`. `Arr` is Array, `Json`
  JSON, `TiledBg` Tiled Background, `EightDir` 8 Direction and `Sin` Sine.
  `solid`, `scrollto`, `jumpthru`, `bound`, `wrap`, `destroy` and `gamepad`
  are lowercase. Any other spelling stops the load with
  `missing plugin id`.
- `savedWithRelease` in `project.c3proj` is the release that last saved
  the project. Its value is the release number times 100 plus its patch:
  `49502` for r495.2, `50500` for r505. An editor older than that refuses
  to open the project ("saved in a newer version of Construct"). If a save
  in a newer release changed no file except `project.c3proj`, you can undo
  it by hand. Set `savedWithRelease` back and remove the project properties
  that the older release does not know. For example, r505 adds
  `saveLLMContextFile` and changes some display names in `usedAddons`,
  such as `bound` to "Bound to". Write those names back as the older
  release spells them. [observed in a game project, 2026-10-08: saved once
  in r505, refused by r495.2, opened and previewed in r495.2 after these
  changes]
- A family is `families/<Name>.json` (`name`, `plugin-id`, `sid`,
  `instanceVariables`, `behaviorTypes`, `effectTypes`, `members`). It is
  listed under `families` in `project.c3proj`, like an object type. A
  container has no file. `project.c3proj` holds
  `"containers": [{"members": ["TankBase",
  "TankTurret"]}]`, with object type names as members and no
  `selectMode`. Nothing under `objectTypes/` names a container.
- The editor sorts some lists of `project.c3proj` on save, so an entry
  appended at the end moves in the diff of the next save. `usedAddons`
  holds plugins, then behaviors, then effects. Each group is sorted by
  `id` in code point order, uppercase before lowercase: `AJAX` before
  `AdvancedRandom`, `Touch` before `gamepad`. A container's `members` are
  sorted without regard to case: `heroLabel` before `HeroStats`. Insert an
  entry where the sort puts it. [observed in a game project, r504, October
  2026: a save moved `Timeline`, `Spritefont2` and `Anchor` from the end of
  `usedAddons` into place and reordered a container's members]
- The save leaves out a frame's `collisionPoly` when it is the whole image
  in the editor's vertex order, `[0, 0, 1, 0, 1, 1, 0, 1]`. It keeps
  `useCollisionPoly`, `true` or `false`. A frame without `collisionPoly`
  takes the whole image, so both ways of writing it save the same. The
  whole image in another vertex order, such as `[1, 0, 1, 1, 0, 1, 0, 0]`,
  is kept as written. [observed in a scratch project, r495.2 and r504,
  2026-10-04: Save as project folder of a Sprite whose frames held the
  whole image in both orders, a triangle, and the whole image with
  `useCollisionPoly` false; both frames in the editor's order came back
  without `collisionPoly` and with their `useCollisionPoly`, the other two
  as written]
- Every `image` block and every animation frame carries an
  `imageSpriteId`, an integer that no other image or frame of the project
  has. If an id repeats, the editor stops with `id already in use`. An
  object type copied from another one's file keeps the original's ids. So
  give the copy its own `name` and its own 15-digit `sid`. Then give its
  `image` block, or each of its frames, an unused `imageSpriteId`.
  `check_project.py` prints one for each id that repeats. [observed in a
  game project, r504, 2026-10-06: a Sprite Font copied from another Sprite
  Font's file did not open until the copy had its own `imageSpriteId`]
- A Sprite Font has `"plugin-id": "Spritefont2"` and an `image` block in
  its object type file, as a Tiled Background has. Its picture is
  `images/<lowercase name>.png`, and its `usedAddons` entry is
  `{"type": "plugin",
  "id": "Spritefont2", "name": "Sprite font", "author": "Scirra", "bundled":
  false}`. Its layout instance holds `text`,
  `enable-bbcode`, `character-width`, `character-height`, `character-set`,
  `spacing-data`, `scale`, `character-spacing`, `line-height`,
  `horizontal-alignment`, `vertical-alignment`, `wrapping`,
  `initially-visible`, `origin` and `read-aloud`. `spacing-data` is a
  string that holds JSON, `"[[25,\".\"],[53,\"0123456789\"]]"`, or `""`
  for none. [examples: animated-spritefont-effects, 3d-castle-maze
  `TextFont`; a game project the editor r504 opened and previewed,
  2026-09-30]
- A project with Bundle addons set, such as the test project of an addon
  under development, holds `"bundleAddons": true` in `project.c3proj`, and
  each bundled addon's `usedAddons` entry has `"bundled": true` and its
  `"version"`. The addon itself is at `addons/<type>/<id>.c3addon`, and at
  `addons/effect/<id>.c3addon` for an effect. [observed in a project the
  editor r504 saved, 2026-10-03]
- Local Storage is an IndexedDB database named `c3-localstorage-` plus the
  project's `uniqueId`. So it survives closing the preview and is separate
  per project. A tool that rewrites `project.c3proj` must keep `uniqueId`,
  or the project loses its saved data. [runtime: exported c3runtime.js
  `_GetProjectStorage`; manual:
  scripting/scripting-reference/interfaces/istorage.md "unique to the specific
  project"]

## Timelines and custom eases

Each rule below comes from the editor's project loader and saver
(`projectResources.js`, r504), the official example `blacksmith-forge` and a
game project that the editor r504 opened and previewed on 2026-09-30.

- A timeline is `timelines/<name>.json`, listed by name under `timelines`
  `items` in `project.c3proj`. A custom ease (the **Eases** folder, which
  the editor calls transitions) is `timelines/transitions/<name>.json`. It
  is listed under the first subfolder of `timelines`, the one without a
  `name`. A subfolder with a `name` is a timeline folder.
- A custom ease file is `{"name", "linear": false, "purpose": "any",
  "transitionKeyframes": [...]}`. Each keyframe has `x`, `y`, the start
  anchor `sax`, `say` and the end anchor `eax`, `eay`. The anchors are
  offsets from the keyframe. `se` and `ee` say whether each anchor is
  used, and `sm` is `"cubic"` or `"linear"`. As in the runtime's built-in
  eases, the first keyframe is (0, 0) with its end anchor off, and the last
  is (1, 1) with its start anchor off. A timeline keyframe or a Tween
  action names the ease by its bare name.
- The Timeline controller is a single-global object type,
  `"plugin-id": "Timeline"`, with a `usedAddons` entry `{"type": "plugin",
  "id": "Timeline", "name": "Timeline controller", "author": "Scirra",
  "bundled": false}`.
- An instance track names one instance in a layout: `worldInstance` is its
  uid, `objectType` its type and `project` the project's `uniqueId`. `id`
  is the track ID that *Set instance* names. A template instance in a
  layout that never runs works, because *Set instance* puts the runtime
  instance in its place.
- A property keyframe holds `value` and `rValue`, which relative mode
  reads, and `aValue`, which absolute mode reads. Angles are in radians.
  An `angle` addon gives the direction of the segment that starts at that
  keyframe, `closest`, `clockwise` or `anti-clockwise`, and extra
  `revolutions`. The runtime turns in that direction even when it is the
  longer way. So write the direction of the change to the next keyframe,
  or `closest` ([plugins/timeline.md](../plugins/timeline.md)). A
  keyframe's `ease` is a built-in ease id or a custom ease's name.
- The editor saves *Use system timescale* as `ignoreSystemTimescale`, and
  the name is inverted. `true` follows the system time scale, `false`
  ignores it, and a file without the key follows it. The export writes the
  key's value to the runtime's `useSystemTimescale`.
- An instance track's `virtualPosition` is the editor's preview offset of
  the instance while the playhead is dragged. The runtime does not read
  it. The editor writes `"relativeFlags": 16383, "version": 1` after the
  offsets, whatever the file held, so a generator writes those. The 14
  bits, low to high, are z elevation, origin Y, origin X, opacity, angle,
  height, width, Y, X, scale Y, scale X, depth, scale Z and 3D rotation.
  2047 is the 2D bits alone, as in files from before the 3D offsets. A
  timeline file also ends with `"nestedData": {}`,
  `"childrenNestedData": {}` and `"transitionsData": []`. A save sometimes
  fills `transitionsData` with copies of the custom eases that the timeline
  uses. The editor reads them only when the timeline is pasted, so write
  `[]` in a file. [editor r504 `projectResources.js`; the exported
  `c3runtime.js` has no `virtualPosition`; observed in a game project,
  r504, October 2026: 2047 written with and without `version` came back
  16383]

## Naming an event to the user

The editor numbers events, but the JSON holds no event numbers. The
editor's margin and its Find results (`Event 15 action 2`) count blocks,
groups, function blocks, custom action blocks and script blocks per sheet
in document order, sub-events included. Variables, comments and includes
take no number, and the editor lists them under the next numbered event.
Quote these numbers to the user, never JSON line numbers. Read a
screenshot or a pasted Find result the same way. To find the JSON
behind a number, run the `construct3-agent-plugin` skill's
`scripts/print_sheet.py --outline <sheet>` in the project folder. It prints
each row with its number and its `sid`, the string to search the sheet file
for. Without `--outline`, it prints the same rows with their conditions and
actions as the editor words them. Read the sheet that way before and after
an edit.

## Checks before handing over

Run the skill's `scripts/check_project.py` on the project folder. Run it
from the copy installed in the project,
`.agents/skills/construct3-agent-plugin/`, or in place here with
`--project <folder>`. It checks that:

- the JSON parses
- every `objectClass`, instance variable and behavior name exists, families
  included
- `sid`, `uid` and `imageSpriteId` are unique
- every ACE `id` and parameter key is in `<Construct3-RAG>/data/c3-schemas/`
- every called function is defined with the right parameter count
- every object created at runtime has a template instance in some layout
- the project follows the rules the editor applies on opening, the table in
  `<Construct3-Agent-Skills>/plugin/skills/construct3-agent-plugin/references/checker-rules.md`

If it passes, open and preview the project with the skill's
`scripts/open_in_editor.py --preview`. It prints `opened`, or the editor's
own message that names the sheet, event and parameter it refused. Then it
prints the errors of the first 5 seconds of play, each with its event. The
preview, not the checker, catches an expression whose types do not fit.

The checks cannot tell what the game does: which instances a condition
picks, what order triggers fire in, what happens once a player acts. So ask
the user to open the project and preview it, and tell the user what to look
at.
