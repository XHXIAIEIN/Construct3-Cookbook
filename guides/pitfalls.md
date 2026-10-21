# Event Sheet Pitfalls

These are runtime facts that general programming intuition gets wrong.
Read them with [design/thinking.md](design/thinking.md) before you write
events. Every entry ends with its source: a manual page under
`Construct3-Manual/`, a schema file, an official example id, a page of the
community cheat sheet at fed-4.gitbook.io/c3-cheat-sheets, or an
observation in a game project with its date. If you edit
`eventSheets/*.json`, `layouts/*.json` or clipboard JSON by hand, read
[project-files/hand-editing.md](project-files/hand-editing.md) first.

Each group lists one conclusion per pitfall. If the events touch what a
group names, open its page for the cases and the sources before you write
the events.

## Topics

### How events work

If the events depend on what the manual's "How events work" page covers, read [primitives/events/how-events-work.md](primitives/events/how-events-work.md).

- A type and its family are picked separately, so a pick that narrows `Piece` never narrows `Pieces`. Refer to the name that the caller narrowed.
- A picking condition reads its type and its container members from each candidate in turn, not from the outer event's pick. So store the outer value in a local before *Pick by evaluate*, and compare with the local.
- Sub-events run after the parent's actions, so their conditions see what those actions changed.
- A destroyed instance still counts in `Count` until the top-level event ends. Test "none left" in a top-level event of its own.
- If a pick finds no instance, it stops its event, and *Pick all* does the same. So `PickedCount = 0` never holds below a pick of that type. Test "none left" with `Count = 0` in an event that does not pick the type.
- A destroyed child still counts as a child until the top-level event ends. Count the children from a later top-level event, or with *Pick children* and `PickedCount`.
- Each condition keeps only the instances that pass it. So `Column = 0` followed by `Column = 1` never holds, and `Value ≠ 0` means any instance, not all. Narrow once, then compare `PickedCount`.
- If you deactivate a group, its events stop, but its behaviors, timers and tweens keep running. So a deactivated group does not pause the game.
- Until the top-level event ends, only UID, *Pick children* and `Count` find a created instance outside its own event. So call a function that acts on the older instances before the creation, or set the created instance's values while it is picked. If nothing runs later, put *Wait 0* before the step.

### Containers

If the events depend on what the manual's "Containers" page covers, read [primitives/objects/containers.md](primitives/objects/containers.md).

- Container members are created, destroyed and picked together. But hierarchy children are not picked with their parent, so pick them with *Pick children*.
- A pick of a family never picks the container of a member type. In a sub-event, pick the type from the family with `Enemy: Pick by unique ID Enemies.UID`. Add one such sub-event per member type.
- In a container, an expression that names another member reads the member of the same instance. If such an expression is a parameter of a custom action, put *For each* before the call. Then each instance passes its own value.
- A Dictionary or JSON in a container gives each instance its own copy. Use it instead of a growing list of instance variables.

### Conditions

If the events depend on what the manual's "Conditions" page covers, read [primitives/events/conditions.md](primitives/events/conditions.md).

- An event, or a branch of sub-events, holds one trigger. A function or a custom action is the trigger of its branch. So a tween's *On finished* goes in a top-level event of its own, which calls the next function. Only an OR block lists several triggers.
- The editor treats *On collision with another object*, Timer *On timer* and the Gamepad button conditions as triggers, and every rule above applies to them. But the runtime tests them in sheet order.
- You cannot invert a trigger, a loop, *Else*, *Trigger once* or a condition that only picks. For "not on collision", invert *Is overlapping*.
- *Trigger once* and *Every X seconds* do nothing useful under a trigger, and the editor does not offer them there.
- An event runs every tick unless a trigger, *Every X seconds* or *Trigger once* is in it or above it. So a variable that it flips with *Toggle* or `3 - x` flips every tick. Flip the variable under the trigger that causes the change, such as a pause flag in *On key pressed*. For a timeout, flip it where the time left is tested, and set the time back there. *Trigger once* flips it once each time the conditions turn true, not once per input.
- Events with the same trigger run in order on one input. So a switch written as two such events ("frame 0: set 1", "frame 1: set 0") sets itself back. Write one event with the trigger, and put the cases in sub-events, with *Else* at the start of the second.
- A trigger can fire with several instances picked, and Timer *On timer* can too. If a *Pick nearest* or a function call expects one instance, add *For each* after the trigger.
- *Else* is decided per block, not per instance. To branch per instance, use a second event with the inverted condition, or set a default and override it.
- *Else* does not narrow the picks. It can follow a normal sub-event inside a trigger block, but not the trigger block itself.

