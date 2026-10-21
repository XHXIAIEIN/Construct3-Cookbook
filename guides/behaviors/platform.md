# Event Sheet Pitfalls: Platform

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A Solid stops a Platform object at its edge, so the two touch and do not
  overlap. *Is overlapping* stays false while the player stands on a Solid
  floor or walks into a Solid wall. So an event that pushes a crate the
  player is against never runs. Test touching with *Is overlapping at
  offset*, 1 pixel towards the Solid. That is (1, 0) for a wall on the
  right and (0, 1) for the floor. The offset moves the object the condition
  belongs to, so a test from the crate's side takes the opposite sign.
  *On collision* still fires, because the behavior registers the collision
  as it pushes the object out. [manual:
  plugin-reference/common-features/common-conditions.md "Is overlapping at
  offset"; observed in a copy of the official example follow-rewind-time,
  stable r495.2 preview, 2026-10-04: a Platform player held against a Solid
  wall on a Solid floor, *Is overlapping* false, at offset (1, 0) and
  (0, 1) true; observed in the platformer template with a Solid door,
  stable r495.2 preview, 2026-10-09: *Is overlapping* the door never held,
  at offset (1, 0) it did; runtime: exported c3runtime.js, Platform calls
  `RegisterCollision` after `PushOutSolidAxis`]

- Platform's *Simulate control* Jump jumps from the floor only, or in the
  air as the one extra jump that *Double jump* allows. Pressed in the air
  with *Double jump* off, it does nothing. A jump from the air, such as a
  coyote-time jump just after walking off a ledge, is *Set vector Y* to
  `-Self.Platform.JumpStrength`. *On jump* does not fire for it, so that
  event also runs what *On jump* would run. [manual:
  behavior-reference/platform.md "Double jump"; observed in a probe
  project, r495.2 preview at 60 and 144 Hz, 2026-10-08: *Simulate control*
  Jump pressed 7 to 208 ms after walking off a ledge never jumped, and
  *Set vector Y* jumped at every press within the 0.1 s window]
