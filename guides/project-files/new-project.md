# A new project: sheets, layers, objects and look

Read this before you generate a project, add a layout, layer, event sheet,
group or object type to one, or decide how the game looks. It shows how the
official examples split a project into sheets, groups, folders and layers
and how they build its objects. It also names the rules of a generated
game's look, and gives its viewport, HUD and motion with the generator
template's helpers that hold them. Design the events first with
[design/thinking.md](../design/thinking.md).

## Sheets and groups

The official examples split events in these ways (groups in 237 of
432, several sheets in 48, includes in 14). Before you write into a
project, read [design/style.md](../design/style.md) for what goes inside a
group and how to name and comment it.

- A game of one layout has one sheet, with groups by subsystem named as in
  the examples: *Setup* (`On start of layout`), *Player*, *Controls*,
  *Camera*, *Tutorial*, *Game over*, *Restart* (the restart key and
  *Restart layout*). What runs every tick goes in a group of its own,
  *Update* by default. A feature's variables are locals of its group, and
  the groups sit in one outer group named for the game, whose static
  locals hold the state they share, so the sheet has no globals
  ([design/style.md](../design/style.md), the user's conventions).
- If the game has a second layout, each screen gets its own sheet (*Menu*,
  *Game*, *Credits*). Levels share one sheet (samuroof: Level1 to Level5
  use *Game*). If several screens need a subsystem, or the subsystem grows
  too large for the screen's sheet, it moves to its own sheet (*Player*,
  *Enemies*, *HUD*, *Camera*, *Effects*, *Sound*). The screen's sheet then
  includes that sheet (kiwi-story: eMain includes nine).
- Declare the global variables on one sheet, *Globals*, so that they can be
  found, as kiwi-story, samuroof and kitty-katcher do. A global is
  project-wide, whichever sheet declares it. Only what another sheet
  reads is global; state that the groups of one sheet share is a static
  local of its outer group.
- If a phase begins later, its group starts inactive: a tutorial, a boss
  enabled on entry, debug tools (19 examples). Deactivating a group stops
  its events and nothing else, so it is not a pause.

[manual: project-primitives/events/groups.md, includes.md, event-sheets.md
"share events between layouts", variables.md "Global variables"; examples:
kiwi-story, samuroof, airborne-explorer, family-tree, labyrinth; survey of
Construct-Example-Projects, 2026-09-18]

## Viewport, look and HUD

- A generated game fills the screen at any aspect ratio (`screen.fill`),
  so the screen shows more than the viewport on its longer side, and a HUD
  element held to an edge carries the Anchor behavior for that edge
  ([coordinates-and-angles.md](../primitives/objects/instances.md)). A
  patterned backdrop in a one-screen layout lies over the viewport on a
  layer at parallax 0, and Anchor on all four edges stretches it to the
  screen ([anchor.md](../behaviors/anchor.md)). Only a scrolling level's
  backdrop, on a layer at parallax 1, and a popup's dim reach the generator
  template's `SCREEN_PAD` past the layout ([input.md](../plugins/touch.md)).
  A one-screen game's layout is the viewport's size, with *Unbounded
  scrolling* on, so that the game stays centred with the HUD.
