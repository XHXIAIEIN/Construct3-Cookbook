# Event Sheet Pitfalls: Bullet

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Bullet *Bounce off object* moves the ball out of the object at once. So
  an *On collision* with that object in a later event of the same tick
  finds no overlap and does not run. So feedback in events of its own with
  the same *On collision*, such as a sound, a squash, sparks or a hit
  freeze, runs only above the event that bounces, or as actions of that
  event. Put these events above it, because the collision events are
  tested in sheet order. [manual:
  behavior-reference/bullet.md "Bounce off object"; observed in a pong
  project, r506 preview, 2026-10-15: feedback groups each with Ball *On
  collision with* the paddles, below the event that bounces, on a paddle
  hit the time scale, the paddle's width and the Sparks count did not
  change; the same groups above it, all three changed]

- A Bullet's angle of motion and the object's angle are two separate
  values. They change together only while the behavior's *Set angle*
  property is on. 8 Direction and Car have the same property. The Bullet
  moves by a velocity vector. *Set angle of motion* turns that vector and
  keeps its length, so at speed 0 it does nothing. *Set speed* from speed
  0 then starts a vector at angle 0, and the object moves right. So a
  projectile that is created at speed 0 and gets *Set angle of motion*,
  then *Set speed*, flies right whatever its angle. Set the speed first,
  then the angle of motion. [manual:
  behavior-reference/bullet.md "Set angle", "Set angle of motion",
  "AngleOfMotion"; behavior-reference/8-direction.md "Set angle"; Ashley in
  Scirra/Construct-bugs#6105: by design, set the angle of motion again after
  the speed; runtime: exported c3runtime.js r504, Bullet `_SetAngleOfMotion`
  multiplies the new direction by the vector's length, and `_SetSpeed` sets
  dx to the speed and dy to 0 when the length is 0; observed in a game
  project, r504 preview, 2026-10-05: in recorded frames every projectile flew
  right, and with the two actions swapped each flew along its angle]

- A created bullet that hits nothing keeps flying outside the layout
  forever. These instances pile up and slow the game. A Destroy in its hit
  events removes the bullets that hit, not the ones that miss. Give a fired
  object the Destroy outside behavior with the region `layout`, or with
  `viewport` if the layout is larger than the screen. The behavior has no
  conditions or actions. In the official examples, the bullets without it
  end on Solid walls and ground. `check_project.py` warns when nothing
  removes a fired Bullet object that misses.
  [manual: behavior-reference/destroy-outside.md;
  observed in a generated shooter, stable r495.2 preview, 2026-10-09: a shot
  through an empty column was at y -658 three seconds later, and with
  Destroy outside it was gone; the 524 official examples: 58 of the 169
  Bullet objects their events create have Destroy outside, and all but four
  of the rest have Fade, Wrap or Tween, are destroyed or placed again by
  events, or hit a Solid]
