# Event Sheet Pitfalls: Drag & Drop

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- While a dragged or tweening instance has collisions disabled, the slot
  where it will land reads as empty until it lands. This includes the slot
  that it is flying back to. The drop events rely on this. But an event
  that fills empty slots by itself, such as a buy button or a spawn,
  creates an instance there. Then the returning instance lands on top of
  it. Make such an event wait while the player drags any instance or any
  landing tween plays. [observed in a
  game project, r504 preview, 2026-10-01: a piece dropped back on its slot,
  the buy button pressed within its 0.2 s snap, the bought weapon landed on
  the piece]

- Drag & Drop moves the dragged instance only when the pointer moves. It
  sets the position to the pointer minus the grab offset. A tick without
  movement writes nothing. A *Set position* on the dragged instance holds
  while the finger rests, but the next move overwrites it. So if the look
  must trail the finger or lift above it, put that look on a child that
  the events position. Drops and overlaps still use the dragged instance.
  [runtime: exported
  c3runtime.js r503, `Behaviors.DragnDrop` `_OnMove`, called from the
  `pointermove` dispatch only; observed in a game project, r503 preview,
  2026-09-29]

- Drag & Drop starts one drag for each press, on the front instance under
  the pointer. That is the instance on the highest layer, and on that
  layer the one highest in Z order. It considers the instances of every
  object type that has the behavior, but only those whose behavior is
  enabled and whose layer is interactive. It ignores the visibility of the
  instance and of its layer. A popup without Drag & Drop takes no part in
  this choice, so the player can still drag the pieces under it. The
  player can also drag a hidden piece or a piece on a hidden layer. To
  stop drags while a popup shows, turn the pieces' layer off with *Set
  layer interactive*, or the behavior with *Set enabled*. [runtime:
  exported c3runtime.js r504, `Behaviors.DragnDrop` `_OnInputDown` skips an
  instance whose behavior is disabled or whose layer fails
  `IsSelfAndParentsInteractive`, then keeps the instance with the highest
  layer index, then the highest Z index; observed in a minimal project, r504
  preview, 2026-10-05: of two overlapping instances on two layers, the upper
  layer's dragged, also with that layer hidden and with that instance
  hidden, and the lower one dragged once the upper layer was not interactive;
  of two on one layer, the higher in Z dragged]
