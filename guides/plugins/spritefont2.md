# Event Sheet Pitfalls: Sprite font

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

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