### Functions

If the events depend on what the manual's "Functions" page covers, read [primitives/events/functions.md](primitives/events/functions.md).

- Function locals are out of scope for the function block's own top-level actions.
- A function with a return type is called as the expression `Functions.MyFunction`. Parentheses only carry parameters.
- Without *Copy picked*, a function runs with every object reset to all instances picked.
- With *Copy picked*, type and family picks are copied separately. Put logic that acts on the caller's picks in a custom action.
- A custom action runs once with all of the caller's picks, and a System condition in it reads the first instance. If the action decides per instance, put *For each* first.
- A custom action returns nothing. To hand its result back, set an instance variable of the object in the block, and read it after the call.
- Parameters are bare identifiers in expressions: `OffsetX`, not `Functions.OffsetX`.
- If a parameter and a variable of the function's group differ only in case, the editor renames the later one. If it renames the parameter, the function reads the variable. Give them names that differ by more than case (`launchSpeed` beside `SPEED`).
- If two functions, or two custom actions of one object, have names that differ only in case, the editor renames the second. Then every call runs the first. Give them names that differ by more than case.
- A function without parameters is called without parentheses: `Functions.name`, not `Functions.name()`.
- To replace a call by a string from the deprecated Function plugin, use a function map of built-in functions. Run *Map function to string*, then *Call mapped function* with the string, or `Functions.CallMapped` for a value.
- *Call mapped function* forwards parameters from its index only to a mapped function. The default function gets every parameter from 0. If a call finds nothing to run, it only prints a warning in the console. Give the default function the caller's whole parameter list.

### Event sheet includes

If the events depend on what the manual's "Event sheet includes" page covers, read [primitives/events/includes.md](primitives/events/includes.md).

- A function can be called from any sheet, included or not. But a trigger runs only in a sheet that the layout uses or includes. In any other sheet it does nothing and shows no error. If the function waits on one of the sheet's triggers, include that sheet.

### Event variables

If the events depend on what the manual's "Event variables" page covers, read [primitives/events/variables.md](primitives/events/variables.md).

- In a System condition or action, `Self` has no object, so the editor refuses to open the project.
- A variable or function parameter named like a system expression (`mid`, `left`, `max`, `round`) is read as the expression.
- Variable names ignore case. A local hides a global of the same name inside its scope. If one of two locals with the same name is in the other's scope, the editor renames the later one (`STEP2`). Then every use refers to the other one. Give each variable a name that differs by more than case from the others in its scope.
- A local variable at sub-event level is visible to its siblings, not to the parent's own actions.
- A variable at the root of a sheet is a global. Every sheet reads it, and it keeps its value between layouts. Only a variable in a group or under an event is local. Put a variable meant for one sheet in a group.
- A non-static local resets every tick, so a trigger of a later tick (*On timer*, AJAX *On completed*) reads its initial value. Make it static, or use a global or an instance variable.
- If you set a text into a number variable, the text is parsed. `"12px"` stores 12, and `"abc"` stores NaN, not 0. NaN fails every comparison. Convert the text with `int()` or `float()` first.
- A local's declaration resets the local when the tick reaches it. So a value that an event above the declaration sets is lost below it. A static local keeps the value. Declare a local above the first event that writes it.

### Expressions

If the events depend on what the manual's "Expressions" page covers, read [primitives/events/expressions.md](primitives/events/expressions.md).

- Construct has no null, and a missing value reads as 0. So test *Has key* or the size first.

### Layouts

If the events depend on what the manual's "Layouts" page covers, read [primitives/layouts.md](primitives/layouts.md).

- The origin (0, 0) is the top-left of the layout and Y grows downwards.
- `ViewportLeft` and the other viewport expressions take a layer. `LayoutWidth` and `ViewportWidth(layer)` are different values.

### Object instances

If the events depend on what the manual's "Object instances" page covers, read [primitives/objects/instances.md](primitives/objects/instances.md).

- Angles are clockwise degrees from 0 facing right. Compare them with `anglediff`, not with `<`.
- A sprite is drawn facing right at angle 0. Paint art facing right.
- The origin is image point 0, at the centre by default, so a sprite at the layout's edge shows only half.

