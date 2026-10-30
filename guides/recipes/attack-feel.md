# Attack feel

An attack feels right when its wind-up, its animation, its sounds and its
hit effect land on the same moments. This file gives the numbers for each
of them and the Construct way to build each. It applies to an action game
in which a click-to-attack hero makes a melee swing or a ranged shot. For
the general effects (shake, hit stop, squash), read [feel.md](feel.md).
For the loudness and the mix, read [sound.md](sound.md). For the frame
counts inside the hit effect itself, read [vfx-timing.md](vfx-timing.md).

The numbers come from the study of one published action game. Each rule
ends with the kind of its evidence:

- `data`: read from that game's data files (its gameplay settings, attack
  and animation data, sound banks, effect and UI definitions);
- `documented`: stated in the game's player-written reference;
- `derived`: computed from values in the data;
- `inferred`: a reading that the data does not state, so a starting point
  to tune;
- `observed`: played in a probe project in the editor's preview, with its
  release and date.

A distance is given as a multiple of the hero's move speed, because the
game measures in its own units. The Construct way in each rule comes from
the schemas. Unless the rule says so, no preview has played it.

## The timing of one attack

- The attack cycle is `1 / attackSpeed`. The wind-up runs from the start
  of the attack to the hit. Its length is the cycle times a wind-up share.
  By default, use a share of 18 to 20 %. For a heavy weapon, use 25 to
  30 %, and for a ranged or caster hero, 16 to 18 %. [derived]
- A base attack speed of 0.625 to 0.7 a second gives a cycle of 1.4 to
  1.6 s. The wind-up at that speed, `baseWindup`, is 0.25 to 0.35 s.
  [derived]
- Deal the damage, or launch the projectile, when the wind-up ends, not
  when the animation ends. A melee hit lands at that moment, with no delay
  for distance. [data, derived]
- When the attack speed rises, the wind-up shrinks with the cycle. To keep
  the weight of a heavy weapon, shrink it by half as much:
  `windup = baseWindup + 0.5 × (cycle × share − baseWindup)`.
  [documented, data]
- Clamp the attack speed between 0.2 and 3.0 a second. Above about 1.6 a
  second (1.3 to 2.1, by hero), switch to a shorter attack animation
  instead of a faster playback of the long one. [documented, data]
- In Construct, run the attack on a Timer behavior. When the attack
  starts, *Start timer* "windup" for the wind-up and "cycle" for the
  cycle. *On timer* "windup" deals the damage or creates the projectile.
  *On timer* "cycle" starts the next attack while the target is in range.
  [inferred]
- An empowered strike from a skill has its own wind-up of about 0.30 to
  0.34 s. This wind-up shrinks only a little as the attack speed rises.
  Store it as its own number, not as a share of the cycle. [derived]

## The attack animation

- Make one animation per attack, not three. It holds the wind-up, the
  release and the recovery. In one studied 60-frame attack at 30 fps, the
  release is frame 10 and the 50 frames after it are the recovery. [data]
- Put the release frame where `baseWindup` ends: frame 8 to 11 at 30 fps.
  Most of the game's attacks match this within ±20 %. [derived]
- Scale the playback so that the release frame lands on the current
  wind-up: Sprite *Set speed* to `Self.OriginalAnimationSpeed * baseWindup /
  windup`. Run it after *Set animation*, because *Set animation* resets
  the speed to the animation's own
  ([pitfalls: Sprite](../plugins/sprite.md)). The next attack then cuts
  the recovery short: at about 90 % of it at the base attack speed, and at
  about 45 % at 2 attacks a second. [derived, inferred, observed]
- Draw the last frames of the recovery close to the first pose of the
  wind-up, because the next attack can cut the recovery at any frame.
  [inferred]
- Start each attack from its first frame, with no blend from the previous
  attack. For a Sprite, *Set animation* to the chosen attack from the
  beginning. If that animation is already playing, *Set animation* does
  nothing, so use *Start animation* from the beginning
  ([pitfalls: Sprite](../plugins/sprite.md)). [data]
- On every attack, pick one of two attack animations at random, 50 % each,
  instead of alternating them: `choose("Attack1", "Attack2")`. To make one
  rarer, weight it: `random(1) < 0.75 ? "Attack1" : "Attack2"`.
  [data, inferred]
- An attack that a state chooses, such as an empowered strike or another
  form, stays outside the random pick. Before the pick, test the state
  variable that names such an attack. If the variable is set, play that
  attack. [data, inferred]
