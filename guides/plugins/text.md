# Event Sheet Pitfalls: Text

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A Text object has no *Set color*. `plugins/_common.json` lists
  `set-default-color`, but the editor refuses it on a Text with
  `missing action id 'set-default-color'`, and the project does not open. A
  Text's colour is its font colour: *Set font color* (`set-font-color`). A
  plugin file lists the shared ACEs it gets under `commonAces`, and
  `lookup_ace.py` and `check_project.py` follow it, so
  `lookup_ace.py Text color` prints only *Set font color*.
  [plugins/text.json `set-font-color`; observed in a game project, r495.2
  editor, 2026-09-23]

- A Text object wraps at its own width and draws only the lines that fit its
  height. Text longer than the box sized for the placeholder gains a cut-off
  line. With centre or bottom vertical alignment, the lines already shown also
  move up. Size the box for the longest text at the font size and line height.
  Or, after *Set text*, resize it from `Self.TextHeight` plus a margin, with
  the width fixed. `TextWidth` and `TextHeight` measure the text as wrapped
  inside the current box, so `TextWidth` never grows the box past its width.
  Both are current in the action right after *Set text*. Check what else moves
  the lines before choosing the size:
  - Origin: a resize keeps the origin still and grows the box away from it.
    With a top origin, the first line stays in place. With a centre origin,
    the box grows both ways, and the first line moves even under top
    alignment. Put the origin on the edge the text must keep, as a bar keeps
    the edge it grows from.
  - Wrapping: *Word* breaks only at spaces and hyphens. So Chinese, Japanese
    or Korean text needs *CJK*, which breaks between characters and wraps CJK
    punctuation correctly. The same string takes a different number of lines
    under each mode, so size for the current mode.
  - Direction and horizontal alignment decide the edge a line starts from, so
    a widened RTL or right-aligned text with a left origin moves. [inference
    from the manual's property descriptions, unverified at runtime]
  [manual: plugin-reference/text.md "Wrapping", "Vertical alignment", "Text
  direction", "Origin", "TextWidth"; examples: text-based-adventure
  `Set height to min(Self.TextHeight + 4, 644)`, flowchart-questionnaire sizes
  a background from `TextWidth + 10`, `TextHeight + 10`; observed: 2026-09-23]

- A single line taller than its Text box is not hidden. It draws with the
  bottom of the glyphs cut off at the box edge. Size is in points, so a line
  needs about `size × 4/3 × 1.2` pixels of height. A 44 pt bold price in a
  46 px tall box lost the bottom of its digits. For a *Set font size* at
  runtime, such as a bigger critical hit number, size the box for the largest
  size. [manual: plugin-reference/text.md "Size"; observed in a game project,
  2026-09-28]

- A Text object draws its text into a texture of its own. A change of text or
  font size redraws and re-uploads that texture on the next frame. So a *Set
  font size* every tick during a pop tween redraws the text and uploads a
  texture every frame, at the device's full resolution. In one game project,
  each damage number that popped this way was redrawn every frame: 175
  texture uploads a second at 144 Hz, most of the Text cost of the whole
  game. *Set text* to the string already shown costs nothing, because the
  runtime compares and returns. Animate a number by moving its finished
  texture (position, angle, opacity). Or draw it with a Sprite Font and
  tween its *Scale*, which redraws nothing: with that tween, the same
  project redrew no damage number and no countdown. *Set resolution mode*
  to *Fixed* only stops redraws caused by the display scale, not by the
  font size.
  [manual: plugin-reference/text.md "Set resolution
  mode"; observed in a game project, r504 export, runtime `_SetText` source
  and a counter on `_OnBeforeRender`, 2026-09-30]
