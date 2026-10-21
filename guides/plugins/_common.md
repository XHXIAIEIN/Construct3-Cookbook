# Event Sheet Pitfalls: Common to all objects

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- *Pick children* picks only among the instances of the child type that
  are already picked. If the child type is in the parent's container,
  narrowing the parent narrows the child type at the same time. For
  example, `PieceArt` is in `Piece`'s container. In `Piece: On drop`,
  `PieceArt` is already the art of the dragged piece. So `Pieces: Pick
  children PieceArt` finds nothing on the piece under it. Give the child
  type a family of its own, `Arts` with the one member `PieceArt`. Then
  pick children of the family, because its picks are kept apart from the
  container's. [runtime: exported
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

- A hierarchy child can be on a different layer from its parent, because
  the connection belongs to the instances, not to the layers. A child on a
  lower layer stays a child. So a lifted parent can draw above everything
  while its parts stay under an outline. [releases: beta.json, "hierarchy
  information not duplicated properly if connections were setup between
  instances in different layers"; observed in a game project, 2026-09-17;
  observed in a minimal project, r504 preview, 2026-10-02: a child on
  another layer than its parent kept the parent and moved 40 px with it]

- *ChildCount*, *Compare child count* and *Has children* count every
  attached child of any type. So a second child type on the same parent
  changes every count that meant one type. To get the top index of one
  type, use *Pick children* and then *Pick highest/lowest* (highest) on
  that type. Or count in a *For each* over the picked children.
  [manual: plugin-reference/common-features/common-expressions.md
  "ChildCount", common-conditions.md "Compare child count"; observed in a
  game project, 2026-09-17]

- *Set mesh point* in *Relative* mode adds to the current position of the
  point, not to its default position. So a derivation that runs every tick
  accumulates. Derive with *Absolute* and normalised coordinates, which
  run 0..1 across the object box and may go past it. A texture value of -1
  leaves the texture position unchanged. [manual:
  plugin-reference/common-features/common-actions.md "Set
  mesh point"]

- A mesh pulled into a trapezoid in X and Y bends every straight line of
  its image. Each cell draws as two triangles, and the image follows each
  triangle separately, so a line kinks where it crosses a diagonal. More
  points make the kinks shorter but never remove them. Also, rows spaced
  evenly show no depth. Moving the top points sideways gives a skew, a
  parallelogram. Pulling them in gives a trapezoid, which looks like a
  plane seen at an angle only with depth. For that plane, leave X and Y at
  their defaults and give the near row a Z with *Set mesh point*
  (mesh-z-elevation). Put the object on a layer whose *Rendering mode* is
  *3D*, under the layout's *Perspective* projection, as
  [3d-layers.md](../recipes/3d-layers.md) says. Then the lines stay
  straight and the rows get closer towards the far edge. A 2x2 mesh is
  enough for this. The raised row draws larger than the object box, so
  size or place the object for the tilted shape. [observed 2026-10-18 in a
  preview, r506.2
  editor, 778x511 viewport: on a Sprite with a 16x12 grid image, an 8x8
  mesh with its top row pulled in by 0.3 on each side drew zigzag lines and
  even rows; a 2x2 or 8x8 mesh with x and y at their defaults and z 600 on
  the bottom row drew straight lines and rows closer towards the top; manual:
  scripting/scripting-reference/object-interfaces/iworldinstance.md
  "setMeshPoint"]

- *Set width* stretches the whole image of a Sprite and repeats the image
  of a Tiled Background. On a 9-patch, it stretches or tiles the middle, and
  the corners keep their size. So make a bar with a painted fill a Tiled
  Background, because below its own width it shows a cut of the painting.
  Make a bar with caps a 9-patch, and keep its width positive. [manual:
  plugin-reference/tiled-background.md "display an image in a repeating
  pattern"; plugin-reference/9-patch.md "a Sprite object, which just stretches
  its entire image", "useful for representing things like progress bars";
  reference: recipes/progress-bars.md]

- *Move to top* moves only the instance that it runs on, and the children
  of a hierarchy keep their places in the Z order. So if the parent of a
  dragged piece goes to the top, the piece's body, face and label still draw
  under the pieces created after it. Pick the children with *Pick children*
  and move every part to the top, bottom part first, in the order that the
  parts must stack. [manual:
  plugin-reference/common-features/common-actions.md "Move to top", "top of
  its current layer"; observed in a game project, r503 preview, 2026-09-29;
  observed in a minimal project, r504 preview, 2026-10-02, through the
  scripting `moveToTop()`: the parent went from Z index 10 to the top, its
  child stayed below an instance created after it]

- *Set color* is a tint: it multiplies each channel of the image by the
  colour, and white restores the original. A part drawn in white takes the
  colour exactly, and black outlines stay black. But white highlights take
  the tint too. So if a piece is coloured by level, draw it with a white
  fill, and draw its highlights on a separate child that keeps its colour.
  [manual: plugin-reference/common-features/common-actions.md "Set color";
  observed in a game project, r503 preview, 2026-09-29]

- When a hierarchy is created, the order in which its instances run *On
  created* is not fixed. So in one instance's *On created*, the others may
  not have run theirs yet, and code there cannot rely on the setup of the
  rest of the hierarchy. *On hierarchy ready* fires on the root once every
  instance of the hierarchy is created and has run *On created*. Initialise
  the hierarchy there.
  [manual: plugin-reference/common-features/common-conditions.md "On
  hierarchy ready"; scripting-reference/object-interfaces/iworldinstance.md
  "hierarchyready"; none of the 524 official examples uses the condition]
