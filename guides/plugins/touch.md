# Event Sheet Pitfalls: Touch

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Touch *On tap* skips a tap released within 666 ms and 25 px of the tap
  before it. That tap fires *On double-tap* instead, and the tap after it
  is single again. So a button on *On tap object* loses every second press
  of a player tapping fast. To count every press, use *On touched object*
  (start), or add *On double-tap object*. A tap is itself a release within
  333 ms and 15 px of the touch start. [manual:
  plugin-reference/touch.md "On tap", "On double-tap"; runtime: exported
  c3runtime.js r503, `ShouldTriggerTap`; observed in a game project, r503
  preview, 2026-09-28: 7 mouse clicks 0.3 s apart on the button made 4
  pieces, 8 clicks 0.7 s apart made 8; on *On touched object* (start), 7
  clicks 0.3 s apart made 7]

- One tap on an object fires Touch *On any touch start* first, then *On
  touched object* (start), then, at the release, *On tap*, whatever the
  order of their events in the sheet. So a restart on *On any touch start*
  runs before an *On touched object* event ends the game, and does not fire
  on that tap. A restart on *On tap*, or on *On touched object* in a later
  event, runs after it and fires. Make that restart test a value that the
  end sets after a *Wait*. [observed in a game project, editor preview,
  2026-10-04: events that each appended a letter to a global gave "SO" for
  one tap on a cell, *On any touch start* and *On touched object* in either
  order, by touch and by mouse, and "SOT" with an *On tap* event added first
  in the sheet]

- The Mouse object reacts only to a pointer whose type is mouse. *Mouse button
  is down*, *On any click*, *On button released*, a single *On click* and
  `Mouse.X`, `Mouse.Y` ignore a finger and a pen. *On movement* is the
  exception and fires for touch too. Touch with *Use mouse input* on fires for
  the mouse and the finger alike and has no expression for the pointer type.
  Drag & Drop takes a left click and a finger without the Touch object. So if
  a drag behaves differently under a finger, such as a piece lifted higher so
  the finger does not hide it, test `Mouse: Mouse button is down (left)`: true
  while a mouse drags, false while a finger does. Test it in an event that
  runs every tick under Drag & Drop *Is dragging*, not under *On drag start*.
  That trigger runs from the same pointer-down dispatch as the Mouse object's
  own handler, and the two run in the order they subscribed in, which nothing
  documents. This test decides per drag, so a touchscreen laptop gets each
  drag right. The input-method triggers of the next entry choose a control
  scheme instead. [runtime: exported c3runtime.js r503,
  `Plugins.Mouse.Instance` `_OnPointerDown`, `_OnPointerMove` and
  `_OnPointerUp` each test `"mouse"===e["pointerType"]` before touching the
  position or the button map, and the movement trigger in `_OnPointerMove`
  runs before that test, while a double click comes from the browser's
  `dblclick` untested; `Plugins.Touch.Instance` `_OnPointerDown` drops only a
  mouse pointer with *Use mouse input* off; `Behaviors.DragnDrop` listens to
  the pointer events itself; manual: plugin-reference/mouse.md "On movement",
  plugin-reference/touch.md "Use mouse input"; schema: plugins/touch.json has
  no pointer-type expression; observed in a game project, r503 preview,
  2026-09-30]

- With *Use mouse input* on, a left click is a touch. *On any touch start*,
  *On touched object* and *On tap* fire for it, so a Touch trigger cannot
  detect a finger. Detect the input method with *Use mouse input* off. Then
  *On any touch start* means a finger or a pen, and Mouse *On any click* or
  Keyboard *On any key pressed* means a desktop. Each sets a global variable
  that decides the controls (see "Native first" in
  [design/thinking.md](../design/thinking.md)). The example
  detecting-input-method decides once, on its title screen. The same triggers
  in a sheet that runs during play follow a change of device. Gamepad *On any
  button pressed* adds a gamepad. With *Use mouse input* off, a mouse fires
  no Touch trigger, so every button the mouse must press needs its own Mouse
  event. A project that clicks its Touch buttons with the mouse keeps the
  setting on and tells a finger drag from a mouse drag with the Mouse test
  above. The global variable follows the last input. Whether it has changed
  when a drag starts on the same press depends on the same undocumented order
  as above. [manual: plugin-reference/touch.md "Use mouse input"; example:
  detecting-input-method, `Title events` events 2 and 3 and the comment of 3,
  Touch object with *Use mouse input* off; schema: plugins/gamepad.json
  `on-any-button-pressed`, a trigger; runtime: exported c3runtime.js r503,
  `Plugins.Touch.Instance._OnPointerDown`]

