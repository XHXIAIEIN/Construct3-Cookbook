# Observations Name the Release They Were Made On

Date: 2026-10-30
Data: Construct3-RAG r506.3

## Problem

An entry describes the current stable release of Construct 3. An entry
that a stable release fixed is rewritten or deleted (`AGENTS.md`,
"Construct 3 releases"). An observation records how the runtime behaved on
the release it ran on, so its page can read as current after the behaviour
changed. The check must therefore find the observations that name no
release, and the sources that nobody repeated on a newer stable release.

The check must also find the source itself. A check that accepts any
bracketed span that is not a link's text passes the "[0, 1]" of "clamp the
value in [0, 1]" as the source of an entry that has none.

## Evidence

A count over every source in `guides/`, with the Construct3-RAG data at
r506.3, found 181 sources that hold 195 observations. The table gives each
source's newest observed release:

| Newest observed release | Sources |
|-------------------------|---------|
| None | 45 |
| r495.2 | 11 |
| r502 | 2 |
| r503 | 12 |
| r504 | 61 |
| r505 | 9 |
| r506 | 2 |
| r506.2 | 12 |
| r506.3 | 27 |

So 109 sources were last observed before r506.3, and 47 observations name
no release. Of the 47, 17 name the editor's preview without its release,
such as "stable editor preview", and 2 carry no date either.

The date of an observation does not give its release. The observations
dated 2026-10-14 name r495.2, r504, r505, an r505 beta and r506, so the
projects of one day ran on five releases. A release filled in from the
date would be a guess, and the only fix for one of the 47 is to repeat its
probe.

Three observations were made in a browser and not in Construct: a test
page in Chrome 155, a canvas in Chrome 152 and an audio decode in Edge 155.
Their behaviour depends on the browser's version, which each one names.

## Options

For the observations without a release:

1. **Fail on every one.** CI fails on 47 observations at once, and none of
   them can be fixed without its probe.
2. **Warn on every one.** Nothing keeps a new entry from adding a 48th.
3. **Fail on the ones dated after this record, and warn on the older and
   the undated ones.** Chosen. A new observation names its release, and the
   47 stay listed until their probes are repeated.

For the sources last observed before the stable release:

1. **Fail on them.** CI fails on 109 sources, each of which needs a probe
   by hand in the editor, and every new stable release fails it again for
   every source observed before that release.
2. **List them as warnings.** Chosen.

## Decision

- An observation is a part of a source, between semicolons, that starts
  with "observed" or "observation". A part such as "not observed in play"
  starts otherwise, so it is not one.
- An observation names its release as `rNNN` or `rNNN.N`. An observation
  made outside Construct names the browser and its version instead, such as
  "Chrome 155".
- `scripts/check.py` fails on an observation that names neither and is
  dated after 2026-10-30, the date of this record. It counts the older and
  the undated ones as warnings.
- For each source, the check takes the newest release that its
  observations name. It compares that release with the `version` of the
  Construct3-RAG data. A release named by another part of the same
  brackets, such as `exported c3runtime.js r503`, does not count, because
  the warning lists behaviours to probe again, not code to read again.
- The check prints the two counts on every run. `python scripts/check.py
  --releases` lists each observation and each source with its file and
  line. Neither list changes the exit code.
- An entry's source is the bracketed span that the entry ends with, read
  after the code spans are removed. A bracketed span in the prose and a
  link's text are not a source. `scripts/test_check.py` holds the cases
  that the check must refuse, and CI runs it.

## Re-evaluate when

- The warnings for observations without a release reach 0: the check can
  then fail on every one and drop the date.
- A new entry adds an observation with neither a date nor a release: the
  date rule passes it as a warning, so the check must then require a date.
- A browser version stands for the release of a Construct project, as in
  "a game project's export in Chrome 155": the browser rule then hides a
  missing release, and must accept a browser only where no project ran.
