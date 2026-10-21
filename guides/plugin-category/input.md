# Event Sheet Pitfalls: Input plugins

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Keyboard and Gamepad have separate conditions, so a game that takes both
  writes every input event twice, and a menu that tests *On key pressed*
  misses the gamepad. Route both through one input object: an invisible
  sprite, or globals, with a number per control (up, down, left, right,
  confirm, cancel) and a copy of each from the last tick. At the top of the
  sheet, every tick, copy each control into its last value and set it to 0.
  Then a Keyboard group and a Gamepad group set a control to 1 while its
  key, button or stick past the dead zone is down. Every consumer tests a
  press as `confirm > lastConfirm`, a hold as `confirm = 1` and a release as
  `confirm < lastConfirm`, and a touch layer added later writes the same
  numbers. The copy and the clear come before the groups that write, so a
  consumer anywhere below them reads this tick's state. [observation in a
  studied project, 2026-10-06]
