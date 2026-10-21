# Event Sheet Pitfalls: Sprite font

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A Sprite Font draws each character as its whole cell of the image, then
  moves on by the character's width from *Spacing data*. So paint each glyph
  against the left edge of its cell. An outline that reaches past that width
  into the next cell stays whole, and the next character is drawn over it. The
  font's colour and *Set color* tint every pixel, the outline as well. So bake
  each colour into its own image, one object per colour, as white and gold
  damage numbers take two. A character that would end past the box's width is
  not drawn. A line taller than the box is drawn from the top instead of
  centred. So size the box for the longest text at the largest scale a pop
  tween reaches. [manual: plugin-reference/sprite-font.md "Re-coloring
  SpriteFonts", "Sprite font"; editor r504
  `plugins/general/spritefont/spritefontText.js` `Draw`, `_LayoutText`;
  observed in a game project, r504 preview, 2026-09-30]

- A Sprite Font's *Character spacing* property, which *Set character
  spacing* changes, is added between characters, in layout pixels. Its
  *Scale* property and *Set scale* do not scale it, and nothing is added
  after the last character. `TextWidth` is in layout pixels after the scale:
  the widths from *Spacing data* times the scale, plus the spacing between
  characters. So two characters 20 px wide at a scale of 1/3 read 13.33 at
  spacing 0. The spacing is the same between every pair of characters, so a
  wide spacing splits a number of several digits into digits that read
  apart. Keep the spacing at 0 and put a space character where a gap is
  wanted. [observed in
  a game project, r504 preview, 2026-10-05: a three-character string at scale
  1/3 read `TextWidth` 72.33 at spacing 0 and 92.33 at spacing 10, and one
  character read the same at both]

- *Spacing data* and *Set character width* set the same per-character
  width. The property shows in the Layout View and takes a whole font at
  once, `[[10, "aeou"], [6, "il"]]`, so a font's widths belong there. The
  action is for a width that changes at runtime. A full-width space (U+3000)
  is a character like any other, so give it its own width in a Japanese or
  Chinese font, or it takes the cell width. [manual:
  plugin-reference/sprite-font.md "Spacing data", "Set character width";
  observation in a studied project, 2026-10-06: a font's widths set by
  actions on start, and the full-width space tested by hand in every width
  expression]
