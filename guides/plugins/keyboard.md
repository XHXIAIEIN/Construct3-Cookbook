# Event Sheet Pitfalls: Keyboard

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A game that moves with W, A, S and D alone is hard to control on an AZERTY
  keyboard. On that keyboard, those letters sit elsewhere, and ZQSD takes
  their place. Give every direction its arrow key too, because the arrow
  keys work on most keyboard layouts. Put the arrow key in an OR block
  with the letter or in an event of its own. The same holds for any
  control chosen for where its key sits. The 8 Direction, Platform and Car
  behaviors move with the arrow keys while *Default controls* is on. If a
  project turns it off to simulate controls from letters, add the arrow
  keys in the project's own events.
  [manual: plugin-reference/keyboard.md, the note on keyboard
  layouts; behavior-reference/8-direction.md, platform.md and car.md "Default
  controls"; example: detecting-input-method, `Game events` 5 to 8: each
  direction an OR block of its arrow key and its letter, simulating 8
  Direction]
