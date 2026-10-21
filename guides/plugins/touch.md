# Event Sheet Pitfalls: Touch

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Touch *On tap* skips a tap that is released within 666 ms and 25 px of
  the previous tap. That tap fires *On double-tap* instead, and the next
  tap counts as a single tap again. So a button on *On tap object* misses
  every second press when the player taps fast. To count every press, use
  *On touched object* (start), or add *On double-tap object*. A tap itself
  is a release within 333 ms and 15 px of the touch start. [manual:
  plugin-reference/touch.md "On tap", "On double-tap"; runtime: exported
  c3runtime.js r503, `ShouldTriggerTap`; observed in a game project, r503
  preview, 2026-09-28: 7 mouse clicks 0.3 s apart on the button made 4
  pieces, 8 clicks 0.7 s apart made 8; on *On touched object* (start), 7
  clicks 0.3 s apart made 7]

- One tap on an object fires three Touch triggers in a fixed order,
  whatever the order of their events in the sheet: *On any touch start*,
  then *On touched object* (start), then *On tap* at the release. So a
  restart on *On any touch start* runs before an *On touched object* event
  ends the game, and it does not fire on that tap. A restart on *On tap*,
  or on *On touched object* in a later event, runs after the end and fires
  on the same tap. To stop this, make the restart test a value that the
  end of the game sets after a *Wait*.
  [observed in a game project, editor preview,
  2026-10-04: events that each appended a letter to a global gave "SO" for
  one tap on a cell, *On any touch start* and *On touched object* in either
  order, by touch and by mouse, and "SOT" with an *On tap* event added first
  in the sheet]

