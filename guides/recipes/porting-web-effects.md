# Porting a web or WebGL effect

If the events rebuild an effect from a web page, such as a canvas or WebGL
demo, read this page. It says how the source's units and its frame steps
map onto a Construct project, so the port moves and sizes as the source
does. Design the events first with
[design/thinking.md](../design/thinking.md). For drawing the effect's
lines and shapes, read [plugins/drawingcanvas.md](../plugins/drawingcanvas.md).

## Sizes

- Under *Scale inner* or *Scale outer*, a layout px is not a CSS px,
  because the runtime scales the viewport to fill the window. A size that
  the source gives in CSS px, such as a line 20 to 50 px wide, stays that
  many CSS px at any window size. So convert it every tick: set a variable
  to `ViewportHeight("Layer") / PlatformInfo.CanvasCssHeight`, the layout
  px per CSS px, and multiply the source's sizes by it. Compute it every
  tick, because the window can change size.
  [manual: plugin-reference/platform-info.md, "CanvasCssHeight";
  observed in a game project, r506.3 preview, 2026-10-28]
- Some sizes the source gives as a share of the window, in clip space
  from -1 to 1 or as a fraction of `innerWidth` and `innerHeight`. Take
  such a size as a share of what the player sees, `ViewportWidth("Layer")`
  and `ViewportHeight("Layer")`. The layout's size and the project's
  viewport size are not what the player sees, because *Scale inner* crops
  the viewport to the window's shape and *Scale outer* shows more than it.
  Clip space spans 2 across, so 0.02 of it is 0.01 of the visible height.
  [observed in a game project, r506.3 preview, 2026-10-28]

## Frame steps

- An effect that steps once per `requestAnimationFrame` with no time
  factor, such as a spring, a friction or a lerp by 0.9, runs faster on a
  screen with a higher refresh rate. Port it as one step per tick, with
  no `dt`, so it matches the source on the same screen. This is the one
  case in which a constant lerp factor is right. The row for a smooth
  follow in the "Native first" table of
  [design/thinking.md](../design/thinking.md) still holds for a game's
  own motion: the port copies the source's dependence on the frame rate
  on purpose. [observed in a game project, r506.3 preview, 2026-10-28]
- Do not scale such a step by `fps * dt` to keep the source's pace at any
  frame rate. `fps * dt` reads about 1 under vsync, lags behind for a
  while after the refresh rate changes, and jitters from tick to tick, so
  the motion stutters. If the port must not depend on the frame rate,
  rewrite the step with `dt`, as in `lerp(a, b, 1 - f ^ dt)`, and tune `f` until
  it matches the source at the source's usual refresh rate.
  [observed in a game project, r506.3 preview, 2026-10-28]
