# Menus steered by keys or a gamepad

If the events steer a menu with keys or a gamepad, with sub-menus and a
way back, read this page. Design the events first with
[design/thinking.md](../design/thinking.md). This page expands that
file's row "A menu steered by keys or a gamepad".

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
