from __future__ import annotations

from commet._shared import get_version


class TestVersion:
    def test_get_version_returns_installed_version(self) -> None:
        version = get_version()
        assert version == "0.3.0"

    def test_module_version_matches(self) -> None:
        import commet

        assert commet.__version__ == "0.3.0"
