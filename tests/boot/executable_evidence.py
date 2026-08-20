"""What a finished run left behind, read back and reported safely.

Artifacts on disk, log lines, and a two-process report an operator could paste
into a review - with the pre-shared secret scrubbed out of it, because a
diagnostic that leaks key material is worse than no diagnostic at all.
"""

from pathlib import Path

from boot_builders import SECRET
from executable_process import CONTROL_EXIT, GRACEFUL_MARKERS, WINDOWS


def official(root: Path) -> list[str]:
    """The official file names a finished side left behind, sorted."""
    return sorted(path.name for path in root.iterdir()) if root.exists() else []


def assert_clean_operator_stop(status: int, out: str, err: str, windows: bool = WINDOWS) -> None:
    """Assert the stop was clean under *this platform's* contract.

    POSIX is exactly 0 - a control-event status there would be a real failure.
    Windows delivers `CTRL_BREAK_EVENT` through the console, which terminates the
    process on its own terms after the handlers run, so the status alone cannot
    tell a graceful shutdown from a kill; the server's own shutdown record is
    what does, and 3 is refused without it.
    """
    assert "Traceback" not in err, err
    assert SECRET not in out and SECRET not in err
    if not windows:
        assert status == 0, err
        return
    assert status in {0, CONTROL_EXIT}, err
    missing = [marker for marker in GRACEFUL_MARKERS if marker not in err]
    assert not missing, f"status {status} without a complete shutdown, missing {missing}: {err}"
