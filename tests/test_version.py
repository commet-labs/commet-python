from __future__ import annotations

import re
from pathlib import Path

from commet._shared import get_version

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def _declared_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r'(?ms)^\[project\].*?^version\s*=\s*"([^"]+)"', text)
    assert match is not None, "could not find [project] version in pyproject.toml"
    return match.group(1)


DECLARED_VERSION = _declared_version()


class TestVersion:
    def test_get_version_matches_declared_version(self) -> None:
        assert get_version() == DECLARED_VERSION

    def test_module_version_matches_declared_version(self) -> None:
        import commet

        assert commet.__version__ == DECLARED_VERSION
