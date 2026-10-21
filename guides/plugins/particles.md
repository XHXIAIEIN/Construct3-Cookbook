# Event Sheet Pitfalls: Particles

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- If a Particles object has a Sprite as its *Object*, it spawns real
  instances of that Sprite. *On created* fires for each of them. They are
  not children of the emitter, so the example parents them by hand. For
  per-particle state such as a colour frame, use *On created* with *Pick
  nearest* emitter, and read the value from the emitter's instance
  variable. [example: child-particles; observed in a game
  project, 2026-09-17; observed in that example, r504 preview, 2026-10-02:
  with its parenting event turned off, 49 of 50 particle sprites had no
  parent]
