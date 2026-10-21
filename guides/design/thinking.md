# Construct 3 Event Sheet — Design Guide

Use this guide to decide which events a sheet needs before you write
them. [pitfalls/README.md](../pitfalls.md) lists, one line each,
the runtime facts that intuition gets wrong. For each group that the
events touch, it names the topic file under `pitfalls/` to open.
Before the events go into a project or a generator, read
[design/style.md](style.md). It says how the official
examples organise, name and comment a sheet, and which habits the checker
warns on.

A sheet is a program transcribed into events if it:

- links objects through UID variables
- resets picking with `Pick all`, then picks again from a stored link
- copies picked results into variables and branches on the numbers
- rebuilds a timer, a tween or a lookup table out of variables and
  `Every tick`

Such a sheet works, but an experienced Construct user rejects it.

## The model

Events filter instances. Each condition narrows the picked instances, and
the actions run on the instances that are left. If no condition names an
object, all its instances stay picked. When a trigger fires, the
instances involved in it are already picked. A sub-event and its sibling
sub-events all start from the instances that their parent event picked.
Top-level events start from all instances. Spatial relations
(`Is overlapping another object`, `Pick overlapping point`,
`Pick nearest/furthest`) are conditions, so they pick too.
[manual: project-primitives/events/how-events-work.md,
project-primitives/events/sub-events.md,
plugin-reference/common-features/common-conditions.md]

Manual paths are relative to the `Construct3-Manual/` directory inside the
`Construct3-Manual` clone, next to this repository. Read the clone, because
construct.net rejects fetches from an agent. The live page has the same
path without `.md`, appended to
`https://www.construct.net/en/make-games/manuals/construct-3/`.

## Rules

1. **Test a relation with a condition.** "Is this slot taken?" is
   `Slot: Is overlapping Piece`. "Which slot did it land on?" is
   `Pick Slot overlapping point (Piece.X, Piece.Y)`. "Belongs to" is a
   container, a hierarchy or a family. Add an instance variable only if no
   condition can answer the question.
2. **Read the state that the engine already keeps.** Position, overlap,
   dragging, tween progress, animation name and frame, parent and child all
   have conditions and expressions. So does the number of instances:
   `Brick.Count`, and `PickedCount` for the instances a pick kept. A
   destroyed instance still counts until the top-level event ends
   ([pitfalls: How events work](../primitives/events/how-events-work.md)). A variable that copies one of
   these (`occupied`, `isDragging`, `bricksLeft`) stops matching the engine
   as soon as instances move or are destroyed, because every event that
   must update it can forget to. Store only the values that nothing else
   can answer (level, score, where a drag started), on the
   instance that they describe. If events on a family read such a value,
   declare it on the family.

   A decision that an animation plays out is such a value. While the units
   of a pour drain and fill, the engine's state still describes each tube
   as it was before the pour. So a check that reads this state can seal the
   tube that the pour is about to empty. Record the decision when the
   events make it, then let the animation follow.
3. **Use the trigger's pick.** Inside `On drop`, `Piece` is the dropped
   piece. Narrow the pick with sub-events instead of copying its UID into
   a variable and picking it again.
4. **Use a family for a second instance of the same type.** The dropped
   `Piece` and the `Pieces` already on the slot are two independent picks
   in one event. So the event can compare `Pieces.level = Piece.level`,
   then run `Piece: Destroy`.
5. **Disable collisions instead of setting a flag.** In `On drag start`,
   run `Set collisions disabled`. When the instance settles (Tween
   `On any finished`), enable its collisions again. Every overlap test then
   ignores the dragged instance: its old slot tests as empty, and a drop
   back on that slot takes the empty-slot branch. In the same way, if a
   Solid must stop blocking, such as a door that opens, set its Solid
   *Set enabled* to off. If only its animation changes, it keeps blocking.
