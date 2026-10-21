# Event Sheet Pitfalls: Dictionary

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Dictionary *Set key* changes only an existing key and silently ignores
  a missing one. *Add key* creates or overwrites, so write gates and
  counters with *Add key*. [manual: plugin-reference/dictionary.md
  "Add key", "Set key"; runtime: `scripts/c3runtime.js` of an exported
  r503/r504 web build, `SetKey(t,e){this._data.has(t)&&...}`, `AddKey`]