- When the hero stops attacking, let the attack animation finish, then
  play idle: Sprite *On finished* "Attack1" sets the idle animation. A move
  order during the recovery switches to the run animation at once.
  [derived, documented]
- On a 3D model, cut from one attack to the next with no transition. Use
  a transition of 0.1 s from an attack to idle or run, and from an
  empowered strike to a basic attack. These are the commonest values in
  the game's animation graphs. Set them in 3D Model *Set animation*,
  *Transition duration*. To restart a clip that is playing, read
  [pitfalls: Sprite](../plugins/sprite.md). [derived]

## Cancelling and resets

- A move order during the wind-up cancels the attack: *Stop timer*
  "windup" and carry out the move. [data, documented]
- Ignore move orders in the last 0.033 s of the wind-up and for 0.033 s
  after the release. Then a late click does not cancel the hit. At 60 Hz,
  0.033 s is two ticks. Read the time left as
  `Self.Timer.Duration("windup") - Self.Timer.CurrentTime("windup")`.
  [data, documented]
- A skill that resets the attack does *Stop timer* "cycle", so the next
  attack can start at once. A reset during the wind-up also cancels that
  attack. Do the reset in the skill's own event. A "can reset" flag on the
  skill is then only a label for filters, such as the skills that an AI
  may use. [documented, data]
- A skill used during the wind-up acts by its kind:
  1. A skill with a cast time cancels the attack. If the wind-up has less
     than 0.033 s left, the skill waits for the hit.
  2. An instant skill that does not reset leaves the attack running.
  3. A resetting skill cancels the attack, stops the cycle and makes the
     next hit the empowered strike.

  [documented, derived]
- A skill's default cast time is 0.25 s. During the cast time, the hero
  cannot move, attack or cast, and the player cannot cancel the cast. Big
  skills take 0.4 to 1.0 s, and buffs, dashes and skills centred on the
  hero take none. Time the skill's effect by its cast-time timer, not by
  the animation, which only shows the effect. [data, derived]
- If the player presses a skill during its cooldown or a lock, and the
  skill will be ready within 0.5 s, keep the press. Cast the skill the
  moment it is ready. Otherwise, drop the press. Fast combo skills use a
  window of 0.05 to 0.3 s, so store the window as a number on each skill.
  Never queue a basic attack. [data]

## Projectiles

- A ranged basic attack is a homing projectile at a constant speed. It
  deals its damage when it reaches the target, and then it is destroyed.
  Its speed is 6 to 9 times the move speed for a marksman and 4.5 to 5
  times for a caster. Launch it from the weapon, and aim it at the chest
  of the target, not its feet. [data; ratios derived]
- In Construct, create the projectile at the weapon's image point. Give it
  the Bullet behavior. Run *Set speed* first and *Set angle of motion*
  after it, because in the other order the projectile flies to the right
  ([pitfalls: Object instances](../primitives/objects/instances.md)).
  Every tick, set the angle of motion to `angle(Self.X, Self.Y, Target.X,
  Target.Y)`. Deal the damage when the distance to the target is less than
  the distance that the projectile moves in one tick. [inferred]
- A ranged attack with a short range, 0.9 to 1.3 times the move speed, can
  work without a projectile. Its damage lands at the release, and only the
  hit effect plays. [data, inferred]
- A melee weapon with a long reach, such as a whip or a chain, shows the
  reach as an effect in the animation. It still deals its damage at the
  release, with no projectile. [data, inferred]
- A skill projectile either stops at the first enemy that it touches, or
  it flies to its end point and takes effect there. Common speeds are 3.5
  to 6 times the move speed, and fast ones fly at 6.5 to 10 times.
  [data; ratios derived]

## Sounds of an attack

- Play up to three sounds per attack. Play each from the event of its
  moment, not from an animation frame. A swing plays when the wind-up
  starts, a launch when a projectile is created, and a hit when the damage
  lands. [data]
- In every studied hero, the hit sound plays with no delay after the
  damage. A bow draw can start 0.04 to 0.3 s into the wind-up. [data]
- If the game's sounds follow the music grid ([sound.md](sound.md),
  "Immediate or on the grid"), the damage moves to its cell, and the hit
  sound moves with it.
- Choose the hit sound by the target's material. The material's set
  replaces the default set instead of playing as a layer on top of it. The
  sets are flesh, which is the default, then metal, stone and wood, with 4
  variants each. Melee attacks and physical projectiles use them, but
  spells and arrows do not. [data]
