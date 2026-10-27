# A new project: sheets, layers, objects and look

Read this before you generate a project, add a layout, layer, event sheet,
group or object type to one, or decide how the game looks. It shows how the
official examples split a project into sheets, groups, folders and layers
and how they build its objects. It also gives a generated game's viewport,
look, grid, HUD and motion, and the generator template's helpers that hold
them. Design the events first with
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
  *Update* by default, and a feature's variables are locals of its group
  ([design/style.md](../design/style.md), the user's conventions).
- If the game has a second layout, each screen gets its own sheet (*Menu*,
  *Game*, *Credits*). Levels share one sheet (samuroof: Level1 to Level5
  use *Game*). If several screens need a subsystem, or the subsystem grows
  too large for the screen's sheet, it moves to its own sheet (*Player*,
  *Enemies*, *HUD*, *Camera*, *Effects*, *Sound*). The screen's sheet then
  includes that sheet (kiwi-story: eMain includes nine).
- Declare the global variables on one sheet, *Globals*, so that they can be
  found, as kiwi-story, samuroof and kitty-katcher do. A global is
  project-wide, whichever sheet declares it.
- If a phase begins later, its group starts inactive: a tutorial, a boss
  enabled on entry, debug tools (19 examples). Deactivating a group stops
  its events and nothing else, so it is not a pause.

[manual: project-primitives/events/groups.md, includes.md, event-sheets.md
"share events between layouts", variables.md "Global variables"; examples:
kiwi-story, samuroof, airborne-explorer, family-tree, labyrinth; survey of
Construct-Example-Projects, 2026-09-18]

## Viewport, look and HUD

- Pixel art uses a 320×180 viewport, *Nearest* sampling and *Integer scale
  outer*. Other art uses 1920×1080, *Trilinear* and *Scale outer*. Both
  fill the screen at any aspect ratio, and the screen then shows more than
  the viewport on its longer side. So a HUD element held to an edge carries
  the Anchor behavior for that edge
  ([coordinates-and-angles.md](../primitives/objects/instances.md)). The
  plain paper is the colour of the opaque `Background` layer and needs no
  object. A patterned backdrop in a one-screen layout lies over the
  viewport on a layer at parallax 0, and Anchor on all four edges stretches
  it to the screen ([anchor.md](../behaviors/anchor.md)). Only a scrolling
  level's backdrop, on a layer at parallax 1, and a popup's dim still reach
  the generator template's `SCREEN_PAD` past the layout
  ([input.md](../plugins/touch.md)). A one-screen game's layout is the
  viewport's size, with *Unbounded scrolling* on, so that the game stays
  centred with the HUD.
- Use few colours, each for a role: the player, what hurts, what is
  collected, the panels, the text. The median pixel-art project draws its
  art with hard edges in 35 colours, and 9 of them cover 95% of its opaque
  pixels. Labels use one to three colours, white in two of three.
  They use two sizes, rarely more than four. Every label has 4.5:1 contrast
  with what is behind it, or 3:1 for large-scale text from 18 pt up
  (WCAG 2.2, 1.4.3). Every studio project at 360 px or less samples
  *Nearest*, and most scale by whole numbers. The generator template holds
  these as `PALETTE` and `rgb()`, the colour check of `write_png()`, `FONT`
  and `TEXT_SIZE`, the contrast check of `hud_text()`, `PIXEL_ART` and
  `FULLSCREEN`.
- The look that the user gives comes first: a style, an art direction, or
  references or an existing project to take it from. The generator template
  names where it comes from in `USER_LOOK`, and `PALETTE` and `ART_STYLE`
  follow it. Contrast, the grid and clean edges hold in every look. Paper
  and ink, the colours, type and pointer of the next three items, and the
  checks of its taste hold only when the user gives no look
  (`docs/decisions/paper-and-ink-is-the-fallback.md`).
