# Event Sheet Pitfalls: Mouse

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Mouse *On movement* runs before the Mouse object stores the pointer's new
  position. Inside it, `Mouse.X` and `Mouse.Y` hold the position of the
  previous pointer event, so an object moved there stays one pointer event
  behind. A mouse moved by hand sends a pointer event every few pixels, so
  the object stops a few pixels short when the mouse stops. A pointer that
  jumps in one event, as in a scripted test, leaves the object at the start
  of the jump until the next event. While a finger moves, `Touch.X` and
  `Touch.Y` in this trigger are one pointer event behind too. To follow or
  aim at the pointer, set the position or angle in an *Every tick* event
  that reads `Mouse.X` and `Mouse.Y`. For a finger, use an event with *Is in
  touch* that reads `Touch.X` and `Touch.Y`. `Mouse.MovementX` and
  `Mouse.MovementY` in the trigger hold the amount of the current move.
  [runtime: r495.2
  preview, `Plugins.Mouse.Instance._OnPointerMove` calls the private method
  that triggers `OnMovement` before it sets `_mouseXcanvas` and
  `_mouseYcanvas`; manual: plugin-reference/mouse.md "On movement",
  "MovementX"; observed in a minimal project, r495.2 and r504 previews,
  2026-10-14, the runtime in the worker and in the page, input sent through
  the Chrome DevTools Protocol: after mouse moves without a button to
  (720, 384), (600, 300) and (720, 384), a sprite moved in *On movement*
  stood at (0, 0), (720, 384) and (600, 300), and one moved every tick at
  each new position; a touch drag ending at (800, 400) left a sprite moved
  from `Touch.X` in *On movement* at (783, 392), the previous pointer
  event, and one moved under *Is in touch* at (800, 400); with a mouse
  moved by hand in a headed r495.2 preview, the *On movement* sprite
  stopped 3 px short of the every-tick one]
