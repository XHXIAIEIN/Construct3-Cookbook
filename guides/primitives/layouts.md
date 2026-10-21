# Event Sheet Pitfalls: Layouts

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- The origin (0, 0) is the top-left of the layout, and Y grows downwards.
  So up is `Y - n`, gravity pulls towards +Y, and the top of the screen is
  the smallest Y. [manual: tips-and-guides/common-conventions.md "Units"]

- `ViewportLeft`, `ViewportWidth` and the other viewport expressions take
  a layer, because a parallaxed or scaled layer shows a different
  rectangle. Write `ViewportLeft("HUD")`. `LayoutWidth` is the whole
  layout. `ViewportWidth(layer)` is the part on screen, in layout
  coordinates. `OriginalViewportWidth` is the project's *Viewport size*
  property. [manual:
  system-reference/system-expressions.md "Viewport", "Layout";
  plugins/system.json: every `Viewport*` expression has a `layer` parameter]
