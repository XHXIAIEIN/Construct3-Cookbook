# Event Sheet Pitfalls: Event sheet includes

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

- Any sheet can call a function, whether or not the layout runs the sheet
  that defines it. But the triggers of a sheet, such as *On start of
  layout*, Timer *On timer* and AJAX *On completed*, run only while the
  running layout's sheet is that sheet or includes it. In any other sheet
  they do nothing and raise no error. So a sheet of shared functions needs
  no include. But if a function waits on a trigger of its own sheet, such
  as a request whose *On completed* is in the same sheet, every layout
  that calls the function must include that sheet, or the response is
  never handled. [manual:
  project-primitives/events/functions.md "Functions are global";
  project-primitives/events/event-sheets.md "Layouts have an associated
  event sheet"; project-primitives/events/includes.md; observed in a minimal
  project, r506.2 preview, 2026-10-16: a function in a sheet no layout uses
  ran when the layout's sheet called it, the *On start of layout* of that
  sheet did not run, and the preview logged no error]