- Touch *On touched object*, *Is touching object*, *On tap object* and Mouse
  *On object clicked*, *Cursor is over object* find an instance only by its shape
  under the pointer. So the player can press an invisible instance, one with
  collisions disabled and one on an invisible layer. These conditions skip
  only an instance outside the viewport or on a layer that is not interactive.
  A button hidden to switch it off still works. Add *Is visible* to its event,
  or turn its layer off with *Set layer interactive*. Disabled collisions fail
  overlap and collision tests, not these. [runtime: exported c3runtime.js
  r504, those conditions call `TestAndSelectCanvasPointOverlap`, which tests
  the layer's `IsSelfAndParentsInteractive`, `IsInViewport2` and
  `ContainsPoint`; manual: project-primitives/layers.md "Initially
  interactive"; observed in a game project, r504 preview, 2026-10-03: a tap on
  a button ran its *On touched object* event with the button invisible, with
  its collisions disabled and with its layer invisible, and did not with the
  layer not interactive]

- Touch *On touched object*, *On tap object* and Mouse *On object clicked*
  pick every instance under the pointer, not the one in front. So when
  popups, menus or buttons overlap, a click or tap on the front one also
  runs the event for each instance behind it: the press goes through. Add
  the button's own *Pick top/bottom* (top) as a second condition of the
  trigger's event: it keeps the front instance, counting layers first and
  then Z order, so it works across popup layers too. It compares instances of
  one object type, so buttons made of several types go into a family and the
  event uses the family. [manual: plugin-reference/common-features/common-conditions.md
  "Pick top/bottom"; runtime: the `TestAndSelectCanvasPointOverlap` of the
  entry above selects each instance that contains the point]

- A touch's speed, from `Touch.SpeedAt`, `Touch.SpeedForID` or *Compare
  touch speed*, is the distance between the last two pointer moves divided by
  the time between them. Once the finger has been still for about 50 ms, the
  speed reads 0. The release adds no move. So in *On any touch end* the speed
  is that of the last move if the finger lifts while it moves, and 0 if it
  stopped first: a flick test there passes only for a release made in
  motion. [runtime: exported c3runtime.js r504, `Plugins.Touch.TouchInfo`
  `GetSpeed`; `Plugins.Touch.Instance` `_OnTick2` sets a touch's last time
  to the present once it has not moved for 50 ms, which makes the speed 0,
  and `_OnPointerUp` records no position; observed in a minimal project, r504
  preview, 2026-10-05: pointer events dispatched in the page, ten moves
  16 ms apart, read 1829 px/s in *On any touch end* with the release 16 or
  36 ms after the last move, and 0 with the release 56 ms or more after it]

- A tap on the screen, a tap anywhere, is Touch *On any touch start*, which
  fires for a touch wherever it lands. *On touched object* fires only for a
  touch that starts inside the object, so an invisible Sprite laid out as the
  tap area misses every tap outside its box: one built 397 px square in a
  corner of a 720×1280 layout counted the taps in that corner and none in
  the middle. Use *On any touch start* with no object, and `Touch.X` and
  `Touch.Y` where the rule reads where the tap landed. [manual:
  plugin-reference/touch.md "On any touch start", "On touched object";
  observed in a generated project, editor preview, 2026-10-09]

- A popup closed by a tap on its dim, Touch *On touched object* with the
  dim, closes only where the dim reaches. Under *Scale outer* the viewport
  grows with the window's aspect ratio, so a dim sized to the design area
  leaves strips at the sides of a wide window or above and below a tall one.
  There the game shows through and a tap closes nothing. Size a full-screen
  cover far past any aspect ratio, such as 8000×8000 around the centre of
  the design area. A Sprite does this without a layer of its own texture,
  which a layer background faded by layer opacity needs. Test the tap
  against the panel instead of the cover: *On any touch start* and *NOT Is
  touching object* for the panel and for each of its buttons, in a group
  that is active only while the popup is open. Then the cover only draws,
  and its size decides nothing about input. [manual:
  system-reference/system-expressions.md "OriginalViewportWidth", the
  viewport size that *Scale outer* changes with the screen;
  interface/debugger/gpu-profile-tab.md, the cost of a layer's own
  texture; observed in a game project, r504 preview, 2026-10-06: popup
  dims 1400×2000 on a 430×932 *Scale outer* design area left both sides of
  a wide window uncovered, and taps there did not close the popup; dims at
  8000×8000 and the touch test above fixed both]