### Layers

If the events depend on what the manual's "Layers" page covers, read [primitives/layers.md](primitives/layers.md).

- The *On tap object* events of one tap run in order, and each one tests the layer when it runs. So if a close event makes the layer under the popup interactive again, the *On tap object* of a button under the popup fires on the same tap. Give the close and the buttons one trigger, and put *Wait 0* before *Set layer interactive*.
- A blend mode changes only the pixels under the object's own quad, and the layer needs *Force own texture*.
- An instance listed earlier on a layer is drawn under the instances listed after it. So a dragged piece listed before its target vanishes behind the target when dropped. List the piece after the target, or run *Move to top* in *On drag start*.
- A global layer shares its content between layouts, but not its state. Each layout starts it with the visibility and interactivity of its properties, and with its instances as placed. Under *On start of layout*, set the layer's state from global variables.

### Templates

If the events depend on what the manual's "Templates" page covers, read [primitives/objects/templates.md](primitives/objects/templates.md).

- If a part is in both the parent's container and its template hierarchy, it is created once. Put it in both, so that it is picked with the parent and follows it.
- An instance created at runtime copies an existing instance or template. Without one, its behavior properties read 0. Keep one instance per object in a layout that never runs.

### Data & storage plugins

If you choose between the data & storage plugins for one goal, read [plugin-category/data-and-storage.md](plugin-category/data-and-storage.md).

- Android and iOS exports have no File System. Save with Local Storage and hand files over with Share.

### Input plugins

If you choose between the input plugins for one goal, read [plugin-category/input.md](plugin-category/input.md).

- Keyboard and Gamepad are separate conditions. Write both into one input object, which holds a value per control and its copy from the last tick. Read a press as `confirm > lastConfirm`.

### Movements behaviors

If you choose between the movements behaviors for one goal, read [behavior-category/movements.md](behavior-category/movements.md).

- 8 Direction cannot move toward a target or steer around walls. On open ground, chase with Move To, and repeat *Move to object*, because it reads the target's position once. Around walls, use Pathfinding: run *Find path* about every second, and *Move along path* in *On path found*.
- *Simulate control* acts only in the tick in which it runs. Put it in an event whose condition stays true while the control is held, such as *Key is down*, not *On key pressed*.
- Every instance with *Default controls* on moves with the arrow keys. Turn it off on each instance that the player does not steer, such as a pushed crate. Move that instance with *Simulate control*.

### System

If the events use a System condition, action or expression, read [plugins/system.md](plugins/system.md).

- *Wait* does not stop a loop, so the remaining iterations run in the same tick.
- A *Wait* keeps the instances that its event picked. So *Wait 2 seconds* then *Destroy* destroys the instance that started the wait, without a stored UID.
- *Wait for previous actions* waits only for asynchronous actions. It waits for the *Wait* actions in a function only if the function is marked *Asynchronous*. The mark changes nothing inside the function.
- A *Wait* delays only the rest of its own block and its sub-events. Sibling events run at once.
- A *Wait* with *Use time scale* on never ends while the time scale is 0.
- *Wait 0* resumes at the start of the next tick, not at the end of the event or sheet. Use it only if a trigger fires before the tick applies what the trigger reports, or if no later event or trigger can pick what a trigger created.
- *Set time scale* 0 stops animations too. To keep one animation playing through a pause (an ultimate, a cutscene), run *Set object time scale* 1 on its object. Restore both time scales in the Sprite's *On finished*.
- For a hit stop, run *Set time scale* 0.1, then *Wait*, then *Set time scale* 1. For a smooth ramp, use a value tween.
- If two *Wait* hit stops overlap, the shorter one ends both. Count the hit stops in progress, and restore the time scale when the count returns to 0. Do not restore it at a `wallclocktime` deadline, because that runs on another clock and leaves the game slowed.
- A hit stop slows tweens and `dt` too. If a tween must end on an audio beat, set its object's time scale to 1 and restore it in *On finished*. If a blend must keep real time, use `dt / timescale`.
- `lerp(a, b, 0.1)` run each tick depends on the framerate. Write `lerp(a, b, 1 - f^dt)`.
- If the factor comes from the engine, such as a tween's value, `lerp` needs no time of its own.
- `lerp` and `unlerp` do not clamp.
- `%` keeps the sign of the left operand, so `-1 % 5` is `-1`.
- `%` is applied before `*`, so `a * b % c` is `a * (b % c)`. Write `(a * b) % c`.
- *For* counts down when its end is below its start. Before `For 0 to count - 1`, test the count, or test that start ≤ end.
- `tokencount("", ",")` is 1, so a loop over an empty list runs once on an empty token. Test `list ≠ ""` before the loop.
- `anglelerp` toward a moving angle jumps when the moving angle passes the angle opposite the start. Ease an offset from the moving angle instead: `aim + anglelerp(startOffset, restOffset, x)`.
- `rgbEx` clamps each channel at 100, so 0-255 values draw pale or white. Write `HexColor("#RRGGBB")`, or `rgbEx255` for computed channels.
- *Set canvas size* also sets the project's window size, so a 4:3 game inside 16:9 shows more of the layout. Run *Scroll to position* back to the centre, and cover the extra width with bars.
- *Create object* picks the created instance in its type, not in its families. So a family action after it moves every other instance. To reach the created instance through the family, use *Pick last created*.
- *Create object* runs once per event, however many instances are picked.
- With an empty template name, *Create object* copies the first instance of the type in the first layout of the project that holds one. So it never reads a template instance in a later layout. Mark that instance as a template, and name it in *Create object*.
- *Create hierarchy* creates the children on the layer of the created parent, whatever layers the template's children sit on. Move a child to its own layer after the creation.
- If only events create an object, it loads its images at creation and draws nothing until they arrive. So a screen-sized picture shows late. Call *Load object images* for it in *On start of layout*.
- *Restart layout* and *Go to layout* keep every global variable and static local at its current value.