- In Construct, give the target an instance variable `material`, and play
  `"hit_" & material & "_" & n` with Audio *Play (by name)*. If the
  variable is empty, use flesh. A critical hit adds one fixed heavy layer.
  [data, inferred]
- Play the variants from a shuffled list, as [sound.md](sound.md) says
  ("Tiers and loudness"). In Construct, keep the variant numbers in an
  Array and *Shuffle* it. Read the next index on each play. When the list
  is used up, *Shuffle* it again. [data]
- An unpitched sound with only 2 variants can add a random rate within ±2
  to 3 semitones: *Set playback rate* to `2 ^ (random(-2.5, 2.5) / 12)` on
  its own tag. [data]
- Lengths: a swing 0.4 to 0.7 s, a hit 0.7 to 1.2 s, a critical layer 1.0
  to 1.6 s, a skill cast 2.3 to 3.3 s. [data]
- When the next hit sound plays, let the previous one play to its end. Do
  not *Stop* it, because a hit outlasts the shortest attack interval, so
  the two overlap. [derived]
- One moment can play several layers with delays. An empowered strike can
  start its wind-up sound at once and a longer impact 0.2 to 0.25 s later.
  The impact comes about 0.1 s before the damage, and the strike plays no
  separate hit sound. [data; offset derived]
- A sound of a lasting state, such as a buff or a flying projectile,
  starts with the state, on its own tag. When the state ends, the sound
  fades out in 0.25 s, or in 0.5 s for a projectile: Audio *Fade volume*
  to −60 dB, then *Stop* in *On fade ended*. [data, inferred]
- Small motion sounds, such as armour, footsteps or a shell ejecting, go
  on animation frames: Sprite *On frame changed* with a test of
  `AnimationFrame`. Most of them fall in the recovery or a turn. [data]

## Hit effects and damage numbers

- A hit effect is 2 to 8 one-shot layers that end within 0.2 to 0.5 s.
  [data]
  - A flash of 0.3 s that shrinks to nothing, or grows from small.
  - A slash or impact shape of 0.2 s that grows to 4 and then 8 times its
    size as it fades.
  - Optional sparks of 0.3 to 0.45 s that fly outwards.
- Divide that length into a rise, a peak, a fall and an ember, and keep
  the fall the longest part. The peak lands on the damage, so the rise
  runs before it. [vfx-timing.md](vfx-timing.md) gives the frame counts of
  the four parts and the ratio that separates an impact from a charge.
- Make each layer a Sprite with Tween (one property) on *Size* and on
  *Opacity*. Set *Destroy on complete* on the longer of the two tweens.
  [inferred]
- A melee hit deals its damage in *On timer* "windup". Its effect peaks
  on that tick, so a sweep layer, such as a trail that draws the swing,
  rises before it ([vfx-timing.md](vfx-timing.md)). Build it in four
  steps:
  1. When the attack starts, run *Start timer* "sweep" for
     `windup - RiseFrames / 60`, with `RiseFrames` from 6 to 8. If the
     wind-up is shorter than the rise, create the sweep layer at once
     instead.
  2. In *On timer* "sweep", create the sweep layer at opacity 0. Tween its
     *Opacity* to 100 over `min(RiseFrames / 60, windup)`.
  3. In *On timer* "windup", start the sweep layer's fall with a second
     *Opacity* tween. It stops the rising tween, so the peak lands on the
     tick of the damage. Set *Destroy on complete* on the fall.
  4. In the same trigger, create the burst layers, such as the flash, the
     impact shape and the sparks. Bring each one to full opacity in the
     first 10 % of its life, 1 to 3 frames at 60 fps. Fade it over the
     other 90 %. In a pixel-art game, step it through animation frames and
     fade only its glow ([pixel-art-vfx.md](pixel-art-vfx.md)).

  The lengths of 0.2 to 0.5 s above count from the damage. When the attack
  speed changes, keep the rise and move only its start. [derived,
  inferred]
- Every event that cancels the wind-up also runs *Stop timer* "sweep". It
  destroys the sweep layer if one exists. A move order, a skill with a
  cast time and a reset each cancel it. [inferred]
- Create the effect at the target's chest, an image point above its
  centre, and keep it there with Pin *Pin to image point*. Set about half
  of the layers to the *Additive* blend mode. [data, inferred]
