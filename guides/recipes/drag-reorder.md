# Reordering a row by dragging

If the player reorders a row of items by dragging them, such as a hotbar,
an inventory row or a hand of cards, read this page. Design the events
first with [design/thinking.md](../design/thinking.md). For the drag
itself, read [pitfalls: Drag & Drop](../behaviors/dragndrop.md).

The sources of this page are a probe project played in the r506.3
preview at 144 Hz and at 60 Hz on 2026-10-30. The row had 6 items 96 px
apart. Each number below is the probe's value at both rates, unless a
rate is named.

## Objects and state

- Each visible Item is in a container with an invisible Grip that has
  Drag & Drop. Drag & Drop writes the Grip's position only while the
  pointer moves, so the events position the Item, and the drop events
  read the Grip.
- Each Item holds its logical `Slot`, its `Home` (the X of its slot) and
  an `Offset` with its velocity. Every tick, the Item's X is
  `Home + Offset`. The drop changes only `Slot`. So no event moves an Item
  to its new place, and every change of place is one motion.
- When `Home` changes, add the old `Home` minus the new `Home` to
  `Offset`, then set `Home`. The Item stays where it is and springs to its
  new place. This one rule moves the row when it closes up at the lift
  and when it settles at the drop.
- Globals hold the dragged item's slot `DragSlot`, the `Gap` where it
  will land and `GapTime`, the `time` at which `Gap` last changed. Both
  slots are -1 while nothing is dragged.

## The events, every tick

1. Cursor. If a Grip *Is dragging*, *Set cursor style* Grabbing. Else, if
   *Cursor is over object* Grip, Pointer. Else, Normal. *Cursor is over
   object* works on the invisible Grip.
2. Gap. Under *Is dragging*, compute the gap from the Grip:
   `abs(Grip.Y - RowY) > Band ? DragSlot : clamp(round((Grip.X - X0) / Pitch), 0, Last)`.
   If it differs from `Gap`, set `Gap` and set `GapTime` to `time`. A drop
   outside the row's band then leaves the order as it was.
3. Each other Item takes its rank among the items that are not dragged,
   `R = Slot < DragSlot ? Slot : Slot - 1`, and its distance from the gap,
   `N = DragSlot < 0 ? 0 : (R < Gap ? Gap - 1 - R : R - Gap)`. `N` must be
   0 while nothing is dragged, so that the drop moves all items at once.
   In the probe, a formula without that case gave the last item an `N` of
   5 at the drop, and it waited 120 ms before it moved.
4. Ripple. The items lean away from the gap by `A × 0.7 ^ N`, to the
   left before the gap and to the right after it, and by 0 when the gap
   is the dragged item's own slot. A was 10 px in the probe. Each Item
   takes its new target only once `time - GapTime >= 0.024 × N`, so the
   nearer items move first.
5. Spring. Step each Item's `Offset` toward its target on the implicit
   spring of [feel.md](feel.md), the row "A dragged thing that lags":
   `Vel = (Vel + dt × K × (Target - Offset)) / (1 + C × dt + K × dt²)`,
   then `Offset = Offset + Vel × dt`. K 455 and C 32 give a damping ratio
   of 0.75.
6. The dragged Item: `Offset = Grip.X - Home`, velocity 0, and a second
   spring on its Y toward 16 px above the row. It keeps that place while
   the pointer rests.

## The line, the drop and the cancel

- The insertion line is a Sprite with its origin at its centre. When it
  appears, *Set height* 0, then *Tween (one property)* its height in
  0.15 s with `easeoutcubic`, so it grows from its middle. When the gap
  moves, tween its X in 0.12 s. Hide it while the gap is the dragged
  item's own slot. Run these under the gap's change, not every tick.
- Drop: in the Grip's *On drop*, if `Gap ≠ DragSlot`, *Pick all* Item
  and set each `Slot`: the dragged item takes `Gap`, an item with `R <
  Gap` takes `R`, and the others take `R + 1`. Then set `DragSlot` and
  `Gap` to -1. The springs move every Item to its new slot.
- Cancel: *On key pressed* Escape with *Is dragging*: set `Gap` to
  `DragSlot`, then Drag & Drop *Drop*. *Drop* fires *On drop*, which then
  changes no slot, and the items spring back.

## Measured

| | 144 Hz | 60 Hz |
|---|--------|-------|
| Offsets reached, N = 0 to 3 | 10, 7, 4.9, 3.43 px | the same |
| First move of N = 1, 2, 3 after the gap changes, for 24, 48, 72 ms | 28, 49, 76 ms | 33, 50, 83 ms |
| Overshoot of the spring | 2.0 % | 1.4 % |
| Time to stay within 2 % of a 10 px step | 243 ms | 167 ms |

The delays become whole ticks. At 60 Hz the starts are 33, 17 and 33 ms
apart, but no two items start on the same tick. The implicit step damps
more at the lower rate, so the spring settles sooner at 60 Hz.

When the pointer swept the gap across 4 slots in 90 ms, only the items
next to the line took the passing targets. The others waited for the
last gap and then moved in order. Every item ended on its target. A
*Wait* per item does not do this, because a *Wait* that the next gap
change makes stale still runs ([pitfalls: System](../plugins/system.md)).