### Common to all objects

If the events use a condition, action or expression that every object has (hierarchy, Z order, colour, mesh), read [plugins/_common.md](plugins/_common.md).

- *Pick children* picks only among the current picks of the child type, and a container can narrow these picks. Pick through a family whose only member is the child type.
- *Pick parent* with *Own* looks only one level up. Use *All* to pick a grandparent, because with *Own* the event picks nothing and shows no error.
- A hierarchy child can be on a different layer from its parent. So a lifted parent can be drawn above everything while its parts stay under an outline.
- `ChildCount`, *Compare child count* and *Has children* count children of every type. To count one type, use *Pick children* and then `PickedCount`.
- *Set mesh point* in *Relative* mode adds to the current position, so a point derived and set every tick accumulates.
- If a mesh is pulled into a trapezoid in X and Y, it bends straight lines at each cell diagonal. It also shows no depth, however many points it has. For a plane at an angle, keep X and Y, and give the near row a Z on a *3D* layer under *Perspective*. A 2x2 mesh draws that plane straight.
- *Set width* stretches a Sprite, repeats a Tiled Background and stretches a 9-patch's middle.
- *Move to top* moves only the instance, and leaves its hierarchy children where they are. Move each part.
- *Set color* multiplies. Draw a tinted part white, and keep highlights on an untinted child.
- The instances of a created hierarchy run *On created* in no fixed order. Initialise the hierarchy in *On hierarchy ready* of its root, which fires after all of them have run *On created*.

### 3D model

If the events use 3D model, read [plugins/model3d.md](plugins/model3d.md).

- A 3D model's *Set progress* does nothing while the clip plays or is paused. In r505, *Play* of the playing clip leaves it where it is, so *Stop* the clip first to restart it. After *Play* switches clips, *Stop* and `stop()` leave the first clip playing. *Play* cuts in one tick unless *Transition duration* (r505) is set. A clip cannot cross into itself, so blended repeats alternate two copies.

### Advanced Random

If the events use Advanced Random, read [plugins/advancedrandom.md](plugins/advancedrandom.md).

- Advanced Random's `Random`, weighted draws and permutation tables share one sequence, and *Update seed* restarts it. Seed each draw from the run's seed, its use and a counter, so one kind of draw does not shift another. `advanced_random.py` replays such a run offline. After a Construct update, run its `--check` before you trust the numbers.
- `random()`, `choose()` and *Pick random instance* ignore the seed while *Replace system random* is off. Write a seeded draw as `floor(AdvancedRandom.Random * n)`, or *Pick nth instance* of `floor(AdvancedRandom.Random * PickedCount)`.

### Array

If the events use Array, read [plugins/arr.md](plugins/arr.md).

