"""Tiny builder for Apple Shortcuts (.shortcut) property lists.

Keep ALL knowledge of Apple's undocumented keys in this file, so if Apple
renames something we fix it in exactly one place.
"""
from __future__ import annotations
import plistlib
import uuid as _uuid
from dataclasses import dataclass, field

PREFIX = "is.workflow.actions."

# Shortcut icon colours (WFWorkflowIconStartColor values)
COLORS = {"red": 4282601983, "purple": 3031607807, "blue": 463140863, "teal": 431817727,
          "pink": 3679049983, "green": 4251333119}
# Glyph numbers (sparkles-ish / photo / eye). Cosmetic only.
GLYPHS = {"sparkles": 59771, "photo": 59451, "eye": 59494, "bolt": 59420}


@dataclass
class Ref:
    """A reference to the output of an earlier action (a 'magic variable')."""
    uuid: str
    name: str

    def token(self) -> dict:
        return {"Value": {"Type": "ActionOutput", "OutputUUID": self.uuid,
                          "OutputName": self.name},
                "WFSerializationType": "WFTextTokenAttachment"}


SHORTCUT_INPUT = {"Value": {"Type": "ExtensionInput"},
                  "WFSerializationType": "WFTextTokenAttachment"}


def as_input(x):
    if isinstance(x, Ref):
        return x.token()
    return x


def text_with(*parts) -> dict:
    """Build a WFTextTokenString mixing literal strings and Refs."""
    s, attachments = "", {}
    for p in parts:
        if isinstance(p, Ref):
            attachments[f"{{{len(s)}, 1}}"] = {"Type": "ActionOutput",
                                               "OutputUUID": p.uuid,
                                               "OutputName": p.name}
            s += "￼"
        else:
            s += p
    return {"Value": {"string": s, "attachmentsByRange": attachments},
            "WFSerializationType": "WFTextTokenString"}


@dataclass
class Shortcut:
    name: str
    color: str = "purple"
    glyph: str = "sparkles"
    share_sheet: bool = False          # appear in Share Sheet for images
    actions: list = field(default_factory=list)

    def add(self, ident: str, params: dict | None = None, name: str = "") -> Ref:
        uid = str(_uuid.uuid4()).upper()
        p = dict(params or {})
        p["UUID"] = uid
        self.actions.append({"WFWorkflowActionIdentifier": PREFIX + ident,
                             "WFWorkflowActionParameters": p})
        return Ref(uid, name or ident)

    def to_plist(self) -> dict:
        d = {
            "WFWorkflowClientVersion": "2900.0.1",
            "WFWorkflowMinimumClientVersion": 900,
            "WFWorkflowMinimumClientRelease": 900,
            "WFWorkflowIcon": {"WFWorkflowIconStartColor": COLORS[self.color],
                               "WFWorkflowIconGlyphNumber": GLYPHS[self.glyph]},
            "WFWorkflowImportQuestions": [],
            "WFWorkflowTypes": ["ActionExtension"] if self.share_sheet else [],
            "WFWorkflowInputContentItemClasses": ["WFImageContentItem"],
            "WFWorkflowHasShortcutInputVariables": self.share_sheet,
            "WFWorkflowActions": self.actions,
        }
        return d

    def dumps(self) -> bytes:
        return plistlib.dumps(self.to_plist(), fmt=plistlib.FMT_BINARY)

    def write(self, path: str) -> None:
        with open(path, "wb") as f:
            f.write(self.dumps())
