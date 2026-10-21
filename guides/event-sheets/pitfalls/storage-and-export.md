# Event Sheet Pitfalls: Storage and export

Sources and the rule for adding an entry are in the index,
[pitfalls/README.md](README.md).

- A web export checks for an update only when the page loads, so a tab
  that stays open never finds a later deploy. On each navigation, the
  export's service worker fetches `offline.json` and downloads a newer
  version in the background. About 3 seconds later, it posts *On update
  found* and *On update ready*. *Reload* switches to the new files only
  while no other tab of the game is open, and the player's own refresh
  does the same. In *On update ready*, ask the player to reload. To test
  this, deploy the new version, then load the old version once. [manual:
  plugin-reference/browser.md "On update ready", "Reload"; runtime: exported
  sw.js, `UpdateCheck` runs from the `fetch` handler for `navigate` requests,
  `PostBroadcastMessage` delays 3000 ms, `GetCacheNameToUse` keeps the old
  cache while `clients.matchAll()` finds more than one; r503 export,
  2026-09-28]
- If *On update ready* reloads the page by itself, the page can reload in
  a loop. While another tab of the game is open, the reload starts the old
  version again. That version finds the same update and fires *On update
  ready* once more. To prevent the loop, mark the reload in the URL: set
  the hash to `updated` with *Set hash*, then *Reload*. In *On start of
  layout*, a `Browser.Hash` of `#updated` means that the page comes from
  that reload. So record this in a variable, and clear the hash. If *On
  update ready* fires while the variable is set, ask the player to reload
  instead. [manual:
  plugin-reference/browser.md "Set hash" (does not reload the page),
  "Hash" (includes the `#`); derived from the cache rule of the entry
  above; the guard written so in a game project, r503, 2026-09-28, where
  the loop was not reproduced]
- In a project with the Browser object, the browser's own install banner
  never shows. On every page load, the Browser object calls
  `preventDefault()` on `beforeinstallprompt` and keeps the event for
  *Request install*. Chrome then logs "Banner not shown:
  beforeinstallpromptevent.preventDefault() called". This message is not
  an error. To offer installation, show the game's own button when *On
  install available* fires, and call *Request install* from that button.
  [manual:
  plugin-reference/browser.md "On install available", "Request install";
  runtime: exported main.js r504, the Browser DOM handler's
  `beforeinstallprompt` listener; observed on a game project's web export in
  Chrome, 2026-10-02]
- File System writes only through a picker tag, never to a free path. The
  known folder tags (`<documents>`, `<desktop>`, `<saved-games>`, ...)
  exist only in the Windows WebView2, macOS WKWebView and Linux CEF
  exports. In preview and in a browser, *Has picker tag* is false for all
  of these tags. Test the plugin's own conditions in this order: *Desktop
  features supported*, *Has picker tag*, then *Is supported*. Give each
  branch its fallback. Do not test the OS with Platform Info, because
  Chrome on Windows reports Windows and still has no known folders.
  [manual: plugin-reference/filesystem.md "Accessing known folders";
  construct.net tutorial "Exporting to Windows with the WebView2 wrapper"]
- No tag names the Construct project folder. `<app>` and `<web-resource>`
  are the exported executable's folder and its `www`, and they can be
  read-only, for example under Program Files. Save to
  `<current-app-data>`, or to `<saved-games>` on Windows only. macOS and
  Linux do not support `<saved-games>`, `<screenshots>` and
  `<roaming-app-data>`. If the macOS App Sandbox is on, the known folders
  are the app's container, not the user's Finder folders.
  [manual: plugin-reference/filesystem.md "Known folders table", "macOS App
  Sandbox"]
- In a browser, the plugin needs desktop Chromium, not Firefox or Safari.
  A picker opens only in a user input trigger. A second write to a file
  that was opened earlier prompts for permission. A save picker erases the
  chosen file, so write to it with folder path "" and do not read it.
  *Start in* sets only the folder that the dialog opens at. The picker tag
  persists across sessions. So if *Has picker tag* is true at start, a
  *Save* button can rewrite the same file without a dialog. [manual:
  plugin-reference/filesystem.md "Browser
  permissions model", "Show save file picker"; example:
  file-system-text-editor]
- The plugin's support list leaves out Android and iOS (Cordova) exports,
  and the WKWebView extension covers only macOS. So treat File System as
  unavailable on these platforms, and save with Local Storage. To hand a
  file to the user, use Share's *Add file*, because *Invoke download* does
  not work in a mobile app. Enable each route with its own condition, as
  the taking-screenshots example does with *Is sharing files supported*
  and *Is supported*. This entry is not verified on a device. [manual:
  plugin-reference/filesystem.md
  "Browser/platform support"; plugin-reference/browser.md "Invoke download";
  example: taking-screenshots]
- The JSON plugin has no action that merges one object into another, so
  copy the keys one at a time. *Set JSON* sets one key from a JSON string,
  and `GetAsCompactString(path)` reads one key as such a string. So if a
  large data file is split into several files that the events still read
  through one JSON object, parse each file into a second JSON object,
  `Part`. Then run *For each* on its path `""`, and in the main object *Set
  JSON* at `Part.CurrentKey` to `Part.GetAsCompactString(Part.CurrentKey)`.
  The paths that the events read stay the same if no two files share a
  top-level key. If two files share one, the later file overwrites it.
  Several AJAX requests can share one tag. Each request sets `LastData` to
  its own response and then fires *On completed* for that tag. This
  happens once per request, in the order that the responses arrive. So
  request all files in one block, and count them in a variable. Merge each
  file in *On completed*, and start the game in a sub-event when the count
  reaches 0.
  [manual: plugin-reference/json.md "For each", "Set JSON", "CurrentKey",
  "GetAsCompactString"; schema: plugins/json.json, no merge action; runtime:
  exported c3runtime.js r504, AJAX `onreadystatechange` sets `_lastData`
  and then calls `_TriggerComplete` for each request, `OnComplete` compares
  the tag; observed in a game project, r504, 2026-10-06: four data files
  requested with one tag, merged this way before the first level]