- When the user gives no look, a generated game is paper and ink until its
  art arrives: flat shapes on a white paper that fills the screen, without
  shadows, cards or panels.
  Lightness shows the hierarchy. The player is the one solid mass of ink,
  and structure is the faintest thing on the screen. Electric blue marks
  what is collected, and deep orange marks what hurts. Both are
  high-saturation hues, each at least 3:1 on the paper by colour alone. A
  rectangle is the player or structure, a circle is what is collected, and
  a triangle is what hurts. In an open field, the player and what it meets
  are drawn small in a large field, about 6% of the viewport's shorter side
  across. What is tapped keeps a finger-sized box around its drawing, and
  on a board, what is tapped fills that box. An area or a range is drawn as
  lines, a thin edge over a faint fill, and a reach is drawn as a dashed
  ring. A slot is a disc of the faint fill, the size of what fills it. An
  area with a rule of its own, such as a door or lava, is a striped Tiled
  Background. Where something is transparent, a mask or a background still
  to come, the backdrop is the transparency checker instead. Stretched to
  the screen, its cells start at the screen's edge, not on the grid. A
  level is a run of beats, each asking one thing, with a rest after every
  hard one.
  The generator template holds these as `PALETTE`, `SUBJECT`, `shape()`,
  `zone()`, `ring()`, `PATTERNS`, `area()`, `backdrop()` and `BEATS`. The
  records are `docs/decisions/paper-and-ink-look.md` and
  `docs/decisions/greybox-blockout.md`.
- Labels use Inter, which the skill ships in three weights. Chinese text
  falls back to the platform's font. A weight is a font file, so a label is
  never bold. The screen that the player plays on shows no game name. The
  round, the level or the mode is a small tracked tag at the top left. A
  number that the player plays for is large and light, under a small dim
  name. The controls are keys in thin ink boxes with their verbs, and the
  keys and verbs dim once the player has used them. The generator template
  holds these as `FONT`, `TEXT_SIZE`, `hud_tag()`, `hud_stat()`,
  `hud_keys()` and `hints()`, with `hud_header()` for the title of a menu
  or a result screen. It also copies the font files into `fonts/`.
- If the player points at things in a game, the game shows the pointer as
  colours of the object itself. The object is sky blue while the mouse is
  over it, and amber for an instant when it is touched. The generator
  template switches this with `POINTER`, which is off by default. The
  `pointer_*()` helpers draw and play it.
- The template's `art()` puts the art into the boxes of the stand-ins. The
  art comes from the session's image tool through the skill's
  `prepare_art.py`, or from the user. Do not draw the art in code, because
  art drawn in code looks worse than the stand-ins and mixes styles
  (`docs/decisions/art-from-the-image-tool.md`).
- Positions and sizes use a grid: 8 px at 320×180 (three quarters of the
  examples' x and five sixths of their widths sit on it), 32 px at
  1920×1080 (half of their x, three fifths of their widths). Use whole
  numbers, and use angle 0 unless the object should lean. The HUD is on the
  parallax-0 layer, against a corner or an edge. It stays a fifteenth of
  the shorter side inside that edge, in whole units, which is two units
  (64 px) at 1920×1080. The examples' edge offsets are 0, one unit or two.
  The screen's middle is for the game. On a TV, graphics stay 5% inside
  every edge (EBU R95).
  A tapped object is at least a finger wide: 48 dp (Android accessibility
  help), 44 pt (Apple HIG, *Accessibility*, the iOS default control size),
  44 px (WCAG 2.5.5). In viewport pixels, that is 48 × the viewport's
  shorter side / 360, because a phone shows that side across about 360 dp.
  Rounded up to a whole grid unit, it is 24 px at 320×180 and 160 px at
  1920×1080, with 8 dp between two targets.
  A label's box is as wide as its longest text and aligned to the edge
  that it is anchored to. A row of hearts is spaced by one unit. Nothing on
  the HUD overlaps or leaves the viewport. A value sits close under its
  name. The gap between two groups is at least 1.5 times the gap inside
  one group, the ratio that layout guides for slides and posters ask for.
  So the HUD stands apart from the playfield. The playfield is centred in
  what the HUD leaves, not on the whole screen, and it covers at least 15%
  of it. The one-screen layouts of the official game examples cover 80% at
  the median. The generator template holds these as `UNIT`, `MARGIN`,
  `TOUCH`, `anchor()`, `hud_text()`, `hud_stat()`, `row()`,
  `no_overlap()`, `play_area()`, `centred()`, `spaced()` and `filled()`.
  It holds the HUD to the screen's edges with `anchored()`.
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
