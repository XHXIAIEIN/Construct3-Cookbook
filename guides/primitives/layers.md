# Event Sheet Pitfalls: Layers

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A popup turns the layer under it off with *Set layer interactive* while
  it is open. The events of one trigger run one after the other on the
  same input, and each *On tap object* tests its object's layer as it
  runs. So if the close event turns the layer under the popup on again in
  its own action list, a later *On tap object* event of a button under
  the popup fires on the same tap: the press goes through. Put *Wait 0*
  before *Set layer interactive*, so the layer turns on in the next tick,
  after every event of that tap has run. The wait protects only the events
  of the same trigger. A close on *On touched object* runs at the press,
  and a button's *On tap object* under it fires at the release, ticks
  later, when the layer is on again. So give the close and the buttons
  one trigger, *On tap object* for both. The button's event above the
  close event in the same sheet does not fire on that tap either. [manual:
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
  object's own quad. So a mask sprite the size of the shape it reveals leaves
  everything outside its bounding box unchanged. The layer needs
  *Force own texture*, or the blend changes the whole screen. Size the mask to
  cover everything it must erase, or keep the content inside its box. [manual:
  project-primitives/layers.md "Force own texture"; example:
  mask-effect-puzzle, layer HiddenWorld; observed in a game project,
  2026-09-17]

- A layout draws its layers bottom to top, and on one layer the instances in
  the order the layout file lists them: the first is at the back. A
  draggable piece listed before the slot or box it is dropped on is drawn
  under it, so the piece snapped into the box disappears. Put the piece on a
  layer above, list it after its target, or raise it as it is picked up with
  *Move to top* in Drag & Drop *On drag start*. Seven of the ten official
  examples that test a dragged object against a target raise it at runtime
  (`alchemist`, `family-tree`, `place-stickers` among them).
  `check_project.py` warns on a drop test or a snap whose piece the layout
  draws under its target, and `edit_sheet.py` refuses one a plan adds.
  [manual: project-primitives/objects/instances.md "Z index", 0 is the
  bottom; interface/bars/z-order-bar.md; observed in a generated drag-and-snap
  demo, r495.2 preview, 2026-10-09: the block, listed before the target on
  one layer, snapped to the target's centre and was hidden behind it]

- A global layer shares its content between layouts, not its state. Each
  layout starts the layer with its initial visibility and interactivity
  and places its instances again as placed. The layer's instances are
  destroyed when a layout ends, like every instance of an object type
  without the *Global* property; an instance of a *Global* object type
  survives. So a HUD layer hidden or made non-interactive in one layout is
  visible and interactive in the next, and an instance moved or faded on
  it is back as placed. Keep what the layer shows in global variables, and
  write it under *On start of layout* in every layout that uses the layer.
  [manual: project-primitives/layers.md "Global layers", the initial
  objects and the properties are shared;
  project-primitives/objects/instances.md "Global", all instances are
  destroyed when the layout ends unless the object type is global;
  observed in a minimal project, r506.2 preview, 2026-10-16: a global HUD
  layer hidden and made non-interactive, its sprite moved and faded, was
  visible and interactive in the next layout, with the sprite at its
  placed position and full opacity]
