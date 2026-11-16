import plistlib, subprocess, sys, pathlib, unittest, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build_shortcuts as bs, make_fixtures, verify_clean
from PIL import Image


class Fixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        make_fixtures.main()
        cls.fx = ROOT / "fixtures"

    def test_oracle_catches_every_leaky_fixture(self):
        for n in ("leaky.jpg", "leaky_rotated.jpg", "leaky_tiny.jpg", "leaky.png"):
            self.assertTrue(verify_clean.leaks(str(self.fx / n)), n)

    def test_oracle_catches_gps_and_dates_specifically(self):
        l = " ".join(verify_clean.leaks(str(self.fx / "leaky.jpg")))
        for w in ("GPS", "DateTimeOriginal", "Model", "Make"):
            self.assertIn(w, l)

    def test_oracle_passes_clean(self):
        self.assertEqual(verify_clean.leaks(str(self.fx / "clean.jpg")), [])

    def test_pillow_strip_is_detected_clean(self):
        # Simulates what Convert Image (Preserve Metadata off) must achieve.
        im = Image.open(self.fx / "leaky.jpg")
        out = pathlib.Path(tempfile.mkdtemp()) / "o.jpg"
        Image.frombytes(im.mode, im.size, im.tobytes()).save(out)
        self.assertEqual(verify_clean.leaks(str(out)), [])


class Builder(unittest.TestCase):
    def test_every_shortcut_is_valid_plist_with_unique_uuids(self):
        for fn in bs.ALL:
            sc = fn()
            d = plistlib.loads(sc.dumps())
            ids = [a["WFWorkflowActionParameters"]["UUID"] for a in d["WFWorkflowActions"]]
            self.assertEqual(len(ids), len(set(ids)), sc.name)

    def test_every_share_path_scrubs_without_preserving_metadata(self):
        for fn in bs.ALL:
            sc = fn()
            conv = [a for a in sc.actions if a["WFWorkflowActionIdentifier"].endswith("image.convert")]
            if sc.name == "Poof Peek":
                self.assertFalse(conv); continue
            self.assertEqual(len(conv), 1, sc.name)
            self.assertIs(conv[0]["WFWorkflowActionParameters"]["WFImagePreserveMetadata"], False)

    def test_output_actions_use_cleaned_output_not_raw_input(self):
        for fn in (bs.poof_and_share, bs.poof_latest, bs.poof_pick):
            sc = fn()
            conv_uuid = next(a for a in sc.actions if a["WFWorkflowActionIdentifier"].endswith("image.convert"))["WFWorkflowActionParameters"]["UUID"]
            for a in sc.actions:
                if a["WFWorkflowActionIdentifier"].endswith(("share", "setclipboard")):
                    inp = a["WFWorkflowActionParameters"]["WFInput"]["Value"]
                    self.assertEqual(inp["OutputUUID"], conv_uuid, sc.name)

    def test_share_sheet_flags(self):
        d = plistlib.loads(bs.poof_and_share().dumps())
        self.assertEqual(d["WFWorkflowTypes"], ["ActionExtension"])
        self.assertEqual(d["WFWorkflowInputContentItemClasses"], ["WFImageContentItem"])
        self.assertEqual(plistlib.loads(bs.poof_latest().dumps())["WFWorkflowTypes"], [])

    @unittest.skipUnless(__import__("shutil").which("shortcuts"), "needs macOS shortcuts CLI")
    def test_signing(self):
        paths = bs.build(sign=True)
        for p in paths:
            self.assertEqual(p.read_bytes()[:4], b"AEA1", p.name)


if __name__ == "__main__":
    unittest.main()
