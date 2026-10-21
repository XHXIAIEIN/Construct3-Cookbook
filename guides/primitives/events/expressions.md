# Event Sheet Pitfalls: Expressions

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

- There is no null or undefined. An expression is a number or a text, and a
  missing value reads as the number 0. `Array.At` outside the array,
  `Dictionary.Get` of a key that is not there, the deprecated Function
  plugin's `Function.ReturnValue` when nothing set it and a Timer's
  `CurrentTime` after a one-off timer fired all give 0. `Array.IndexOf`
  gives -1, `int("33xx")` is 33 and `int("xx33")` is 0. So `= 0` cannot
  tell an empty slot from a missing one. Test *Has key*, *Contains value*
  or `Array.Width` first, or use
  `Dictionary.GetDefault(key, fallback)`. [manual:
  plugin-reference/array.md "At", "IndexOf"; plugin-reference/dictionary.md
  "Get", "GetDefault", "Has key"; plugin-reference/function.md
  "ReturnValue"; behavior-reference/timer.md "CurrentTime";
  system-reference/system-expressions.md "int", "float"]
