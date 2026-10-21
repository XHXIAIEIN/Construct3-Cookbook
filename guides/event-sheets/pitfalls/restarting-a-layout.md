# Event Sheet Pitfalls: Restarting a layout

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

- *Restart layout* and *Go to layout* bring the layout's instances back as
  placed. They keep every global variable and static local at its current
  value. So a countdown, a score or a count that a round starts from still
  holds its end value when the layout runs again. If a global countdown
  restarted the layout at 0, it is 0 on the next run, so it restarts the
  layout every tick. Set such a value under *On start of layout*. Or, where
  the game starts over, run *Reset global variables*, and *Reset static*
  for static locals. A countdown works better as a Timer on an object of
  the layout, started under *On start of layout*. The restart recreates the
  object with no timer running, so nothing is left to set back. [manual:
  system-reference/system-actions.md "Restart layout", "Go to layout",
  "Reset global variables"; project-primitives/events/variables.md "Static
  and constant variables"; behavior-reference/timer.md; observed in preview,
  2026-09-28]
- A global layer shares its content between layouts, but not its state.
  Each layout starts the layer with its initial visibility and
  interactivity, and it places the layer's instances again as placed. When
  a layout ends, the layer's instances are destroyed, like every instance of
  an object type without the *Global* property. An instance of a *Global*
  object type survives. So if a HUD layer is hidden or made non-interactive
  in one layout, it is visible and interactive in the next. An instance
  moved or faded on it is back as placed. Keep what the layer shows in
  global variables, and set it on the layer under *On start of layout* in
  every layout that uses the layer.
  [manual: project-primitives/layers.md "Global layers", the initial
  objects and the properties are shared;
  project-primitives/objects/instances.md "Global", all instances are
  destroyed when the layout ends unless the object type is global;
  observed in a minimal project, r506.2 preview, 2026-10-16: a global HUD
  layer hidden and made non-interactive, its sprite moved and faded, was
  visible and interactive in the next layout, with the sprite at its
  placed position and full opacity]