- The game's data holds no tint, flash or outline of the unit that is hit.
  Its only flash is an additive sprite over the chest that shrinks to
  nothing in about 0.3 s. The game changes the colour of the unit only for
  lasting states. For the other ways to show a hit, read
  [feel.md](feel.md), "Hit feedback". [data]
- Give each attack the name of its hit effect. If the attack has no hit
  effect, leave the name empty. Do not add a global default effect,
  because many plain hits show no effect while their critical hits show
  one. A generic effect is a 0.3 s flash that shrinks to nothing. A
  critical hit adds a 0.5 s ring that grows from 0.5 to 1.5 times its
  size. [data, inferred]
- A damage number appears at twice its size and shrinks to its resting
  size in 0.15 s. It flies 50 to 65 px/s sideways, alternating left and
  right, and 150 to 180 px/s up, under a gravity of 500 px/s². It starts
  to fade at 0.4 s, fades over 0.45 s and lives about 0.85 s. The data
  names no unit, so the pixels are a reading. [data, inferred]
- In Construct, give the number the Bullet behavior with *Set gravity*
  500. *Set speed* to the length of the start velocity, then *Set angle of
  motion* to its direction. Draw the number with a Sprite Font and tween
  its *Size*, because a Text whose font size changes redraws every frame
  ([pitfalls: Text](../plugins/text.md)). [inferred]
- A critical number is 1.75 times larger and starts within ±20 px of the
  hit. It flies faster, about 100 px/s sideways and 200 px/s up, under a
  gravity of 625 px/s². It stops at the top of its arc, about 0.32 s in
  (`200 / 625`), and fades there on the same schedule. A normal number
  keeps falling as it fades. [data, inferred]
- To stop a critical number, start a Timer for `vy / gravity` seconds when
  the number is created. In *On timer*, *Set enabled* its Bullet off.
  [inferred]
- Merge damage over time and rapid hits into one number. A further hit
  within 0.35 to 1.3 s adds to the number and extends its life. Show at
  most 20 numbers, and queue the rest 0.2 s apart. [data]
- Where numbers pile up, draw a plain hit at 0.8 of the base size and 55 %
  opacity, and keep the critical numbers over the plain ones. In a burst of
  40 plain numbers over 3 critical ones, the faint plain hits left every
  critical number readable; drawn alike, the critical numbers were lost.
  [observed in a probe project, r506.3 preview, 2026-10-26]
- To keep the critical numbers on top, give the number a `rank` instance
  variable, 1 for a critical hit, and run System *Sort Z order* by `rank`
  from an *Every tick* event. Do not run the sort in the function that
  creates the number: the sort misses the numbers created in that tick, the
  new one included, with or without *Pick all* first. Sorted there, a burst
  created in one tick kept a plain number over a critical one in 60 of 60
  overlapping pairs, and sorted every tick, in none.
  [observed in a probe project, r506.3 preview, 2026-10-26]
- For the ghost of a health bar, the part that shows a loss and then
  closes, read [progress-bars.md](progress-bars.md).

## Orders and the view

- The hero reaches full speed at once: MoveTo *Set acceleration* 0. The
  move speed is about twice the melee range and 5 times the hit radius.
  [data, derived]
- Keep three separate radii. The smallest is for pathing and for pushing
  other units. The hit radius is about 1.9 times the smallest, and the
  radius for picking the unit with the mouse is about 3.4 times. Attack
  range counts from the edges of the two hit circles, not from the
  centres. [data, derived]
- An order on an enemy makes the hero walk into range, then attack. An
  order on the ground moves the hero with no attack on the way. The hero
  looks for targets only once it stops. Scan for targets every 0.2 s, and
  keep the current target during a wind-up. [data]
- The event that accepts a move order creates the ground marker, not the
  mouse click, so a refused order shows no marker. The marker lives
  0.4 s. Four arrows slide to the point, flatten and fade, and a ring
  grows from nothing and fades in 0.2 s. Use Tween (one property) on *X*,
  *Y*, *Y Scale* and *Opacity*. [data, inferred]
- When an attack or an aimed skill starts, turn the hero to face the
  target at once, instead of rotating it towards the target.
  [data, inferred]
- A 3D camera over this kind of game looks down at 55°. Put it behind the
  point it follows by `0.574 × d` and above it by `0.819 × d`, and use 3D
  Camera *Look at position* on the point. Tune the distance `d` and the
  field of view in the project, because the data does not give them.
  [data, derived]
