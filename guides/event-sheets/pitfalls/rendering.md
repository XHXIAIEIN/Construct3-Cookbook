# Event Sheet Pitfalls: Rendering

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

- A Text object has no *Set color*. A Text's colour is its font colour, so
  set it with *Set font color* (`set-font-color`). `plugins/_common.json`
  lists `set-default-color`, but the editor refuses that action on a Text
  with `missing action id 'set-default-color'`, and then the project does
  not open. A plugin file lists the shared ACEs that it gets under
  `commonAces`. `lookup_ace.py` and `check_project.py` follow that list, so
  `lookup_ace.py Text color` prints only *Set font color*.
  [plugins/text.json `set-font-color`; observed in a game project, r495.2
  editor, 2026-09-23]
- *Set width* stretches the whole image of a Sprite and repeats the image
  of a Tiled Background. On a 9-patch, it stretches or tiles the middle, and
  the corners keep their size. So make a bar with a painted fill a Tiled
  Background, because below its own width it shows a cut of the painting.
  Make a bar with caps a 9-patch, and keep its width positive. [manual:
  plugin-reference/tiled-background.md "display an image in a repeating
  pattern"; plugin-reference/9-patch.md "a Sprite object, which just stretches
  its entire image", "useful for representing things like progress bars";
  reference: recipes/progress-bars.md]
- The *Set image X scale* and *Set image Y scale* actions of a Tiled
  Background and of a 9-patch take a percentage, but the layout file writes
  the same property as a fraction. So `"image-scale-x": 0.3333` in
  `layouts/` is `33.33` in an event. An event that writes `Self.Width /
  Self.ImageWidth` shrinks the tile a hundredfold. *Set image Y offset*
  moves the image down as the offset grows. So if a pattern must move
  upward, give it a falling offset, such as `P - time * speed % P`. Make the
  wrap `P` a whole number of tile periods. This also keeps the offset small,
  as the manual asks. The image scale of a 9-patch also scales its corners
  and edges. A change of size alone keeps them at their size and stretches
  the middle. So if a 9-patch must pop or shrink as one piece, set two
  values in the same tick: its size to the rest size times the factor, and
  its image scale to the rest image scale times the factor. [manual:
  plugin-reference/tiled-background.md "stretching ... by a percentage",
  "wrapping the image offset back to 0"; plugin-reference/9-patch.md "Image
  scale X": the patches are drawn with the scale, "increasing the visual size
  of the margins"; runtime: exported c3runtime.js r504,
  `TiledBg.Acts.SetImageScaleX` and `NinePatch.Acts.SetImageScaleX` divide by
  100; observed in a game project, r504 preview, 2026-10-01: a scale of width
  ÷ image width read 0.0019 through the script interface, and screenshots
  0.12 s apart showed the chevrons moving down while the offset grew; observed
  in a game project, r504 preview, 2026-10-05: a 9-patch given size and image
  scale together each tick popped as one piece]
- A bar grows from its origin. Every filling bar in the examples has its
  origin on the edge that it grows from, (0, 0) or (0, 0.5). A cover that
  hides the bar from the right has its origin at (1, 0.5). With an origin
  of 0.5, a bar grows both ways from the middle. [examples: berry-harvester
  ProgressBar, jetpack FuelBar, flatland-golf PowerBarCover, test-your-might
  MightLevelBar (0.5, 1)]
