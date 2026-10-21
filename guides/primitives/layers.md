---
addons: system/set-layer-interactive, _common/move-to-top
---

# Event Sheet Pitfalls: Layers

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A popup turns the layer under it off with *Set layer interactive* while
  it is open. The events of one trigger run one after the other on the
  same input, and each *On tap object* tests its object's layer as it
  runs. So if the close event turns the layer under the popup on again in
  its own action list, a later *On tap object* event of a button under
  the popup fires on the same tap. Put *Wait 0* before *Set layer
  interactive*, so the layer turns on in the next tick, after every event
  of that tap has run. The wait protects only the events of the same
  trigger. A close on *On touched object* runs at the press. But the *On
  tap object* of a button under it fires at the release, ticks later, when
  the layer is on again. So give the close and the buttons one trigger,
  *On tap object* for both. A button's event above the close event in the
  same sheet does not fire on that tap either. [manual:
  project-primitives/events/how-events-work.md "Events run top to bottom";
  runtime: exported c3runtime.js r504, the `TestAndSelectCanvasPointOverlap`
  of the entry on invisible instances above tests the layer as the
  condition runs; observed in a minimal project, r506.2 preview,
  2026-10-16: a tap on a close button over a button of the lower layer,
  which the close event turned on at once, counted on both buttons. With
  *Wait 0* before *Set layer interactive* it counted on the close button
  alone, and so with the lower button's event above the close event. With
  the close on *On touched object* and *Wait 0*, the lower button's *On
  tap object* counted and its *On touched object* did not]

- A blend mode such as *Destination in* changes only the pixels under the
  object's own quad. So if a mask sprite is the size of the shape that it
  reveals, everything outside its bounding box stays unchanged. Size the
  mask to cover everything that it must erase, or keep the content inside
  its box. Turn on *Force own texture* for the layer, because without it the
  blend changes the whole screen. [manual: project-primitives/layers.md
  "Force own texture"; example: mask-effect-puzzle, layer HiddenWorld;
  observed in a game project, 2026-09-17]

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
