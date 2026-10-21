# Event Sheet Pitfalls: Tiled Background

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- The *Set image X scale* and *Set image Y scale* actions of a Tiled
  Background and of a 9-patch take a percentage, but the layout file writes
  the same property as a fraction. So `"image-scale-x": 0.3333` in `layouts/`
  is `33.33` in an event, and an event that writes `Self.Width /
  Self.ImageWidth` shrinks the tile a hundredfold.
  *Set image Y offset* moves the image down as the offset grows. So a pattern
  that moves upward needs a falling offset, such as `P - time * speed % P`.
  Make the wrap `P` a whole number of tile periods, which also keeps the
  offset small as the manual asks. A 9-patch's image scale also scales its
  corners and edges, while a change of size alone keeps them at their size
  and stretches the middle. So a 9-patch that pops or shrinks as one piece
  sets its size to the rest size times the factor and its image scale to the
  rest image scale times the factor, in the same tick. [manual:
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
