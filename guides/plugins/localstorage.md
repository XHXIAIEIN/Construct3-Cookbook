# Event Sheet Pitfalls: Local Storage

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A Local Storage read is asynchronous. *Get item* and *Check item exists*
  only start it, and *On item get*, *On item exists* or *On item missing*
  runs a moment later. The trigger runs in the event sheet of the layout
  that is running then. So if the player leaves the layout before the read
  completes, a trigger that only that layout's sheet holds never runs.
  The value is never read. A later *Set item* from the value in memory then
  overwrites the save with an older one. Read the save once, in a first
  layout that leaves only after the read completes. Or put `NOT Is
  processing gets` and `NOT Is processing sets` on every input that leaves
  the layout or writes the save. [manual: plugin-reference/local-storage.md
  "Using Local Storage", "Is processing gets", "Is processing sets";
  example: airborne-explorer, MenuEvents, menu buttons; observed in a test
  project, r506.3 preview, 2026-10-24: with a 1 s *Wait* before the read,
  a level started before *On item exists* and completed wrote progress 2
  over a saved 3]

- A failed write fires *On error* and not *On item set*. The browser can
  refuse a write, for example when the storage quota is full. So a game
  that leaves the level in *On item set* keeps the player in the level for
  good. Handle *On error*: tell the player that the progress was not saved,
  and leave the layout there too. [manual:
  plugin-reference/local-storage.md "On error", "On item set"; runtime:
  r506.3 `plugins/data-and-storage/localstorage/c3runtime/runtime.js`,
  `SetItem` triggers `OnItemSet` after the write and only `OnError` in its
  `catch`; read from source, not observed]

- Each key is a read of its own, with its own triggers and its own race
  with the input. So with one key per value, every new field adds a read
  and a trigger. Such fields are stars per level, a best time or a
  setting. Keep the whole save in one Dictionary, or one JSON object if it
  nests, with a `version` key for later changes of the layout of the save.
  Read it once at the start with *Get item*, and load it into the
  Dictionary with *Load* from `ItemValue`. In *On item missing*, load the
  defaults. During the game, read and change the Dictionary at once, with
  no trigger. To save, run *Set item* with `AsJSON` under the one key, and
  leave the layout in *On item set*. [manual:
  plugin-reference/local-storage.md "Simplifying usage with Dictionary";
  examples: airborne-explorer, MenuEvents group "Player Profile";
  eventide, EventsMainMenu; both keep `DictProfile` under the key
  `"Profile"` and load `DefaultProfile.json` when it is missing]
