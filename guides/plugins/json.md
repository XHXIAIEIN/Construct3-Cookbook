# Event Sheet Pitfalls: JSON

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- JSON `Type(path)` reads `"undefined"` for a path that is not there, and
  `"array"`, `"object"`, `"number"`, `"string"`, `"boolean"` or `"null"`
  otherwise. So an expression can test presence, while *Has key* works only
  as a condition: `"layers." & name & (JSON.Type("layers." & name &
  ".alt") = "array" ? ".alt" : ".main")`. [runtime: exported c3runtime.js
  r504, JSON `_GetTypeOf` returns `_JSONTypeOf` of the value, `typeof` for
  anything but null and arrays]

- The JSON plugin reads a path as keys separated by dots, so a key with a
  dot in it, `"menu.title"`, is looked for as `menu` and then `title`
  inside it, and *Has key* fails. Escape the dot in the path with a
  backslash, `my\.key`, and a backslash in a key with two, `my\\key`. An
  expression string has no escape character of its own, only the doubled
  quote, so `"my\.key"` is written as it is. Keys without dots need none
  of this, and a Dictionary reads every key whole. [manual:
  plugin-reference/json.md "Escaping",
  project-primitives/events/expressions.md on double quotes; observation in
  a studied project, 2026-10-06]

- The JSON plugin has no action that merges one object into another. *Set
  JSON* sets one key from a JSON string, and `GetAsCompactString(path)`
  reads one key as that string. So to split a large data file into several
  and still read them through one JSON object, parse each file into a
  second JSON object, then run *For each* on its path `""` and *Set
  JSON* in the main object at `Part.CurrentKey` to
  `Part.GetAsCompactString(Part.CurrentKey)`. The paths the events read stay
  the same, provided no two files share a top-level key, since the later
  file overwrites it. Several AJAX requests can share one tag. Each request
  sets `LastData` to its own response and then fires *On completed* for that
  tag, once per request and in the order the responses arrive. So request
  all files in one block, count them in a variable, merge each in *On
  completed*, and start the game in a sub-event when the count reaches 0.
  [manual: plugin-reference/json.md "For each", "Set JSON", "CurrentKey",
  "GetAsCompactString"; schema: plugins/json.json, no merge action; runtime:
  exported c3runtime.js r504, AJAX `onreadystatechange` sets `_lastData`
  and then calls `_TriggerComplete` for each request, `OnComplete` compares
  the tag; observed in a game project, r504, 2026-10-06: four data files
  requested with one tag, merged this way before the first level]