- The look of a game that the skill generates is held by the rules of the
  skill's
  [look manifest](https://github.com/XHXIAIEIN/Construct3-Agent-Skills/blob/main/plugin/skills/construct3-agent-plugin/assets/look-manifest.json).
  Each rule has an id, its value or the template setting that holds it,
  its scope and its record. Read the rule
  there; this page names it by its id and does not restate it.
  - The look that the user gives comes first. With it, only the rules of
    scope `every-look` hold. Without it, the game takes paper and ink, the
    rules of scope `paper-and-ink`.
  - Colour: `colour.palette-only`, `colour.structure`,
    `colour.accent-contrast`, `palette.greys`.
  - Text: `text.contrast`, `type.scale`, `type.min-size`, `type.sizes`,
    `type.inter`, `type.pixel-font`.
  - Grid and screen: `grid.unit`, `grid.shape-size`,
    `grid.world-placement`, `grid.runtime-spawn`, `screen.fill`,
    `screen.safe-area`, `pixel-art.sampling`.
  - HUD and layout: `hud.paper`, `touch.target`, `layout.proximity`,
    `layout.balance`, `layout.fill`, `layout.spread`, `layer.z-order`.
  - Paper and ink's shapes: `subject.size`, `subject.player-shape`,
    `lines.areas`, `backdrop.sheet`, `pattern.areas`, `pointer.colours`,
    `motion.hit`.
  - Art: `art.routes`, `art.roles`, `art.ids`, `art.frames`,
    `art.contrast`.
- A line 1 px thick drops out on some rows when the screen draws the
  viewport smaller than its size. So draw a rule at least as thick as the
  viewport's height divided by the screen's height, rounded up. In a
  1280×720 viewport previewed 720 px wide, Sprite rules 1 px thick showed
  on two rows of four. Rules 2 px thick showed on all four at 720, 960 and
  1100 px wide. The template's `LINE` is 1 px at 720 high and 2 px at
  1080. [observed in a demo project, r506.3 preview, 2026-10-20]
- A button's text is its label, centred on it, and the two move and hide
  together. A bar's name stands in front of the bar. A one-screen layout is
  a stack of bands: the title, the status line, the stage in the middle and
  the hint at the bottom. The stage's main object takes a large share of
  the stage. The generator template holds these as `button()`,
  `labelled_bar()`, `bands()`, `band_text()` and `fit()`, and the record is
  `docs/decisions/layout-by-name.md`. The template's `press()` presses a
  button, and `count_up()` counts a score ([feel.md](../recipes/feel.md);
  `docs/decisions/count-up-and-press.md`). For a settings screen, the
  template's `slider()`, `toggle()` and `text_input()` make the slider,
  toggle and text input (`docs/decisions/input-controls.md`).
- Each class of object keeps one kind of motion, so the player can tell
  what matters. The HUD and menus fade and slide. The studio cohort has
  480 one-shot tweens on objects of a parallax-0 layer, in 71 projects. Of
  these, 73% tween the opacity and 92% use a sine ease, mostly
  `easeinoutsine`. The middle half lasts 0.5 to 1 s, and 7 overshoot. A
  button's press is quicker: 0.1 to 0.5 s on its size or opacity, or a
  pressed frame swapped in at once. The camera moves slowly and evenly,
  1 s or more with `easeinoutsine`, though only 4 projects tween it.
  Overshoot (`easeoutback`, `easeoutbounce`, an elastic ease) is for world
  objects. It is in 102 of their 1613 tweens, mostly on a vertical offset
  or the size, as in a hit, a landing or a pop
  ([feel.md](../recipes/feel.md)). Give a HUD element a bounce only when it
  is the subject of the moment, such as a title card. [survey of the Tween
  actions in the examples' studio cohort, 2026-10-08: each action's object
  classed as HUD when it has an instance on a layer of parallax 0, else as
  world or camera]

## Layouts, sheets, folders and layers

- One `ObjectRepository` layout, with no event sheet, holds one instance of
  every type that the events create, and nothing else. No object is
  global. Keep this layout out of the first place in the project, because
  the game opens on the first layout. If the order still puts it first,
  give it a sheet of one event: *On start of layout*, then *Go to layout*
  to the first screen [a studied project, 2026-10-06].
- Up to about sixty types, `MainCode` is the only sheet. Beyond that, each
  screen has a sheet (`GameEvents`, `MenuEvents`, `CreditsEvents`),
  subsystems have included sheets (`PlayerEvents`, `EnemyEvents`,
  `SoundEvents`), and `Globals` holds shared variables.
- From about forty types, every type is in an object folder, one level
  deep, and the root is empty: `System` (managers, camera, fader, input),
  `Player`, `World`, `UI`, `Interactable`, `Global`, and one folder per
  extra screen (`MainMenu`, `Credits`). Below forty types, the list stays
  flat.
- The layers, from bottom to top, are `Background`, `World`, then `UI` (or
  `HUD`) and `Fader`, each at parallax 0. `Tutorial` has its own layer. A
  layout has two or three layers.
- A layer lists its instances in the order they draw, back to front, as an
  editor user arranges them. The backdrop and the flat areas come first.
  Then come the things that stand, from far to near by the Y of their feet,
  a child after its parent and a label after its board or bar. The
  generator template's `z_order()` puts every layer in this order.

## Objects

- Collision and graphics are separate objects. `PlayerCollision` is an
  invisible one-colour Sprite with Platform or 8 Direction, and
  `PlayerGraphics` holds the animations and no behavior. The two form a
  container. *PlayerCollision: On created* sets the graphics' position and
  calls *Add child* (X, Y, destroy with parent). The graphics then follow
  the collision body, so no event copies the body's position to them.
  Enemies are built the same way: `EnemyCollision` with `EnemyAnimations`.
  A shadow is a child Sprite (`PlayerShadow`). Use a hierarchy, not Pin.
- Ground is a Tilemap with Solid (`GroundCollision`) under the art
  (`Background`, a Tiled Background).
- Movement behaviors run with *Default controls* off. The input events call
  *Simulate control* under Keyboard *Key is down*, which is true every tick
  that the key is held. Under *On key pressed*, the player moves for one
  tick only ([pitfalls: Touch](../plugins/touch.md)).
- An object without a picture is an invisible 16×16 one-colour Sprite,
  stretched over its area if it has one. `GameManager` holds the Timers
  and value Tweens that the sheet reads. `Camera` carries Scroll To, or
  `PlayerCollision` carries it instead. The events test `Trigger`,
  `TeleportTrigger`, `FinishLine`, `SpawnPoint` and `InvisibleWall` with
  Solid by *On collision* or *Is overlapping*, and an instance variable
  tells them apart.
- `Fader` is a viewport-sized one-colour Tiled Background on the top layer,
  with Tween on opacity. Its *On finished* runs *Go to layout* or *Restart
  layout*.
- A light is a one-colour Sprite with *Additive* blend and a Glow or Blur
  effect that softens its edges. Darkness is a `Darkness` sprite or layer
  with *Destination out* holes, on a layer with *Force own texture*.
- Two games of three use Sprite font for text, and the third uses the Text
  plugin. No project uses both. The generator template's labels are Text
  objects in Inter.
- Behaviors and Particles objects make the feel: Tween on almost
  everything, fades included (Tween on opacity), Timer, Sine, Flash, Rotate
  and Bullet. The effects used are Adjust HSL, Glow, Blur and Warp
  object.
- A third-party effect that does not support WebGPU makes the whole project
  render with WebGL, whatever *Enable WebGPU* says. Before you add one,
  read Platform Info `Renderer` in a preview. Prefer the built-in effect of
  the same purpose where one exists. [manual:
  project-primitives/projects.md "Enable WebGPU";
  plugins/platforminfo.json `renderer`]
- Families serve Z order (`ZOrderables`) and enemies. Containers hold the
  collision and graphics pair, and an enemy with its parts. The player's
  instance variables are `hp`, `maxHp`, `dead`.
