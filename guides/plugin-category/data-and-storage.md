# Event Sheet Pitfalls: Data & storage plugins

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

- Android and iOS (Cordova) exports are not in the plugin's support list,
  and the WKWebView extension covers macOS only. So treat File System as
  unavailable there. Save with Local Storage, and hand a file to the user
  with Share's *Add file*, because *Invoke download* does not work in a
  mobile app. Enable each route by its own condition, as taking-screenshots
  does with *Is sharing files supported* and *Is supported*. This is not
  verified on a device. [manual: plugin-reference/filesystem.md
  "Browser/platform support"; plugin-reference/browser.md "Invoke download";
  example: taking-screenshots]