6. **Shape an interaction as a trigger, narrowing sub-events and Else.**
   Each branch reads as a sentence: on drop; over a slot; slot holds a
   piece; same level: merge. Else: swap. Else: move in. Else: go back.
   Do not collect values into variables first and then branch on the
   numbers. A branch holds one trigger, and a function counts as one
   trigger. So if a function starts a tween, put the tween's *On finished*
   in a top-level event of its own
   ([pitfalls: Conditions](../primitives/events/conditions.md)).
7. **Derive appearance every tick.** One event without conditions sets the
   default look. The next event picks the exceptions and overrides the
   default, so no event needs to reset the look.
8. **Choose a UID, `Pick all` or a global last.** Use a UID or a global
   for a singleton and for a reference that crosses events (an inventory
   array of UIDs, a persisted selection). Use `Pick all` when the events
   after it need the rest of a type and not the trigger's instance. For
   example, relic-hunter stops every ghost when one ghost touches the
   player. If the events read both, as a merge does when it compares two
   levels, use a family for the second instance (rule 4). Inside one
   interaction, `Pick all` followed by a pick from a stored link means that
   the events discarded a pick and rebuilt it by hand. The pick from the
   stored link is *Pick by unique ID*, or *Pick by comparison* on a
   variable that holds a UID or a slot number.

## Native first

Before you add a variable, an `Every tick` or a formula, find the built-in
that already does the job. A draft that rebuilds one of the built-ins below
by hand is a program transcribed into events, even if it has none of the
picking problems in the smell table.