- `Array.IndexOf` searches along X only. To find a row, use *For* over `Height` with *Compare at XY* and *Stop loop*. *Stop loop* does not stop *For each element*.

### Audio

If the events use Audio, read [plugins/audio.md](plugins/audio.md).

- With *Use worker* on, scheduled sounds jitter by a message delay. For sample-accurate scheduling, set it to *No*.
- A sound that is not loaded yet plays late. A Music file ignores its scheduled time. Keep beat-locked files in Sounds, and preload them.
- *Preload sounds* skips the Music folder. *Unload audio* stops every instance that still plays the file, so unload a fading track in *On fade ended*.
- In a browser, nothing is heard before the first touch, click or key press. Open on a "tap anywhere to start" screen that goes to the game. Put *Request fullscreen* on that tap. Music on that screen itself starts only at the tap.
- The audio clock starts only at the first release, click or key press. Start music when `CurrentTime` moves, not on a touch.
- The `PlaybackTime` of a scheduled sound is ahead by its scheduling lead. Build a beat grid from `CurrentTime` and integer steps.
- *Set playback rate* changes every instance with the tag. Give each play a one-off tag.
- A sound uses the effect chain of its first tag. An action on `"a b"` acts on each tag.
- *Set effect parameter* cancels a ramp that is still running. So merge overlapping ducks into one release.
- Gain effect values are in dB, and the ramp runs on the linear gain. Compressor parameters stay fixed after the effect is added.
- An exponential ramp to 0 throws an error, also on the dry path of a 100 % mix. Ramp linearly, or keep the value above 0.
- Delay `mix` runs from 0 to 100 and scales only the echoes: first echo = mix × feedback.
- *Fade volume* also acts on instances that are scheduled but not started. So a fade of a one-off tag to -100 dB cancels a play scheduled ahead.
- On resume, every suspended sound restarts at once. Run *Stop all* in *On resumed*, then restart the schedule.
- Stereo pan mixes the channels of a stereo sound, which gives +2.3 dB at ±20. Narrow the pan of loud sounds, and keep them off each other's grid points.
- *Play by name* finds a sound by its folder path, such as `Board/spawn`. Keep sounds that are played by computed names out of folders.
- A sound is heard `OutputLatency` after its scheduled time.

### Browser

If the events use Browser, read [plugins/browser.md](plugins/browser.md).

- Put *Request fullscreen*, *Request permission*, *Request wake lock* and the other requests that need a user input trigger in an *On tap*, *On click* or *On key pressed* event. In any other event the browser refuses them.
- A web export looks for an update only when the page loads.
- An automatic reload in *On update ready* loops while another tab of the game is open. Set the hash to `updated` before *Reload*. If the page starts with that hash, prompt the player instead of a reload.
- The Browser object suppresses the browser's install banner. To offer the installation, run *Request install* after *On install available*.

### Dictionary

If the events use Dictionary, read [plugins/dictionary.md](plugins/dictionary.md).

- Dictionary *Set key* ignores a missing key. Write a missing key with *Add key*.

### Drawing canvas

If the events use Drawing canvas, read [plugins/drawingcanvas.md](plugins/drawingcanvas.md).

- Drawing Canvas *Fill polygon* with *Convex* off draws nothing when two consecutive points coincide. Give consecutive points different positions.

### File system

If the events use File system, read [plugins/filesystem.md](plugins/filesystem.md).

- File System writes only through a picker tag. The known folders exist only in desktop exports.
- No tag names the Construct project folder. Save to `<current-app-data>`.
- In a browser, File System needs desktop Chromium and a user input trigger. A save picker erases the file.

### JSON

If the events use JSON, read [plugins/json.md](plugins/json.md).

- JSON `Type(path)` is `"undefined"` for a missing path, so it can test presence inside an expression.
- JSON reads a dot in a path as a step into a nested key. Escape a dot inside a key as `\.` in the path, or keep dots out of keys. A Dictionary reads keys whole.
- JSON has no merge. To merge data files, run *For each* at `""`, and *Set JSON* `GetAsCompactString(CurrentKey)` per top-level key. Requests that share one AJAX tag each fire *On completed* with their own `LastData`, so count them down.

### Keyboard

If the events use Keyboard, read [plugins/keyboard.md](plugins/keyboard.md).

- W, A, S and D alone do not fit an AZERTY keyboard. Give each direction its arrow key too.

