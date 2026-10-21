# Event Sheet Pitfalls: Scroll To

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Scroll To *Shake* replaces the running shake: it overwrites the magnitude,
  start and end. So a 3 px tombstone shake 0.45 s after an 8 px kill shake
  ends the kill shake. A 3 px splash shake in the same tick as the kill shake
  also replaces it, by running later. Gate *Shake*: call it only if the new
  magnitude is not smaller than the remaining one, `mag × max(0, 1 − (time −
  start) / duration)`, kept in variables. The runtime also multiplies the
  magnitude by `min(object time scale, 1)` and divides the duration by it. So
  during a 0.1 hit stop it shakes at a tenth and in effect starts when the
  stop ends. *Set object time scale* 1 on the camera object keeps it at full
  strength through the stop. [runtime: exported c3runtime.js r504, scrollto
  `Acts.Shake` calls `SetShakeMagnitude`, `SetShakeStart`, `SetShakeEnd`
  unconditionally; `Tick2` computes `mag × min(n, 1)` and `(end − start) / n`
  with `n` the instance's time scale; observed in a game project, r504
  preview, 2026-10-02: an axe kill shook 3 px before the gate and 7 px after,
  and with the camera's time scale at 1 the 12 px boss shake peaked at 10 px
  inside the 0.1 s stop]
