# Event Sheet Pitfalls: Data & storage plugins

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../pitfalls.md).

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