| Need | Use | Not |
|------|-----|-----|
| A delay, a countdown, a cooldown | Timer behavior: *Start timer*, *On timer*, `Duration(tag) - CurrentTime(tag)` | An instance variable decremented by `dt` and compared every tick |
| A fixed-duration move, scale, fade, colour change: known start, known end, known time | Tween behavior: *Tween (one/two/three properties)*, *On any finished* | A progress variable stepped by `dt`, passed to `lerp` and checked for 1 |
| A fixed-duration change of something Tween has no property for: an effect parameter, a behavior property, Z height, a full 360° turn | *Tween (value)*, then *Is playing* with *Set …* to `Self.Tween.Value(tag)` ([pitfalls: Tween](../behaviors/tween.md)) | The same progress variable, or a one-property angle tween set to a full turn |
| Smooth follow of a target that keeps moving: camera, cursor, aim angle | `lerp(a, b, 1 - f^dt)` (`anglelerp` for angles) in `Every tick`; it reads the target again each tick and never finishes | A Tween restarted every tick; `lerp(a, b, 0.1)` with a constant factor, which is framerate-dependent |
| A value derived from another live value: colour from health, zoom from speed, a slider position | `lerp(lo, hi, t)` with `t` from `unlerp`, a ratio, `Tween.Value(tag)` or a timeline; no duration of its own | A variable holding the mapped value, updated from several events |
| Continuous motion toward a target or along a heading | MoveTo, Bullet, Pathfinding, Platform, 8 Direction | `Set X`/`Set Y` from your own velocity variables |
| A part that moves with a body: the graphics on a collision box, a shadow, a held item | Hierarchy: *Add child* once, when the body is created; the child then follows it | An every-tick *Set position* to the body's X and Y |
| Repeating or periodic movement, flashing, fading out | Sine, Flash, Rotate; a fade is a Tween on Opacity | Hand-written oscillation; the Fade behavior, superseded |
| Level data, loot tables, stat curves, any lookup table | Array or Dictionary project file (Project Bar: *New - Array / Dictionary*), loaded in *On start of layout*: AJAX *Request project file*, *Wait for previous actions*, then *Load* from `AJAX.LastData`, all in that one block, because a *Wait* delays only its own block (cell-linking loads its level this way). An AJAX *On completed* is a trigger, so it cannot be a sub-event of *On start of layout*. Nested or hand-written data through the JSON plugin | Per-level instance variables, `level1Hp`, chained conditions or nested ternaries that encode the table in expressions |
| A list that changes at runtime: a deck and its discard pile, a queue, an inventory, a playlist | One Array per list, width 0 at start: *Push* to add, *Shuffle*, `Front`, `Back` or `At(i)` to read, then *Pop* or *Delete* to remove (they return nothing, so read first), *Contains value* to test membership, `Width` to count (place-stickers `InventoryArray`, airborne-explorer `ArrBGM`). Load definitions with several fields from a project file (row above) | A separated string read with `tokenat` (smell table) |
| Things each instance holds, each with its own numbers and its own time: stacked shields, buffs, status effects | One instance per item, a child of its holder (*Add child*, destroy with parent on), with its own variables and a Timer that destroys it when it runs out. The holder reads them with *Pick children* and takes them in order with *For each (ordered)* by the time left ([pitfalls: Timer](../behaviors/timer.md)) | An Array in the holder's container, which an event that picks through a family does not pick ([pitfalls: How events work](../primitives/events/how-events-work.md)); expiry times kept in cells and swept by a loop |
| What a move, an effect or an attack does: its kind and its numbers | One field per fact, a `kind` text and `amount` and `times` numbers, as instance variables or fields of a project file (row above); the branch is an exact comparison, `kind = "block"`, one sibling event or `Else` per kind (alien-battle: under the boss's *On Timer*, `AnimationState = 0`, `= 1`, `= 2`, one attack each) | A code such as `"A6x2"` parsed with `mid`, `tokenat` or `right` and dispatched with `find` (smell table) |
| A sequence scripted in data: an attack pattern, a cutscene, a line of dialogue with its pauses and colours | A cue list in a project file, rows of `delay, cue, params`, parsed once with CSV *Parse CSV* into an Array and drained by a clock; dialogue through Text or Sprite Font *Typewriter text* when nothing moves per glyph ([recipes/scripted-sequences.md](../recipes/scripted-sequences.md)) | A *While* that reads the string with `mid` every tick; a chain of *Wait* actions, one per cue |
| A menu steered by keys or a gamepad, with sub-menus and a way back | An Array of the selected id per depth (*Push*, *Pop*, `Back`), a function map for what back calls, and a highlight derived every tick (rule 7). How the cursor moves and wraps: [recipes/menus.md](../recipes/menus.md) | A global per menu depth; a highlight moved in every input event; one event per item and direction |
| A value that depends on a condition | `condition ? ifTrue : ifFalse` (airborne-explorer `endlessMode ? ENDLESS_TIME_LIMIT : ...`, balloon-blower `currAudioSource > 0 ? ... : ...`); `chooseindex(i, a, b, c)` to pick by a number, `choose` at random | `chooseindex(condition, ifFalse, ifTrue)`, the branches in reverse reading order |
| A cycle of states, elements or turns; whether a set holds an item | The state as a number 0 to N - 1: the next is `(n + 1) % N`, the one after `(n + 2) % N` (alien-battle `(AnimationState + 1) % 3`, balloon-blower `(currAudioSource + 1) % UserMedia.AudioSourceCount`), its name from an Array at that index. Membership: Dictionary *Has key* (airborne-explorer `DictCombo: Has key "Boss"`), Array *Contains value* | Letters looked up through two strings, `mid("FEMAW", find("WFAEM", e), 1)`; `find("," & RELICS & ",", ",rel5,") >= 0` |
| Weighted random, seeded random, noise | Advanced Random: probability tables, `Weighted`, `Seed`, `Classic2d` | A chain of `random()` comparisons with hand-tuned thresholds |
| Data that survives a reload | Local Storage: *Set item*, *Get item*, *On item get* | Globals, which reset on reload; the Persist behavior, which keeps instances across layout changes, not across sessions |
| Logic shared by several events | Functions with parameters and return values; a *custom action* on the object or family if it acts on picked instances | The same action block pasted into several events |
| A part of the sheet that runs only in one phase: tutorial, a boss's AI, debug tools | A Group, off at start if the phase comes later, *Set group active* at the transition. Only its events stop: behaviors, timers and tweens keep running | A global mode variable that every event in that part compares |
| Which controls to offer: on-screen buttons for touch, keys and mouse on a desktop | Touch with *Use mouse input* off: *On any touch start* sets a global to touch, Mouse *On any click* or Keyboard *On any key pressed* sets it to desktop. The global shows the touch-controls layer and activates its group (detecting-input-method). A drag that behaves differently under a finger tests *Mouse button is down* every tick instead ([pitfalls: Touch](../plugins/touch.md)) | Touch triggers with *Use mouse input* on, which also fire for a click |
| Pause, slow motion, hit stop | *Set time scale* 0 (pause) or 0.1 (hit stop, slow motion); *Set object time scale* 1 on the UI that must keep moving; *Use time scale* off on the wait that ends it | A `paused` global checked in every event; behaviors disabled one by one |
| One thing after another inside one interaction: knock back, then re-enable; fade out, then go to layout | *Wait* and *Wait for previous actions* in the same block, which keep the picked instances | A flag set in the block and a Timer or `On any finished` elsewhere to finish the sequence |
| Reacting to a state any instance may reach, whoever started it | Timer *On timer*; Tween *On any finished* | A *Wait* that assumes one caller |
| HUD and UI that stay on screen while the layout scrolls | A layer with parallax 0, 0; *Global* on that layer if every layout shows the same HUD | Every-tick *Set position* from `ViewportLeft`/`ViewportTop` |
| A number shown as a bar, a gauge or a row of icons: health, fuel, progress, lives | One object, `Set width to value / max × LENGTH` clamped, its origin on the edge it grows from, a frame behind it, Tween *Width* for a change; the art decides which object ([recipes/progress-bars.md](../recipes/progress-bars.md)) | A Sprite scaled from its centre origin; a per-tick lerp of the width; one object type or one event per heart |
| Flat art at different depths, seen from an angle or circled: a diorama, a pop-up scene | Each plane on its own layer at a *Z elevation* spaced from `3DCamera.DefaultCameraZ`; 3D Camera *Look at position* every tick from a yaw, a tilt and a distance around the scene's centre; the HUD on a *2D* layer ([recipes/3d-layers.md](../recipes/3d-layers.md)) | *Rotate camera* fed by a drag, which turns the view around the camera; layer Z values typed for one screen size |
| A panel, menu or popup opened and closed as a whole | Its own layer, *Initially visible* off: *Set layer visible*; to fade it, *Set layer opacity* from a *Tween (value)* on a manager object (airborne-explorer, `MenuUI` and `ShopUI`; eventide, `PauseUI`) | *Set visible* on each of its objects, in every event that opens or closes it |
| A set of objects treated alike | Family; instance variables and behaviors declared on the family | Duplicate event blocks per object type |
| Objects that belong together | Container (created, destroyed and picked together); hierarchy for parent-relative position | UID variables, or every-tick position copying |

[manual: behavior-reference/timer.md, behavior-reference/tween.md,
system-reference/system-expressions.md "lerp", "dt", "find", "choose",
"chooseindex", project-primitives/events/expressions.md "Operators" (`%`,
`?:`), plugin-reference/dictionary.md "Has key",
behavior-reference/move.md, behavior-reference/bullet.md,
plugin-reference/array.md "Load", "Manipulating arrays", "Push", "Pop",
"Shuffle", "Contains value", plugin-reference/ajax.md "Request project
file", plugin-reference/json.md, plugin-reference/advanced-random.md
"Probability tables", plugin-reference/local-storage.md,
project-primitives/events/functions.md,
project-primitives/events/custom-actions.md,
project-primitives/events/groups.md, plugin-reference/touch.md "Use mouse
input", system-reference/system-actions.md
"Set group active", "Set time scale", "Set object time scale", "Set layer
visible", "Set layer opacity", "Wait", "Wait for previous actions to
complete", project-primitives/layers.md "Parallax", "Global layers",
"Initially visible", project-primitives/objects/families.md,
project-primitives/objects/containers.md; the pause, hit-stop and wait rows
are sourced in [pitfalls: Wait and time scale](../plugins/system.md)]

Before you choose, check two things. A Timer is state with transitions, so
list its transitions ([pitfalls: Timer](../behaviors/timer.md)). Array
*Load* reads Construct's own JSON format, so make the file in the Array
editor. For hand-written JSON, use the JSON plugin.

A behavior can exist and still be the wrong choice. An existing project
may keep a superseded feature, but a new project uses its replacement.
Fade runs a fixed series of opacity tweens, so use a *Tween (one property)*
on Opacity in its place. In place of Pin, use a hierarchy: *Add child* on
the parent. A hierarchy stays reliable where chains of pinned objects do
not. In place of the Solid behavior's own *Tags* property, use instance
tags, which *Use instance tags* selects by default. Z axis scale
*Normalized* is deprecated rather than superseded. A new project uses
*Regular*, where Z is a co-ordinate on the same scale as X and Y, so 3D
sizes match how they look.
[manual: tips-and-guides/superseded-features.md,
tips-and-guides/deprecated-features.md]

## Feel

[recipes/feel.md](../recipes/feel.md) has the recipe for each of these:
screen shake, hit stop, squash, hit flash, a choreographed sequence, a
following camera, a fade between layouts, a keyframed motion such as a
weapon swing, effects layered on one body, and a dragged thing that lags.
[recipes/sound.md](../recipes/sound.md) says which sounds play, when and
how loud, and how to make and check a placeholder file. If you generate a
game or write events for any of these, read both files first.
[recipes/scripted-sequences.md](../recipes/scripted-sequences.md) says
how an attack pattern, a cutscene or dialogue runs from a data file, and
how events parse and localise dialogue markup.

## Layout of the sheet

If you generate a project, or add a layout, layer, event sheet, group or
object type to one, read [project-files/new-project.md](../project-files/new-project.md)
first. It says how the examples split the sheets and groups, and how they
build the rest of the project.

## Smell table

If a draft matches one row, redesign it instead of patching it.

| The draft has | Why it is wrong | Replace with |
|---------------|-----------------|--------------|
| Instance variables holding another object's UID | A relation stored as pointers | Container, hierarchy, family, or a spatial condition |
| `Pick all` inside a trigger's sub-events, then a pick from a stored link | A pick discarded and rebuilt | Narrowing sub-events; a family for a second instance of the type |
| Globals such as `DragUID`, `Selected` | The trigger's pick copied into globals | The picked instance; store only what the engine cannot recover, such as a start position |
| Local variables filled by one block, then an `Else` chain on them | A program transcribed into events | Trigger, narrowing sub-events, `Else` |
| A boolean such as `occupied`, `busy` written from several events | State that copies a condition | `Is overlapping another object`, `Is dragging`, `Is playing` |
| A variable that counts instances: raised on create, lowered on destroy, or set from `PickedCount` every tick | A copy of the engine's count | `Brick.Count`, read where the decision is made. A destroyed instance is released at the end of the top-level event, and a pick of no instance stops its event. So test "none left" with `Brick.Count = 0` in a top-level event of its own ([pitfalls: How events work](../primitives/events/how-events-work.md)) |
| Custom actions named `attach`, `detach`, `sync` that write two variables | Two copies of one fact | One source, usually the engine's |
| `Pick by unique ID` for the object the trigger already picked | Re-picking what is picked | Delete the condition |
| `For each` before actions that already run per picked instance | A redundant loop | Delete it, unless a function call or a pick by one instance's position follows (see [pitfalls: Conditions](../primitives/events/conditions.md)) |
| `Every tick` stepping a progress variable by `dt` and feeding it to `lerp` between fixed ends | A tween written by hand, with its own "finished" bookkeeping. `lerp` toward a moving target, or from a value that the engine updates, is not this | Tween behavior, *On any finished* |
| Per-level numbers in variable names, expression constants or a chain of `Compare` blocks | A lookup table transcribed into events | Array or Dictionary project file, loaded once; Advanced Random for weights |
| A separated string used as a list or a record: `tokenat`/`tokencount` to read, a `Repeat` that rebuilds it to remove one item, `find` to test membership | An array transcribed into string handling, a loop per removal (a generated card game kept its draw pile, discard pile, hand and exhaust pile this way, and each card as 17 `\|`-separated fields) | Array: *Push*, *Pop*, *Delete*, *Shuffle*, *Contains value*; records in a JSON or Array project file |
| Behaviour coded in strings: sibling events testing `find(code, "B")`, `find(code, "BU")`, numbers cut out with `mid`, `tokenat`, `right` | A mini-language parsed by hand. `find` matches any part of the text and ignores case, so the branch of `"B"` runs for `"BU"` and `"s"` for `"SHIFT"` (a generated card game coded its enemy moves and card effects this way) | One field per fact, compared with `=` (Native first, "What a move, an effect or an attack does") |
| A cue list or dialogue markup read with `mid` one character at a time, in a *While* that runs every tick | Here the script is the product and a string is the right file for it, but the sheet parses it again on every tick | Parse the file once when it loads, into an Array of rows, and step that Array ([recipes/scripted-sequences.md](../recipes/scripted-sequences.md)) |
| A global `state` or `paused` compared at the top of many events | A phase switch or a pause written as a flag | A Group and *Set group active*; *Set time scale* for pause; a layout of its own for another screen |
| A boolean set by one event and a Timer or `Every tick` elsewhere waiting to finish what that event started | A sequence split across events | *Wait* or *Wait for previous actions* in the block that started it |

## Before proposing a structure

1. Write one line per relation: what touches what, what belongs to what,
   which instance the trigger picks.
2. Find an official example with the same behaviors. Filter
   `data/c3-examples/{locale}/*.json` on `used-addons` (`"DragnDrop"` under
   `behaviors` for a drag case). If `Construct-Example-Projects` is cloned
   next to this repository, copy the event shape from
   `example-projects/{id}/eventSheets/`.
   Read a sheet as events, not as JSON: `python
   <Construct3-Agent-Skills>/plugin/skills/construct3-agent-plugin/scripts/print_sheet.py --project
   <Construct-Example-Projects>/example-projects/{id}` prints it in the
   editor's wording, at about a quarter of the length.
   In `family-tree` and `alchemist`, the drop pattern is `On drop`, a
   sub-event `Is overlapping another object`, narrowing conditions, then
   `Else`.
3. Go through the Native first table, and the [Feel](../recipes/feel.md)
   table for each effect the draft names. For each delay, motion, table,
   phase, sequence or effect in the draft, name the built-in that does it.
   Place a new sheet, group or object type as
   [project-files/new-project.md](../project-files/new-project.md) says. If the
   events go into a project, group, name and comment them as
   [design/style.md](style.md) says.
4. Read the manual page for each mechanism that you plan to use.
5. Write the draft. Before you show it, check it against the smell table
   and the [pitfalls](../pitfalls.md), with the topic file of each
   group that it touches.
6. Only then verify every name with `python
   <Construct3-Agent-Skills>/plugin/skills/construct3-agent-plugin/scripts/lookup_ace.py
   OBJECT WORDS`. It prints the matching conditions, actions and
   expressions of a plugin or behavior, with their parameters and the JSON
   to write. It also prints the ACEs that all world objects share with
   them. If it finds nothing, say so and mark the closest match as
   unverified. Never write a name that it did not print.

## Worked case: pieces on a slot grid

If the events drag pieces onto slots or a grid to merge, swap, move or
return them, or if a draft matched a row of the smell table, read
[recipes/worked-case-slot-grid.md](../recipes/worked-case-slot-grid.md).
It writes the interaction with native features first, then as a program
transcribed into events.
