# Event Sheet Pitfalls: Particles

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- A Particles object given a Sprite as its *Object* spawns real instances.
  *On created* fires for each, and they are not children of the emitter (the
  example parents them by hand). Per-particle state such as a colour frame
  comes from *On created* plus *Pick nearest* emitter, read from the
  emitter's instance variable. [example: child-particles; observed in a game
  project, 2026-09-17; observed in that example, r504 preview, 2026-10-02:
  with its parenting event turned off, 49 of 50 particle sprites had no
  parent]
