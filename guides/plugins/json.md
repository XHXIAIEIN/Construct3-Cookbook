# Event Sheet Pitfalls: JSON

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- JSON `Type(path)` reads `"undefined"` for a path that is not there. For
  other paths it reads `"array"`, `"object"`, `"number"`, `"string"`,
  `"boolean"` or `"null"`. So an expression can test whether a path
  exists, as in `"layers." & name & (JSON.Type("layers." & name &
  ".alt") = "array" ? ".alt" : ".main")`. *Has key* does that only as a
  condition. [runtime: exported c3runtime.js
  r504, JSON `_GetTypeOf` returns `_JSONTypeOf` of the value, `typeof` for
  anything but null and arrays]

- The JSON plugin reads a path as keys separated by dots. So it looks for
  a key with a dot in it, such as `"menu.title"`, as `menu` and then
  `title` inside `menu`, and *Has key* fails. In the path, escape a dot
  with a backslash, `my\.key`, and escape a backslash in a key with two,
  `my\\key`. An expression string has only the doubled quote as an escape,
  so write `"my\.key"` as it is. Keys without dots need none of this. A
  Dictionary reads every key whole. [manual:
  plugin-reference/json.md "Escaping",
  project-primitives/events/expressions.md on double quotes; observation in
  a studied project, 2026-10-06]

- The JSON plugin has no action that merges one object into another, so
  copy the keys one at a time. *Set JSON* sets one key from a JSON string,
  and `GetAsCompactString(path)` reads one key as such a string. So if a
  large data file is split into several files that the events still read
  through one JSON object, parse each file into a second JSON object,
  `Part`. Then run *For each* on its path `""`, and in the main object *Set
  JSON* at `Part.CurrentKey` to `Part.GetAsCompactString(Part.CurrentKey)`.
  The paths that the events read stay the same if no two files share a
  top-level key. If two files share one, the later file overwrites it.
  Several AJAX requests can share one tag. Each request sets `LastData` to
  its own response and then fires *On completed* for that tag. This
  happens once per request, in the order that the responses arrive. So
  request all files in one block, and count them in a variable. Merge each
  file in *On completed*, and start the game in a sub-event when the count
  reaches 0.
  [manual: plugin-reference/json.md "For each", "Set JSON", "CurrentKey",
  "GetAsCompactString"; schema: plugins/json.json, no merge action; runtime:
  exported c3runtime.js r504, AJAX `onreadystatechange` sets `_lastData`
  and then calls `_TriggerComplete` for each request, `OnComplete` compares
  the tag; observed in a game project, r504, 2026-10-06: four data files
  requested with one tag, merged this way before the first level]
