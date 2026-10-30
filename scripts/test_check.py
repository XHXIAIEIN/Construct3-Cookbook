"""Cases that check.py must refuse or accept.

    python -m unittest discover -s scripts
"""
import unittest

import check

STABLE = (506, 3)


def report(text: str) -> tuple[list[str], list[str], list[str]]:
    return check.release_report({"page.md": text}, STABLE)


class Source(unittest.TestCase):
    def test_prose_brackets_are_not_a_source(self):
        self.assertIsNone(check.source("- Clamp the value in [0, 1] before you set the opacity."))

    def test_source_after_prose_brackets(self):
        self.assertEqual(check.source("- Clamp it in [0, 1]. [manual: system-expressions.md]"),
                         "manual: system-expressions.md")

    def test_link_text_is_not_a_source(self):
        self.assertIsNone(check.source("- Read [the index](pitfalls.md)."))

    def test_brackets_in_code_are_not_a_source(self):
        self.assertIsNone(check.source("- Read `arr[0]` before the loop, not `arr[\n  i]`."))

    def test_source_holds_a_link(self):
        self.assertEqual(check.source('- A fact. [manual: [Tween](tween.md) "Value"]'),
                         'manual: [Tween](tween.md) "Value"')

    def test_open_bracket_closes_nothing_after_a_blank_line(self):
        plain = check.plain_prose("- A range [0, 1) of values. [manual: a]\n\n- Text [\n\n- B. [manual: b]")
        self.assertEqual([plain[s + 1:e] for s, e in check.brackets(plain)], ["manual: a", "manual: b"])


class Releases(unittest.TestCase):
    def test_observation_without_release_after_the_cutoff_fails(self):
        problems, unnamed, _ = report("- A fact. [observed in a game project, 2026-11-02]")
        self.assertEqual(problems, ["page.md:1: no release in 'observed in a game project, 2026-11-02'"])
        self.assertEqual(unnamed, [])

    def test_older_or_undated_observation_without_release_warns(self):
        problems, unnamed, _ = report("- A. [observed in a game project, stable editor preview, 2026-10-07]\n"
                                      "- B. [manual: a.md; observation in a studied project]")
        self.assertEqual(problems, [])
        self.assertEqual([w.split(":")[1] for w in unnamed], ["1", "2"])

    def test_release_or_browser_names_the_observation(self):
        self.assertEqual(report("- A. [observed in a probe project, r506.3 preview, 2026-11-02]\n"
                                "- B. [observed with a test page, Chrome 155, 2026-11-02]"), ([], [], []))

    def test_not_observed_is_no_observation(self):
        self.assertEqual(report("- A. [runtime: c3runtime.js r503, from source, not observed in play]"), ([], [], []))

    def test_newest_observed_release_is_older_than_stable(self):
        _, _, stale = report("- A fact.\n  [runtime: c3runtime.js r506.3;\n  observed in a minimal project,"
                             " r495.2 and r504 previews, 2026-10-14]")
        self.assertEqual(stale, ["page.md:3: last observed on r504"])

    def test_observation_on_stable_is_current(self):
        self.assertEqual(report("- A. [observed in a game project, r504, 2026-10-01; observed again in a probe"
                                " project, r506.3 preview, 2026-10-26]")[2], [])


if __name__ == "__main__":
    unittest.main()
