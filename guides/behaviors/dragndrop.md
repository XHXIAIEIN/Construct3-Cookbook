# Event Sheet Pitfalls: Drag & Drop

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- While a dragged or tweening instance has collisions disabled, the slot
  where it will land reads empty until it lands, the slot it is flying back
  to included. The drop events expect that. But an event that fills empty
  slots on its own (a buy button or a spawn) puts a new instance there, and
  the returning one lands on top of it. Make such an event wait while any
  instance is being dragged or its landing tween is playing. [observed in a
  game project, r504 preview, 2026-10-01: a piece dropped back on its slot,
  the buy button pressed within its 0.2 s snap, the bought weapon landed on
  the piece]

- Drag & Drop moves the dragged instance only when the pointer moves. It sets
  the position to the pointer minus the grab offset, and a tick without
  movement writes nothing. A *Set position* on the dragged instance holds
  while the finger rests, but the next move overwrites it. So put a look that
  trails or lifts above the finger on a child the events position. Drops and
  overlaps are still judged by the dragged instance. [runtime: exported
  c3runtime.js r503, `Behaviors.DragnDrop` `_OnMove`, called from the
  `pointermove` dispatch only; observed in a game project, r503 preview,
  2026-09-29]

- Drag & Drop starts one drag per press, on the front instance under the
  pointer: the one on the highest layer, then the one highest in Z order on
  that layer. It considers only instances whose behavior is enabled and
  whose layer is interactive, of every object type that has the behavior. It
  ignores visibility, of the instance and of its layer. A popup without
  Drag & Drop takes no part, so the pieces under it can still be dragged, and
  a hidden piece or a piece on a hidden layer is dragged too. To stop drags
  while a popup shows, turn the pieces' layer off with
  *Set layer interactive*, or the behavior with *Set enabled*. [runtime:
  exported c3runtime.js r504, `Behaviors.DragnDrop` `_OnInputDown` skips an
  instance whose behavior is disabled or whose layer fails
  `IsSelfAndParentsInteractive`, then keeps the instance with the highest
  layer index, then the highest Z index; observed in a minimal project, r504
  preview, 2026-10-05: of two overlapping instances on two layers, the upper
  layer's dragged, also with that layer hidden and with that instance
  hidden, and the lower one dragged once the upper layer was not interactive;
  of two on one layer, the higher in Z dragged]
