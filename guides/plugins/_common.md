# Event Sheet Pitfalls: Common to all objects

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- *Pick children* picks only among the child type's instances already picked.
  A child type in the parent's container is narrowed as soon as the parent
  is. In `Piece: On drop`, `PieceArt` is in `Piece`'s container and is
  already the dragged piece's art. So `Pieces: Pick children PieceArt` finds
  nothing on the piece under it. Give the child type a family of its own,
  `Arts` with the one member `PieceArt`, and pick children of the family,
  because its picks are kept apart from the container's. [runtime: exported
  c3runtime.js r503, `AnySDK.PickChildren` keeps the child class's current
  picks unless they are all of it, then applies the result to the child's
  container; observed in a game project, r503 preview, 2026-09-28: the merge
  target's body was not picked until the pick went through a one-member
  family]

- *Pick parent* with *Which* set to *Own* looks only one level up. With
  `Robot → Arm → Hand`, `Hand: Pick parent Robot (own)` picks nothing,
  because `Hand`'s own parent is `Arm`. Then the event's actions never run,
  and no error shows. If the parent you name is not the direct one, set
  *Which* to *All*. *Pick children* with *All* works the same way down the
  hierarchy.
  [manual: plugin-reference/common-features/common-conditions.md "Pick
  parent"; observed in a game project, r504 preview, 2026-09-30: a deploy
  flag cleared from `On Tween "hop" finished` through `Pick parent base
  (own)` stayed set, and the piece never started attacking until the pick was
  changed to *All*]

- A hierarchy child can be on another layer than its parent, because the
  connection is per instance, not per layer. A child on a lower layer stays a
  child. So a lifted parent can be drawn above everything while its parts
  stay under an outline. [releases: beta.json, "hierarchy information not
  duplicated properly if connections were setup between instances in
  different layers"; observed in a game project, 2026-09-17; observed in a
  minimal project, r504 preview, 2026-10-02: a child on another layer than
  its parent kept the parent and moved 40 px with it]

- *ChildCount*, *Compare child count* and *Has children* count every attached
  child of any type. So a second child type on the same parent changes every
  count that meant one type. Get the top index from *Pick children* plus
  *Pick highest/lowest* (highest) on that type, or count in a *For each*
  over the picked children.
  [manual: plugin-reference/common-features/common-expressions.md
  "ChildCount", common-conditions.md "Compare child count"; observed in a
  game project, 2026-09-17]

- *Set mesh point* in *Relative* mode adds to the point's current position,
  not to its default, so a per-tick derivation accumulates. Derive with
  *Absolute* and normalised coordinates (0..1 across the object box, values
  may go past it). A texture value of -1 leaves the texture position
  unchanged. [manual: plugin-reference/common-features/common-actions.md "Set
  mesh point"]

- A mesh pulled into a trapezoid in X and Y bends every straight line of
  its image: each cell is drawn as two triangles, and the image follows each
  triangle on its own, so a line kinks where it crosses a diagonal. More
  points make the kinks shorter but never remove them, and rows spaced
  evenly show no depth. Moving the top points sideways gives a skew
  (parallelogram); pulling them in gives a trapezoid, which reads as a plane
  seen at an angle only with depth. For that plane, leave X and Y at their
  defaults and give the near row a Z with *Set mesh point*
  (mesh-z-elevation), on a layer whose *Rendering mode* is *3D* under the
  layout's *Perspective* projection, as
  [3d-layers.md](../recipes/3d-layers.md) says. Its lines stay straight
  and its rows get closer towards the far edge, and a 2x2 mesh is enough.
  The raised row draws larger than the object box, so size or place the
  object for the tilted shape. [observed 2026-10-18 in a preview, r506.2
  editor, 778x511 viewport: on a Sprite with a 16x12 grid image, an 8x8
  mesh with its top row pulled in by 0.3 on each side drew zigzag lines and
  even rows; a 2x2 or 8x8 mesh with x and y at their defaults and z 600 on
  the bottom row drew straight lines and rows closer towards the top; manual:
  scripting/scripting-reference/object-interfaces/iworldinstance.md
  "setMeshPoint"]

- *Set width* stretches a Sprite's whole image, repeats a Tiled Background's,
  and on a 9-patch stretches or tiles the middle while the corners keep their
  size. So make a bar with a painted fill a Tiled Background, which shows a
  cut of the painting below its own width. Make a bar with caps a 9-patch,
  whose width must stay positive. [manual:
  plugin-reference/tiled-background.md "display an image in a repeating
  pattern"; plugin-reference/9-patch.md "a Sprite object, which just stretches
  its entire image", "useful for representing things like progress bars";
  reference: recipes/progress-bars.md]

- *Move to top* moves only the instance it runs on. A hierarchy's children
  keep their places in the Z order. So a dragged piece whose parent went to
  the top still draws its body, face and label under the pieces created after
  it. Pick the children (*Pick children*) and move every part to the top,
  bottom part first, as the parts should stack. [manual:
  plugin-reference/common-features/common-actions.md "Move to top", "top of
  its current layer"; observed in a game project, r503 preview, 2026-09-29;
  observed in a minimal project, r504 preview, 2026-10-02, through the
  scripting `moveToTop()`: the parent went from Z index 10 to the top, its
  child stayed below an instance created after it]

- *Set color* is a tint: it multiplies each channel of the image by the
  colour, and white restores the original. A part drawn in white takes the
  colour exactly, and black outlines stay black. But white highlights take the
  tint too. So draw a piece coloured by level with a white fill, and its
  highlights on a separate child that keeps its colour. [manual:
  plugin-reference/common-features/common-actions.md "Set color"; observed in
  a game project, r503 preview, 2026-09-29]

- When a hierarchy is created, the order of its instances' *On created* is
  not fixed. In one instance's *On created*, the others may not have run
  theirs yet, so code there cannot rely on how the rest of the hierarchy is
  set up. *On hierarchy ready* fires on the root once every instance of the
  hierarchy is created and has run *On created*. Initialise the hierarchy
  there. [manual: plugin-reference/common-features/common-conditions.md "On
  hierarchy ready"; scripting-reference/object-interfaces/iworldinstance.md
  "hierarchyready"; none of the 524 official examples uses the condition]
