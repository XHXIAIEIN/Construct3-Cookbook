# Event Sheet Pitfalls: Text

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A Text object has no *Set color*. A Text's colour is its font colour, so
  set it with *Set font color* (`set-font-color`). `plugins/_common.json`
  lists `set-default-color`, but the editor refuses that action on a Text
  with `missing action id 'set-default-color'`, and then the project does
  not open. A plugin file lists the shared ACEs that it gets under
  `commonAces`. `lookup_ace.py` and `check_project.py` follow that list, so
  `lookup_ace.py Text color` prints only *Set font color*.
  [plugins/text.json `set-font-color`; observed in a game project, r495.2
  editor, 2026-09-23]

- A Text object wraps at its own width and draws only the lines that fit
  its height. So if the text is longer than the placeholder that the box
  was sized for, the lines that do not fit are cut off. Under centre or
  bottom vertical alignment, the lines already shown also move up. Size the
  box for the longest text at its font size and line height. Or, after *Set
  text*, keep the width fixed and set the height to `Self.TextHeight` plus a
  margin. `TextWidth` and `TextHeight` measure the text as wrapped inside
  the current box, so `TextWidth` never grows the box past its width. Both
  expressions are current in the action right after *Set text*. Before you
  choose the size, check what else moves the lines:
  - Origin: a resize keeps the origin still and grows the box away from it.
    With a top origin, the first line stays in place. With a centre origin,
    the box grows both ways, and the first line moves even under top
    alignment. Put the origin on the edge that the text must keep, as a bar
    keeps the edge that it grows from.
  - Wrapping: *Word* breaks only at spaces and hyphens. So set *CJK* for
    Chinese, Japanese or Korean text, because it breaks between characters
    and wraps CJK punctuation correctly. The same string takes a different
    number of lines under each mode, so size the box for the current mode.
  - Direction and horizontal alignment decide the edge that a line starts
    from. So if an RTL or right-aligned text with a left origin is widened,
    the text moves. [inference from the manual's property descriptions,
    unverified at runtime]
  [manual: plugin-reference/text.md "Wrapping", "Vertical alignment", "Text
  direction", "Origin", "TextWidth"; examples: text-based-adventure
  `Set height to min(Self.TextHeight + 4, 644)`, flowchart-questionnaire sizes
  a background from `TextWidth + 10`, `TextHeight + 10`; observed: 2026-09-23]

- A Text object draws a single line that is taller than its box, with the
  bottom of the glyphs cut off at the box edge. The font size is in points,
  so a line needs about `size × 4/3 × 1.2` pixels of height. In one project,
  a 44 pt bold price in a 46 px tall box lost the bottom of its digits. If
  events change the size with *Set font size* at runtime, such as for a
  bigger critical hit number, size the box for the largest size. [manual:
  plugin-reference/text.md "Size"; observed in a game project, 2026-09-28]

- A Text object draws its text into a texture of its own. If the text or
  the font size changes, the object redraws that texture and uploads it
  again on the next frame. So a *Set font size* in every tick of a pop tween
  redraws the text and uploads a texture every frame, at the device's full
  resolution. In one game project, each damage number that popped this way
  was redrawn every frame. This made 175 texture uploads a second at 144 Hz,
  which was most of the Text cost of the whole game. *Set text* to the
  string already shown costs nothing, because the runtime compares the
  strings and returns. Animate a number by moving its finished texture:
  change its position, angle or opacity. Or draw the number with a Sprite
  Font and tween its *Scale*, which redraws nothing. With that tween, the
  same project redrew no damage number and no countdown. *Set resolution
  mode* to *Fixed* stops only the redraws that the display scale causes,
  not the redraws that the font size causes.
  [manual: plugin-reference/text.md "Set resolution
  mode"; observed in a game project, r504 export, runtime `_SetText` source
  and a counter on `_OnBeforeRender`, 2026-09-30]

- A Text object takes one font family, not a CSS font list. The runtime
  puts the whole font name in quotes as one family, unless the name is a
  generic family such as `sans-serif`. So the *Font* property or *Set font
  face* with `Inter, "PingFang SC", sans-serif` names a family that does
  not exist, and the text draws in the browser's default face, a serif in
  Chrome. Give one name: a font file of the project by its name, or one
  generic family. A character that the font lacks, such as a Chinese
  character in Inter, already falls back to a face of the platform, so it
  needs no list. [runtime `lib/gfx/text.js` `_GetFontString`, r506.3;
  observed in a Chrome 152 canvas, where `12pt "Arial, Microsoft YaHei,
  sans-serif"` measured the same width as `12pt serif`, 2026-10-30]