### Mouse

If the events use Mouse, read [plugins/mouse.md](plugins/mouse.md).

- In Mouse *On movement*, `Mouse.X`, `Mouse.Y`, `Touch.X` and `Touch.Y` hold the previous pointer event's position. To follow or aim at the pointer, read it in *Every tick*, or in *Is in touch* for a finger.

### Particles

If the events use Particles, read [plugins/particles.md](plugins/particles.md).

- A Particles object given a Sprite spawns real instances that are not the emitter's children.

### Sprite

If the events use Sprite, read [plugins/sprite.md](plugins/sprite.md).

- An instance with collisions disabled fails every overlap and collision test, in both directions. To take a dragged or tweening instance out of these tests, disable its collisions instead of using an `isMoving` flag.
- Image point 0 is the origin. The first point added is 1, and `ImagePointCount` leaves out the origin.
- *Set animation* to the animation already playing does nothing.
- If frames serve as looks rather than as an animation, set the animation's *Speed* to 0.
- *Set frame* to a frame of another image size resizes the instance and swaps its collision polygon.
- A bar grows from its origin. Put the origin on the edge it grows from.

### Sprite font

If the events use Sprite font, read [plugins/spritefont2.md](plugins/spritefont2.md).

- A Sprite Font draws whole cells and tints its outline with its colour. Draw each glyph at the left of its cell, and make one image per colour. Size the box for the largest scale.
- A Sprite Font's *Character spacing* is in layout pixels, and *Scale* does not scale it. It applies only between characters, and `TextWidth` includes it. Keep it at 0, and put a space character where you want a gap.
- Put a Sprite Font's widths in *Spacing data*, which the Layout View shows. Use *Set character width* for a width that changes at runtime. Give a full-width space its own width.

### Text

If the events use Text, read [plugins/text.md](plugins/text.md).

- A Text object has no *Set color*, and a project that uses it does not open. Colour Text with *Set font color*.
- A Text object draws only the lines that fit its height. Size the box for the longest text.
- If a single line is taller than its Text box, it draws with the bottom of its glyphs cut off.
- A change of a Text's font size redraws and re-uploads its texture. Animate position, angle or opacity instead, or use a Sprite Font and tween its scale.

### Tiled Background

If the events use Tiled Background, read [plugins/tiledbg.md](plugins/tiledbg.md).

- The image scale of a Tiled Background or a 9-patch is a percentage in events and a fraction in the layout file. So multiply the fraction by 100. A growing Y offset moves the image down, so scroll upward with a falling offset. A 9-patch pops as one piece only if its image scale changes with its size.

### Timeline controller

If the events use Timeline controller, read [plugins/timeline.md](plugins/timeline.md).

- A relative track adds each tick's step, counted from 0. So keyframe values are offsets from the pose at the start of play. Moves that start and end at 0 can be layered and repeated, and they leave no offset.
- An angle keyframe turns in the direction that its setting gives, even the long way round if the values disagree. Set the direction to the sign of the change to the next keyframe.
- *Set instance* applies only to the next *Play*. One *Play* starts a copy per picked instance, all with the same tags. Set one instance at a time, and tag each copy with its UID.
- A copy is found by the timeline's name inside the copy's name. So make sure that no timeline name contains another.
- *Stop* rewinds to 0 and reverts a relative track's offsets, while *Pause* holds. A finished timeline ignores both *Stop* and *Resume*, and it keeps its offsets. Run *Set time* 0 before you replay it or put the instance back.
- *Set time* pauses and never fires *On keyframe reached*.
- *On keyframe reached* picks nothing. Pick the instance again from the UID in `Timeline.TimelineTags`.
- *On keyframe reached* sees the previous tick's pose. So put *Wait 0* before you read where the keyframe put the instance.
- A negative playback rate rewinds to 0 and finishes there. Set it positive again before the next *Resume*.
- A timeline stopped at its end ignores *Resume* at any rate. Run *Set time* to just before the end, then rewind.
- In the tick in which a copy starts, it reads `Time` 0 while *Is playing* is true. To know that a move is in progress, test *Is playing*.
- If you rewind a copy that reads `Time` 0, it starts backwards from its end, and a relative track ends off by its end pose. Rewind only when `Time > 0`; otherwise run *Set time* 0.
- A negative playback rate fires *On keyframe reached* again for each keyframe it passes on the way back. Set a flag for the rewind, and test the flag in the keyframe event.
- With *Use system timescale* on, the default, a hit stop slows the timeline too.

