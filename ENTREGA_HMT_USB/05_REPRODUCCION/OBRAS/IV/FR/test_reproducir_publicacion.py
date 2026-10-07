"""Fast validator tests; no TeX process, original source, or historical receipt."""
import tempfile
from pathlib import Path
import unittest
from reproducir_publicacion import (
    validate_fls, validate_log, source_graph, clean_environment, LUAOTFLOAD_CONFIG,
)


class PublicationValidatorTests(unittest.TestCase):
    def test_fresh_font_database_is_limited_to_texmf(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            env = clean_environment(work, 946684800)
            conf = Path(env["XDG_CONFIG_HOME"]) / "luaotfload" / "luaotfload.conf"
            self.assertEqual(conf.read_text(encoding="utf-8"), LUAOTFLOAD_CONFIG)
            self.assertIn("location-precedence = texmf", LUAOTFLOAD_CONFIG)
            self.assertIn("scan-local = false", LUAOTFLOAD_CONFIG)
            self.assertEqual(list(Path(env["OSFONTDIR"]).iterdir()), [])
            self.assertEqual(env["SOURCE_DATE_EPOCH"], "946684800")

    def test_clean_log_and_underfull_are_distinguished(self):
        report = validate_log("Output written on main.pdf (2 pages).\nUnderfull \\hbox\n")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["underfull_hbox"], 1)

    def test_failures_are_not_suppressed(self):
        log = ("LaTeX Warning: Reference 'absent' on page 2 undefined.\n"
               "LaTeX Warning: Label 'same' multiply defined.\n"
               "Overfull \\hbox (1.0pt too wide)\n"
               "Overfull \\vbox (2pt too high)\nMissing character: U+1234\n"
               "! Undefined control sequence.\n"
               "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.\n")
        report = validate_log(log)
        self.assertTrue(all(report["blocking"].values()), report)

    def test_recorder_closure_and_rejected_external_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root, work, runtime = base / "package", base / "package/output/tex", base / "texlive"
            work.mkdir(parents=True)
            runtime.mkdir()
            (root / "main.tex").write_text("source", encoding="utf-8")
            (runtime / "article.cls").write_text("runtime", encoding="utf-8")
            private = base / "private.tex"
            private.write_text("not packaged", encoding="utf-8")
            good = ("PWD " + str(root) + "\nINPUT ./main.tex\nINPUT " +
                    str(runtime / "article.cls") + "\nOUTPUT " + str(work / "main.log"))
            report = validate_fls(good, root, root, work, [runtime], ["main.tex"])
            self.assertEqual(report["errors"], [], report)
            bad = good + "\nINPUT " + str(private) + "\nOUTPUT " + str(root / "main.aux")
            report = validate_fls(bad, root, root, work, [runtime], ["main.tex", "missing.tex"])
            self.assertEqual(len(report["errors"]), 3, report)

    def test_literal_graph_follows_only_active_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.tex").write_text("% \\input{absent}\n\\input{child}\n", encoding="utf-8")
            (root / "child.tex").write_text("body", encoding="utf-8")
            report = source_graph(root, root / "main.tex")
            self.assertEqual(report["errors"], [])
            self.assertEqual(set(report["files"]), {"main.tex", "child.tex"})


if __name__ == "__main__":
    unittest.main()