- If *Convex* is off, Drawing Canvas *Fill polygon* draws nothing when two
  consecutive points of the polygon coincide. A closing point that repeats
  the first point is such a pair. The rest of the sheet keeps running, and
  no error is logged. If *Convex* is on, the same points fill. So add a
  closing point only if it is a point of its own, or count the points in a
  variable and loop over that count. A convex shape can also tick *Convex*.
  [observed in a game project, r502 preview, 2026-09-24; observed in a
  minimal project, r504 preview, 2026-10-02: a square filled 5776 pixels,
  the same square with its first point, a middle point or a closing point
  repeated filled 0, and all three filled 5776 with *Convex* on; reported as
  Scirra/Construct-bugs#9292, open]
- A blend mode such as *Destination in* changes only the pixels under the
  object's own quad. So if a mask sprite is the size of the shape that it
  reveals, everything outside its bounding box stays unchanged. Size the
  mask to cover everything that it must erase, or keep the content inside
  its box. Turn on *Force own texture* for the layer, because without it the
  blend changes the whole screen. [manual: project-primitives/layers.md
  "Force own texture"; example: mask-effect-puzzle, layer HiddenWorld;
  observed in a game project, 2026-09-17]
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
- *Move to top* moves only the instance that it runs on, and the children
  of a hierarchy keep their places in the Z order. So if the parent of a
  dragged piece goes to the top, the piece's body, face and label still draw
  under the pieces created after it. Pick the children with *Pick children*
  and move every part to the top, bottom part first, in the order that the
  parts must stack. [manual:
  plugin-reference/common-features/common-actions.md "Move to top", "top of
  its current layer"; observed in a game project, r503 preview, 2026-09-29;
  observed in a minimal project, r504 preview, 2026-10-02, through the
  scripting `moveToTop()`: the parent went from Z index 10 to the top, its
  child stayed below an instance created after it]
- A layout draws its layers from bottom to top. On one layer, it draws the
  instances in the order that the layout file lists them, so the first
  instance is at the back. If a draggable piece is listed before the slot or
  box that it is dropped on, the piece is drawn under that target. Then the
  piece disappears when it snaps into the box. Put the piece on a layer
  above, list it after its target, or raise it with *Move to top* in Drag &
  Drop *On drag start* as it is picked up. Seven of the ten official
  examples that test a dragged object against a target raise it at runtime,
  among them `alchemist`, `family-tree` and `place-stickers`.
  `check_project.py` warns on a drop test or a snap whose piece the layout
  draws under its target. `edit_sheet.py` refuses such a test or snap when a
  plan adds it.
  [manual: project-primitives/objects/instances.md "Z index", 0 is the
  bottom; interface/bars/z-order-bar.md; observed in a generated drag-and-snap
  demo, r495.2 preview, 2026-10-09: the block, listed before the target on
  one layer, snapped to the target's centre and was hidden behind it]
- *Set color* is a tint: it multiplies each channel of the image by the
  colour, and white restores the original. A part drawn in white takes the
  colour exactly, and black outlines stay black. But white highlights take
  the tint too. So if a piece is coloured by level, draw it with a white
  fill, and draw its highlights on a separate child that keeps its colour.
  [manual: plugin-reference/common-features/common-actions.md "Set color";
  observed in a game project, r503 preview, 2026-09-29]
- `rgbEx` and `rgba` take each channel from 0 to 100, and `rgbEx255` and
  `rgba255` take each channel from 0 to 255. `rgbEx` clamps a channel past
  100, so a colour written on the 0-255 scale draws paler. In one demo, a
  blue drew pale, and grey lines of `#DEDEDE` drew white. Write a fixed
  colour as `HexColor("#RRGGBB")` and a computed colour as
  `rgbEx255(r, g, b)`. Do not use the deprecated `rgb`. [manual:
  system-reference/system-expressions.md "rgbEx"; observed in an Array
  IndexOfY demo, r506.3 preview, 2026-10-20]
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
- A Sprite Font draws each character as its whole cell of the image. Then
  it moves on by the character's width from *Spacing data*. So paint each
  glyph against the left edge of its cell. If an outline reaches past that
  width into the next cell, the outline stays whole, and the next character
  is drawn over it. The font's colour and *Set color* tint every pixel, the
  outline as well. So bake each colour into its own image, with one object
  per colour: white and gold damage numbers take two objects. The font does
  not draw a character that would end past the box's width. It draws a line
  that is taller than the box from the top instead of centred. So size the
  box for the longest text at the largest scale that a pop tween reaches.
  [manual: plugin-reference/sprite-font.md "Re-coloring
  SpriteFonts", "Sprite font"; editor r504
  `plugins/general/spritefont/spritefontText.js` `Draw`, `_LayoutText`;
  observed in a game project, r504 preview, 2026-09-30]
- A Sprite Font adds its *Character spacing* property between characters,
  in layout pixels, and *Set character spacing* changes it. The *Scale*
  property and *Set scale* do not scale the spacing, and the font adds no
  spacing after the last character. `TextWidth` is in layout pixels after
  the scale: the widths from *Spacing data* times the scale, plus the
  spacing between characters. So two characters 20 px wide at a scale of
  1/3 read 13.33 at spacing 0. The spacing is the same between every pair of
  characters, so a wide spacing splits a number of several digits into
  digits that read as separate. Keep the spacing at 0, and put a space
  character where the text needs a gap. [observed in
  a game project, r504 preview, 2026-10-05: a three-character string at scale
  1/3 read `TextWidth` 72.33 at spacing 0 and 92.33 at spacing 10, and one
  character read the same at both]
- *Set canvas size* changes the size of the viewport and, with it, the
  project's *Window size*. So if a 4:3 game is shown inside a 16:9 window,
  its viewport grows and shows more of the layout at the sides. To keep the
  game where it was, *Scroll to position* back to the centre of the play
  area. Cover the extra width on each side with a bar sprite on the top
  layer. [plugins/system.json
  `set-canvas-size`, "also altering the 'Window size' project property";
  observation in a studied project, 2026-10-06]
- *Spacing data* and *Set character width* set the same width per
  character. The property shows in the Layout View and takes a whole font
  at once, as in `[[10, "aeou"], [6, "il"]]`, so set a font's widths there.
  Use the action for a width that changes at runtime. A full-width space
  (U+3000) is a character like any other. So in a Japanese or Chinese font,
  give it its own width, because otherwise it takes the cell width. [manual:
  plugin-reference/sprite-font.md "Spacing data", "Set character width";
  observation in a studied project, 2026-10-06: a font's widths set by
  actions on start, and the full-width space tested by hand in every width
  expression]