### Touch

If the events use Touch, read [plugins/touch.md](plugins/touch.md).

- Touch *On tap* skips a tap within 666 ms and 25 px of the tap before it. That second tap fires *On double-tap* instead. If a button counts every press, use *On touched object* (start).
- One tap fires *On any touch start* and *On touched object*, then *On tap* at the release, whatever the order in the sheet. So a restart on *On tap*, or on *On touched object* in a later event, fires on the tap that ends the game. Make the restart test a value that the end of the game sets after a *Wait*.
- Mouse ignores fingers. To tell a finger drag from a mouse drag, test *Mouse button is down* each tick, not in *On drag start*.
- If *Use mouse input* is on, Touch fires for clicks too. To detect the input method, turn it off.
- Touch and Mouse press an object that is invisible or has collisions disabled. Add *Is visible* to the event, or make the object's layer not interactive.
- Touch and Mouse pick every instance under the pointer. Add the button's *Pick top/bottom* (top) to the trigger's event. For buttons of several types, pick through a family.
- Touch speed reads 0 after about 50 ms without a move. So a flick tested in *On any touch end* passes only for a release made in motion.
- A tap anywhere on the screen is *On any touch start* with no object. An invisible Sprite used as the tap area misses taps outside its box.
- Under *Scale outer*, a dim sized to the design area leaves strips where a tap misses it. Size the dim 8000×8000. Close the popup on *On any touch start* with *NOT Is touching* the panel and its buttons.

### Anchor

If the events use Anchor, read [behaviors/anchor.md](behaviors/anchor.md).

- *Scale outer* keeps a parallax-0 HUD centred on the design area. Pin a HUD to a screen edge with Anchor, and stretch a backdrop to the screen with Anchor's left and right edges. In a one-screen layout, turn on *Unbounded scrolling* so the game stays centred too.

### Bullet

If the events use Bullet, read [behaviors/bullet.md](behaviors/bullet.md).

- Bullet *Bounce off object* moves the ball out of the object at once. So an *On collision* with that object in a later event of the same tick does not run. Put the feedback events above the event that bounces.
- A Bullet's angle of motion and the object's angle are two separate values. At speed 0, *Set angle of motion* does nothing, and *Set speed* from 0 moves the object right. Set the speed first, then the angle of motion.
- A fired bullet that misses flies on outside the layout forever, because its hit events destroy only the bullets that hit. Give it the Destroy outside behavior.

### Drag & Drop

If the events use Drag & Drop, read [behaviors/dragndrop.md](behaviors/dragndrop.md).

- The slot where a dragged or tweening instance will land reads empty until the instance lands. So make an event that fills empty slots on its own wait for that instance.
- Drag & Drop moves the instance only when the pointer moves. So put a trailing or lifted look on a child.
- Drag & Drop drags the front instance under the pointer, by layer and then by Z, visible or not. To stop drags under a popup, use *Set layer interactive* on the pieces' layer, or the behavior's *Set enabled*.

### Follow

If the events use Follow, read [behaviors/follow.md](behaviors/follow.md).

- Follow replays the target's path after a delay. Use it for a trailing companion, not a chasing enemy.

### Platform

If the events use Platform, read [behaviors/platform.md](behaviors/platform.md).

- A Solid stops a Platform object at its edge, so *Is overlapping* stays false. To test touching, use *Is overlapping at offset* with 1 pixel towards the Solid. *On collision* still fires.
- With *Double jump* off, Platform's *Simulate control* Jump does nothing in the air. To jump from the air, as in coyote time, use *Set vector Y* to `-Self.Platform.JumpStrength`. *On jump* does not fire then, so run its actions in the same place.

### Scroll To

If the events use Scroll To, read [behaviors/scrollto.md](behaviors/scrollto.md).

- Scroll To *Shake* replaces the running shake, and the object's time scale scales it. Call it only if the new magnitude is at least the remaining one. To shake through a hit stop, set the camera object's time scale to 1.

### Solid

If the events use Solid, read [behaviors/solid.md](behaviors/solid.md).

- A Solid blocks while its behavior is enabled, so a door that only plays an open animation keeps blocking. When the door opens, disable its Solid with *Set enabled*, or destroy the door.

