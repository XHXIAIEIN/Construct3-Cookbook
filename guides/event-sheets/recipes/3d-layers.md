# Flat layers in depth and a camera around them

This page covers a scene of flat art set at different depths and seen from
an angle: a diorama, a pop-up book, a drawing whose strokes stand at
different distances, which the player tilts or circles. Design first with
[design/thinking.md](../design/thinking.md). This page expands that
file's row "flat art at different depths".

## What gives depth

- **A layer is a flat plane at its Z elevation.** Set it with the layer's
  *Z elevation* property, System *Set layer Z elevation* or
  `ILayer.zElevation`, and read it with `LayerZElevation(layer)`. A higher
  value moves the layer towards the default camera. A layer can turn in its
  own plane (`ILayer.angle`), but nothing tilts it about X or Y: the layer
  properties, the System actions and `ILayer` have no such rotation. For a
  tilted or curved sheet, give a Sprite a mesh and set a Z on each point
  with *Set mesh point* (mesh-z-elevation), or use a 3D Shape.
  [manual: project-primitives/layers.md "Z elevation"; schema
  `plugins/_common.json` `set-mesh-point`]
- **One object can stand at its own height** with *Set Z* (`set-z-elevation`)
  or `IWorldInstance.zElevation`, on top of its layer's Z. The
  top-down-jump example lifts its player this way.
- **Projection.** The layout's *Projection* is *Perspective* by default, so
  a plane further from the camera shows smaller. *Orthographic* keeps every
  plane the same size, and then the stack shows depth only through the
  camera's angle. System *Set layout projection* switches the projection
  at runtime (orthographic-projection). *Vanishing point* (System *Set
  layout vanishing point*, 0 to 100, 50 the middle) moves the point where
  distant planes converge. Under *Orthographic*, it does nothing.
  [manual: project-primitives/layouts.md "Projection", "Vanishing point"]
- **Rendering mode per layer.** The 3D Camera moves only the layers whose
  *Rendering mode* is *3D*. A *2D* layer ignores the camera and scrolls as
  usual. Put the HUD and a fixed backdrop on *2D* layers, because on a
  *3D* layer, content that rises higher can overlap them. The skill's
  template makes every layer *3D*, so set the HUD layer to *2D*. [manual:
  plugin-reference/3d-camera.md "Using a 3D Camera",
  project-primitives/layers.md "Rendering mode"]
- **Z axis scale.** A new project uses *Regular*, where Z has the scale of
  X and Y. The default camera Z then follows the viewport height and the
  field of view. So read it as `3DCamera.DefaultCameraZ` instead of
  writing 100, which is the value under the deprecated *Normalized* scale.
  [manual: plugin-reference/3d-camera.md "3D Camera properties",
  project-primitives/projects.md "Z axis scale"]

The official examples put depth on instances and 3D Shapes. Every layer in
them has a Z elevation of 0, and none calls *Set layer Z elevation*. So no
example shows a stack of raised layers. Check such a stack in a preview
before you build on it. [checked over the layouts and sheets of
Construct-Example-Projects, 2026-10-18]

## Spacing the layers

Seen from straight above at camera height `C`, a plane at height `z` shows
at `C / (C - z)` of its size. So a layer at half the camera's height shows
twice as large, and one at `-C` shows half as large. Keep the stack well
below the camera's Z, because a plane at or above the camera is behind it
and is not drawn. A plane nearer than the project's *Near distance* or
further than its *Far distance* is not drawn either. Space the layers as
shares of `DefaultCameraZ`, such as `-0.6`, `-0.3`, `0` and `0.3` of it,
because fixed numbers hold for one viewport only. [derived from the
perspective projection; manual: project-primitives/projects.md "Near
distance", "Far distance"]

## Circling the scene

*Rotate camera* is mouse look. It turns the direction that the camera
points in and leaves the camera where it is, so it cannot circle a scene.
To circle a scene, move the camera around a centre, and look at the
centre every tick. The back-face-culling example does this with an
invisible object that has the Orbit behavior. *Every tick*, it runs
`3DCamera: Look at position` with the camera at
`(CameraPos.X, CameraPos.Y, 300)`, the look position at the scene's centre
at Z 0, and the up vector `(0, 0, 1)`. So the camera turns around the
scene by itself, as a tour that plays without input. [manual:
plugin-reference/3d-camera.md "Rotate camera"; back-face-culling]

To let the player drag the view, keep three numbers: `Yaw`, the compass
direction of the camera from the centre; `Tilt`, its angle from straight
above; and `Distance`. `sin` and `cos` take degrees.

1. Mouse *On movement* with *Mouse button is down* `left`: add
   `Mouse.MovementX * 0.3` to `Yaw`, and set `Tilt` to
   `clamp(Tilt - Mouse.MovementY * 0.3, 5, 80)`.
2. Mouse *On mouse wheel* `up`: set `Distance` to
   `clamp(Distance - 50, NEAR, FAR)`; *On mouse wheel* `down`: the same with
   `+ 50`.
3. *Every tick*, `3DCamera: Look at position` with the camera at
   `cx + Distance * sin(Tilt) * cos(Yaw)`,
   `cy + Distance * sin(Tilt) * sin(Yaw)`,
   `cz + Distance * cos(Tilt)`, the look position at `(cx, cy, cz)`, and up
   vector `(0, 0, 1)`. `cz` is the middle of the stack.

Keep `Tilt` above 0. At 0 the camera is straight above and looks along its
up vector, and that breaks its orientation. The manual gives the same
reason to keep the polar angles of *Rotate camera* off 0 and 180. Keep
`Tilt` below 90, because at 90 the camera is level with the stack and sees
the layers edge on. Start `Distance` at `DefaultCameraZ`, so that the
first frame shows the layout at about its 2D size. [derived from *Look at
position* and back-face-culling; not yet observed in a preview]

In a script, call the camera's methods on the object type, not on an
instance:
`runtime.objects["3DCamera"].lookAtPosition(camX, camY, camZ, lookX, lookY, lookZ, 0, 0, 1)`.
The name starts with a digit, so index it with quotes. [schema:
`I3DCameraObjectType`]

## Not this

| The draft has | Why it is wrong | Replace with |
|---------------|-----------------|--------------|
| *Rotate camera* fed by a drag to circle the scene | It turns the view around the camera | *Look at position* from `Yaw`, `Tilt` and `Distance` |
| A layer tilted to face the camera | Layers do not tilt | A mesh with a Z on each point, or a 3D Shape |
| Layer Z values typed for one screen size, at or above the camera | The default camera Z follows the viewport and the field of view, and a plane at or above the camera is not drawn | Values as shares of `DefaultCameraZ` |
| The HUD on a *3D* layer | The camera moves it, and raised content can cover it | *Rendering mode* *2D* on the HUD layer |
