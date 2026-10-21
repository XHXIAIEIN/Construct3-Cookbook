# Event Sheet Pitfalls: File system

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

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