### Tile movement

If the events use Tile movement, read [behaviors/tilemovement.md](behaviors/tilemovement.md).

- Tile movement's *Set grid position* takes a column and a row, not pixels. Convert a position with `round((X - offset X) / grid width)`.

### Timer

If the events use Timer, read [behaviors/timer.md](behaviors/timer.md).

- *Start timer* on an existing tag restarts that timer. After *Stop*, or after the tick in which a *Once* timer fires, the timer's expressions return 0.
- For a reset N seconds after the last input (a combo, an idle screen), use a *Once* timer. Run *Start timer* for N in the input's trigger on every input, and reset in *On timer*. If only its own *On timer* restarts a tick timer under a condition, the timer stops permanently.
- A timer is state that you start and stop. So before you choose a timer, list every transition.
- A timer and a tween scheduled to end together end a tick apart.
- A *Once* timer still counts as running for the rest of the tick in which its *On timer* fires. If an event below branches on *Is timer running* for that tag, put *Stop timer* first in the *On timer*.
- Timer tags cannot time stacked buffs of one kind on one instance. No expression names the tag that fired, and a re-cast restarts the tag. Make each shield or buff a child instance of its holder, with its own Timer and amount. Spend them with *Pick children* and *For each (ordered)* by the time left.

### Turret

If the events use Turret, read [behaviors/turret.md](behaviors/turret.md).

- Turret *Add object to target* adds the whole type or family, whatever is picked. To target only some instances, run *Acquire target* on one picked instance instead.

### Tween

If the events use Tween, read [behaviors/tween.md](behaviors/tween.md).

- A value tween read under *Is playing* drives what Tween has no property for, including a full 360° turn.
- *On finished* runs before *Destroy on complete* destroys the instance, and *On any finished* runs for that tween too.
- A tween started on a property stops the tweens already on it, so those never finish or destroy their instance. Destroy a dying instance with a Timer, not with its death tween.
- If a value tween starts under a tag that already plays, it runs beside the first one, and `Value(tag)` reads the first one. *Stop* the tag before you start it again.
- `Tween.Value(tag)` reads 0 once the tween ends. Animate a channel as the amount left of it, from the full amount to 0.
- A property tween adds its change each tick. If a *Set* changes that property while the tween plays, the value stays, and the rest of the tween adds to it. Guard the *Set* with *NOT Is playing*.
- *Stop* releases a tween at the end of the tick. `Value(tag)` reads the stopped value until then.
- A width tween can end slightly short of its target. Then `Width < target` restarts a tween of no distance, which blocks a real tween for 0.3 s. Start the tween on `Width < target - 0.5`. Set the width to `target` on `Width < target` and `NOT Is playing`. Write the same two events with `>` for a trail.

## Adding an entry

A pitfall is a runtime behaviour of events that changes which events an
agent writes: without the line, the agent writes the events wrong. If a
lesson does not change the events, put it here instead:

- How a project file is written: [project-files/hand-editing.md](project-files/hand-editing.md).
  If a script can test the rule, make it a rule of the
  `construct3-agent-plugin` skill's checker.
- What the editor, the preview or a script that drives them does: the
  `construct3-agent-plugin` skill's references, such as [editor-and-preview.md](https://github.com/XHXIAIEIN/Construct3-Agent-Skills/blob/main/plugin/skills/construct3-agent-plugin/references/editor-and-preview.md).
- How to check a change by playing it, with its cases, its scene and what
  to read: [verifying-a-change.md](https://github.com/XHXIAIEIN/Construct3-Agent-Skills/blob/main/plugin/skills/construct3-agent-plugin/references/verifying-a-change.md).
- How the game looks, its art and its colours: [project-files/new-project.md](project-files/new-project.md),
  or the look documents that the `AGENTS.md` of Construct3-Agent-Skills
  lists.

An entry states a fact, its consequence and its source. Manual wording
outranks an observation, and an observation outranks intuition. Intuition
alone is not an entry.

Put the entry on the one page that owns it, by the rules in "Where an
entry goes" of the repository's `AGENTS.md`. Then add its conclusion as one
line to the page's group here, at the same position as the entry on the
page. A conclusion keeps the fix, not only the prohibition. If the page
does not exist, create it with the name that `AGENTS.md` gives it, and add
a group here that says when to read it. Link the entry from the other
pages that it concerns.
