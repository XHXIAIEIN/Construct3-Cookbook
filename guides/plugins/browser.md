# Event Sheet Pitfalls: Browser

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- These actions ask the browser for something it grants only just after the
  player touches, clicks or presses a key: *Request fullscreen*, *Request
  install*, *Request permission* (Touch), *Request wake lock*, *Request
  pointer lock*, *Share*, the clipboard's paste requests, the File chooser's
  *Click*, the File System pickers, a Bluetooth device request, screen
  recording, speech recognition and Google Play *Sign in*. In *On start of
  layout* or on a timer the browser refuses *Request fullscreen*, and *On
  fullscreen error* fires. Put each in an event with an *On tap*, *On click*,
  *On key pressed* or form control trigger, such as a fullscreen button, or in
  a function such an event calls. The `construct3-agent-plugin` skill's
  `check_project.py` warns if one has no touch, mouse, keyboard or form
  control condition in its event or above it. *Request MIDI access* is the
  exception. Some browsers allow it on startup, so the MIDI examples ask there
  and offer a button for a second try. [manual: plugin-reference/browser.md
  "Request fullscreen", "On fullscreen error", "Request install"; touch.md
  "Request permission"; platform-info.md "Request wake lock"; mouse.md
  "Request pointer lock"; share.md; clipboard.md; file-chooser.md "Click";
  filesystem.md; bluetooth.md; bbc-micro-bit.md; video-recorder.md;
  speech-recognition.md; google-play.md "Sign in"; midi.md; example:
  midi-input, event 2]

- A web export looks for an update only when the page loads, so a tab left
  open never sees a deploy. On each navigation its service worker fetches
  `offline.json` and downloads a newer version in the background. It posts *On
  update found* and *On update ready* about 3 seconds later. *Reload*, like
  the player's own refresh, switches to the new files only while no other tab
  of the game is open. In *On update ready*, ask the player to reload. To test
  it, deploy the new version, then load the old version once. [manual:
  plugin-reference/browser.md "On update ready", "Reload"; runtime: exported
  sw.js, `UpdateCheck` runs from the `fetch` handler for `navigate` requests,
  `PostBroadcastMessage` delays 3000 ms, `GetCacheNameToUse` keeps the old
  cache while `clients.matchAll()` finds more than one; r503 export,
  2026-09-28]

- An *On update ready* that reloads the page by itself can reload it in a
  loop. While another tab of the game is open, the reload starts the old
  version again, which finds the same update and fires *On update ready*
  once more. Mark the reload in the URL: set the hash to `updated` with
  *Set hash*, then *Reload*. In *On start of layout*, a `Browser.Hash` of
  `#updated` means the page came from that reload, so record it in a
  variable and clear the hash. When *On update ready* fires with the record
  set, ask the player to reload instead. [manual:
  plugin-reference/browser.md "Set hash" (does not reload the page),
  "Hash" (includes the `#`); derived from the cache rule of the entry
  above; the guard written so in a game project, r503, 2026-09-28, where
  the loop was not reproduced]

- In a project with the Browser object, the browser's own install banner
  never shows. On every page load the Browser object calls
  `preventDefault()` on `beforeinstallprompt` and holds the event for
  *Request install*. Chrome then logs "Banner not shown:
  beforeinstallpromptevent.preventDefault() called", which is not an error.
  To offer installing, show the game's own button once *On install
  available* fires, and call *Request install* from it. [manual:
  plugin-reference/browser.md "On install available", "Request install";
  runtime: exported main.js r504, the Browser DOM handler's
  `beforeinstallprompt` listener; observed on a game project's web export in
  Chrome, 2026-10-02]
