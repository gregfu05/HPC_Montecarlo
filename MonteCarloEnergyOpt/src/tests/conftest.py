"""Configure test environment for package imports."""

import sys
from pathlib import Path


def _ensure_repo_root_on_path() -> None:
    """Prepend repository root so `import src` works when running pytest from repo root."""
    repo_root = Path(__file__).resolve().parents[2]
    root_str = str(repo_root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


_ensure_repo_root_on_path()
