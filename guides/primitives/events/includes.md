# Event Sheet Pitfalls: Event sheet includes

Sources and the rule for adding an entry are in the index,
[pitfalls.md](../../pitfalls.md).

- A function is called from any sheet, whether or not the layout runs the
  sheet that defines it. The triggers of a sheet, *On start of layout*,
  Timer *On timer*, AJAX *On completed*, run only while the running
  layout's sheet is that sheet or includes it; in any other sheet they do
  nothing and raise no error. So a sheet of shared functions needs no include, but
  a function that waits on a trigger of its own sheet, such as a request
  whose *On completed* lives beside it, needs that sheet included by every
  layout that calls it, or the response is never handled. [manual:
  project-primitives/events/functions.md "Functions are global";
  project-primitives/events/event-sheets.md "Layouts have an associated
  event sheet"; project-primitives/events/includes.md; observed in a minimal
  project, r506.2 preview, 2026-10-16: a function in a sheet no layout uses
  ran when the layout's sheet called it, the *On start of layout* of that
  sheet did not run, and the preview logged no error]
