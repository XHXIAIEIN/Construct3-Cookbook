# Menus with sub-menus

If the events steer a menu with keys, a gamepad or a pointer, with
sub-menus and a way back, read this page. Design the events first with
[design/thinking.md](../design/thinking.md). This page expands that
file's row "A menu steered by keys, a gamepad or a pointer". A menu whose
rows the pointer opens by hovering also needs "Sub-menus opened by a
pointer". A button or a control with a text on it needs "A label on a
button".

## The selection

- One Array holds the selected item's id per depth. When a sub-menu opens,
  *Push* the new item's id. On back, *Pop* it. `Back` is the current
  selection.
- A second column of the Array holds the name of the function that the
  back event calls at that depth, through a function map. So each sub-menu
  says how it closes, and one back event serves every depth.

## Moving the cursor

- The next item in a direction is the nearest item within a few degrees of
  that direction.
- If no item lies that way, the next item is the farthest item the
  opposite way, so the cursor wraps.
- Read keys and the gamepad through one input object, as
  [pitfalls: Touch](../plugins/touch.md) says. Then a press is
  `confirm > lastConfirm` for both.

## The highlight

Derive the highlight every tick from the selected id, as rule 7 of the
design guide says. One event without conditions gives every item its
default look. The next event picks the item whose id is `Back` and
overrides that look. No input event moves the highlight.

[manual: plugin-reference/array.md "Push", "Pop", "Back";
project-primitives/events/functions.md "Function maps"; a studied project,
2026-10-06]

## A label on a button

Vertical alignment Center centres a Text's em box, not its letters. The
runtime draws each line from its top, one em high. Capitals, digits and
Chinese fill less than the em and sit near its top, so a label centred on a
button by its box looks set high. Short lowercase letters such as "menu"
sit centred.

- Lower a label that holds capitals, digits or Chinese by about 0.11 em: 3
  px at 27 px, 2 px at 16 px. Use one value for every label of one font and
  size, so that "Play" and "Continue" on two buttons stand on one line.
- Shrink the label's box from the top by twice that amount, so the label
  stays inside its button or its control's row. If the box is one line
  high, as the name beside a bar is, move it down by that amount instead,
  because a line taller than its box draws from the box's top.
- A Sprite Font centres its character cell. Lower the label by the
  distance from the centre of a capital to the centre of the cell, in whole
  font pixels times its scale: 1 font pixel for Fusion Pixel 8 px.
- A glyph drawn alone on a shape, such as a play triangle on a disc, is
  centred by its area, not its box. A triangle's centroid lies a third of
  its height up from its base, so raise a triangle that points up by a
  sixth of its height from the centre of its box.

The skill's generator template does this in `button()`, `toggle()` and
the other controls, `labelled_bar()` and the stage band of `band_text()`,
and its `review_look.py` reports a label off its shape's centre as
`optical`.

[runtime: r506.3 `lib/gfx/text.js`; observed in a test project, r506.3
preview at 1280×720 in system-ui and at 640×360 in Fusion Pixel 8 px,
2026-10-30]

## Sub-menus opened by a pointer

A pointer that moves from a row to its sub-menu crosses other rows on a
diagonal. If each row opens its own sub-menu at once, the sub-menu that
the player aims at closes before the pointer reaches it. Delays and a
safe triangle keep it open. The pointer decides only when an id goes
onto or off the selection Array. The highlight still comes from the Array,
so a row that the pointer crosses does not light up.

- **The row under the pointer.** Every tick, pick it with Mouse *Cursor
  is over object* and *Pick top/bottom* (top), because a sub-menu
  overlaps its parent's rows. *Pick top/bottom* compares the instances of
  one object type, so if the rows are of several types, put them in a
  family and use the family. A closed level must fail this test, so add
  *Is visible* or turn its layer off with *Set layer interactive*
  ([pitfalls: Touch](../plugins/touch.md)). Read positions on the menu's
  layer, as `Mouse.X("Menu")`.
- **The pointer's path.** In an *Every tick* event, when the pointer's
  position differs from the stored one, copy the stored position to an
  older pair, then store the current one. The older position is the apex
  of the triangle, so the apex never lies on the pointer. Do not record
  it in *On movement*, because `Mouse.X` and `Mouse.Y` are one pointer
  event behind in that trigger ([pitfalls: Mouse](../plugins/mouse.md)).
- **The safe triangle.** While a sub-menu is open, the triangle joins the
  apex to the two corners of the sub-menu's near edge, the left edge for a
  sub-menu on the right. The pointer (px, py) is inside when
  `(bx - ax) * (py - ay) - (by - ay) * (px - ax)` has one sign for the
  three edges a→b, b→c and c→a. Put the test in a function that returns 1
  or 0. The pointer must also be within the last
  min(90, max(56, 0.43 × the parent's width)) CSS px of the parent, on the
  side of the sub-menu. Convert CSS px as
  [porting-web-effects.md](porting-web-effects.md) "Sizes" says. While
  the pointer is in the triangle, a row that it crosses does not become
  the hovered row. Once the pointer is inside the sub-menu, the triangle
  ends.
- **A finger.** The Mouse object ignores a finger
  ([pitfalls: Touch](../plugins/touch.md)). So a touch takes effect at
  once through Touch *On touched object*, with no delay and no triangle.

Time each delay from a `wallclocktime` stored when the hovered row
changes, and compare it every tick. A menu over a paused game runs at time
scale 0, where `time` stops and a *Wait* with *Use time scale* never ends
([pitfalls: System](../plugins/system.md)).

| Delay | Seconds | Rule |
|-------|---------|------|
| Open | 0.22 | A row hovered this long takes effect. A folder row pushes its id and opens its sub-menu. A plain row pops the deeper levels. Leaving the row first cancels it |
| Safe window | 1.2 | A row hovered inside the triangle takes effect when the pointer leaves the triangle, or this long after the hover began. So a pointer that stops there still opens its row |
| Close | 0.36 | When the pointer is over no level and not over the menu's button, the whole menu closes after this long. Coming back first cancels it. A click outside closes it at once |

[manual: system-reference/system-expressions.md "time", "wallclocktime";
a studied web menu, 2026-10-26, for the triangle and the delays]