- The Mouse object reacts only to a pointer whose type is mouse. *Mouse button
  is down*, *On any click*, *On button released*, a single *On click* and
  `Mouse.X`, `Mouse.Y` ignore a finger and a pen. *On movement* is the
  exception and fires for touch too. The Touch object with *Use mouse input*
  on fires for the mouse and the finger alike. It has no expression for the
  pointer type. Drag & Drop takes a left click and a finger by itself,
  without the Touch object. So if a drag must behave differently under a
  finger, test `Mouse: Mouse button is down (left)`. An example is a piece
  lifted higher so that the finger does not hide it. The condition is true
  while a mouse drags and false while a finger drags. Test it in an event
  that runs every tick under Drag & Drop *Is dragging*, not under *On drag
  start*. *On drag start* runs from the same pointer-down dispatch as the
  Mouse object's own handler. The two run in the order in which they
  subscribed, and nothing documents this order. The test decides for each
  drag, so on a touchscreen laptop each drag gets the behavior of the
  pointer that makes it. The input-method triggers of the next entry
  choose a control scheme instead. [runtime: exported c3runtime.js r503,
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
  detect a finger. To detect the input method, turn *Use mouse input* off.
  Then *On any touch start* means a finger or a pen, and Mouse *On any
  click* or Keyboard *On any key pressed* means a desktop. Each of these
  triggers sets a global variable that decides the controls (see "Native
  first" in [design/thinking.md](../design/thinking.md)). The example
  detecting-input-method decides once, on its title screen. The same
  triggers in a sheet that runs during play follow a change of device.
  Gamepad *On any button pressed* detects a gamepad too. With *Use mouse
  input* off, a mouse fires no Touch trigger, so every button that the
  mouse must press needs its own Mouse event. If a project clicks its
  Touch buttons with the mouse, keep the setting on. Then tell a finger
  drag from a mouse drag with the Mouse test above. The global variable
  follows the last input. If a drag starts on the same press, whether the
  variable has changed by then depends on the same undocumented order as
  above. [manual: plugin-reference/touch.md "Use mouse input"; example:
  detecting-input-method, `Title events` events 2 and 3 and the comment of 3,
  Touch object with *Use mouse input* off; schema: plugins/gamepad.json
  `on-any-button-pressed`, a trigger; runtime: exported c3runtime.js r503,
  `Plugins.Touch.Instance._OnPointerDown`]

- Touch *On touched object*, *Is touching object*, *On tap object* and Mouse
  *On object clicked*, *Cursor is over object* find an instance only by its
  shape under the pointer. So the player can press an invisible instance,
  one with collisions disabled and one on an invisible layer. These
  conditions skip only an instance outside the viewport or on a layer that
  is not interactive. So a button that is hidden to switch it off still
  works. Add *Is visible* to its event, or turn its layer off with *Set
  layer interactive*. Disabled collisions make an instance fail overlap and
  collision tests, but not these conditions. [runtime: exported c3runtime.js
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
  runs the event for each instance behind it. Add the button's own *Pick
  top/bottom* (top) as a second condition of the trigger's event. It keeps
  the front instance, by layer first and then by Z order, so it works
  across popup layers too. It compares instances of one object type only.
  So if the buttons are of several types, put them in a family and use the
  family in the event. [manual:
  plugin-reference/common-features/common-conditions.md
  "Pick top/bottom"; runtime: the `TestAndSelectCanvasPointOverlap` of the
  entry above selects each instance that contains the point]

- `Touch.SpeedAt`, `Touch.SpeedForID` and *Compare touch speed* read the
  speed of a touch. It is the distance between the last two pointer moves
  divided by the time between them. Once the finger has been still for
  about 50 ms, the speed reads 0. The release adds no move. So in *On any
  touch end*, the speed is that of the last move if the finger lifts while
  it moves. If the finger stopped first, the speed is 0. A flick test in
  that trigger therefore passes only for a release made in motion.
  [runtime: exported c3runtime.js r504, `Plugins.Touch.TouchInfo`
  `GetSpeed`; `Plugins.Touch.Instance` `_OnTick2` sets a touch's last time
  to the present once it has not moved for 50 ms, which makes the speed 0,
  and `_OnPointerUp` records no position; observed in a minimal project, r504
  preview, 2026-10-05: pointer events dispatched in the page, ten moves
  16 ms apart, read 1829 px/s in *On any touch end* with the release 16 or
  36 ms after the last move, and 0 with the release 56 ms or more after it]

- Touch *On any touch start* detects a tap anywhere on the screen, because
  it fires for a touch wherever it lands. *On touched object* fires only
  for a touch that starts inside the object. So an invisible Sprite laid
  out as the tap area misses every tap outside its box. For example, one
  built 397 px square in a corner of a 720×1280 layout counted the taps in
  that corner and none in the middle. Use *On any touch start* with no
  object. If the rule needs the place where the tap landed, read `Touch.X`
  and `Touch.Y`. [manual:
  plugin-reference/touch.md "On any touch start", "On touched object";
  observed in a generated project, editor preview, 2026-10-09]

- A popup that closes on Touch *On touched object* with its dim closes
  only where the dim reaches. Under *Scale outer*, the viewport grows with
  the aspect ratio of the window. So a dim sized to the design area leaves
  strips at the sides of a wide window, or above and below a tall one. In
  these strips the game is visible, and a tap closes nothing. Size a
  full-screen cover far past any aspect ratio, such as 8000×8000 around
  the centre of the design area. A Sprite cover does this without a layer
  that has its own texture. A layer background faded by layer opacity
  needs such a layer. Test the tap against the panel instead of the
  cover. Use *On any touch start* and *NOT Is touching object* for the
  panel and for each of its buttons, in a group that is active only while
  the popup is open. Then the cover only draws, and its size has no effect
  on input. [manual:
  system-reference/system-expressions.md "OriginalViewportWidth", the
  viewport size that *Scale outer* changes with the screen;
  interface/debugger/gpu-profile-tab.md, the cost of a layer's own
  texture; observed in a game project, r504 preview, 2026-10-06: popup
  dims 1400×2000 on a 430×932 *Scale outer* design area left both sides of
  a wide window uncovered, and taps there did not close the popup; dims at
  8000×8000 and the touch test above fixed both]
