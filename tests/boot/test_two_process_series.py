"""The shipped CLI playing a whole series, as two real OS processes.

This is the proof no in-process harness can give: each side's own command line
boots, exchanges Step-0 over real HTTP, plays `g01`...`g06`, writes its fourteen
official artifacts and exits 0. Three defects the in-process proof had hidden
were found exactly here.
"""

import json
from pathlib import Path

import executable_evidence as evidence
import executable_outcome as outcome
import executable_process as process
import pytest
from boot_builders import SECRET, free_port

from mars777_thief.app.sealed_record_values import ActorRole

GAMES = 6
FILES = 14
DEADLINE = (30, 60)
"""The negotiated response and watchdog bounds a normal series locks.

Read back from the artifact rather than trusted from the fixture: an agent that
shipped one deadline and locked another would still write a config file, and
this is the file both sides then hold each other to.
"""


def _finish(child: "process.subprocess.Popen[str]", timeout: float) -> tuple[int, str, str]:
    try:
        out, err = child.communicate(timeout=timeout)
    finally:
        if child.poll() is None:
            child.kill()
            child.communicate(timeout=10)
    return child.returncode, out, err


def locked_deadline(root: Path) -> tuple[int, int]:
    """What the official g01 config says the two sides actually locked."""
    name = next(one for one in evidence.official(root) if one.startswith("config_"))
    document = json.loads((root / name).read_text(encoding="utf-8"))
    terms = document["config"]["network_and_league"]
    return terms["response_timeout_sec"], terms["watchdog_timeout_sec"]


def _roots(tmp_path: Path) -> tuple[Path, Path]:
    ours, theirs = tmp_path / "mars777", tmp_path / "opponent"
    ours.mkdir()
    theirs.mkdir()
    return ours, theirs


@pytest.mark.windows_known_limitation
def test_the_real_cli_plays_a_whole_series_against_a_non_counted_opponent(tmp_path: Path) -> None:
    """One full exact-six autonomous series, both sides real OS processes.

    Marked because this pair reproducibly stalls on native Windows and nowhere
    else; see `docs/architecture/CONCURRENCY_MODEL.md`. The mark selects the
    test out of the *gating* Windows suite and into a visible non-gating job -
    it is fully gating on Linux, where it passes, and it is not an `xfail`,
    because a failure here must stay a failure that someone reads.
    """
    ours_port, theirs_port = free_port(), free_port()
    ours_root, theirs_root = _roots(tmp_path)
    launch = process.written_launch(tmp_path)
    environment = process.environment(
        ours_port, root=ours_root, opponent=f"http://{process.HOST}:{theirs_port}/mcp"
    )
    child = process.spawn("mars777_thief", launch, environment)
    opponent = process.spawn_opponent(
        ActorRole.POLICE.value, theirs_port, f"http://{process.HOST}:{ours_port}/mcp", theirs_root
    )
    try:
        assert outcome.await_application(child, ours_port) == process.NOT_ACCEPTABLE
        status, out, err = _finish(child, timeout=600)
        peer_status, _, peer_err = _finish(opponent, timeout=120)
    finally:
        for one in (child, opponent):
            if one.poll() is None:
                one.kill()
                one.communicate(timeout=10)

    assert status == 0, err
    assert peer_status == 0, peer_err
    assert child.pid != opponent.pid
    assert not outcome.crashed(err), err
    assert SECRET not in out and SECRET not in err
    assert f"{FILES} artifacts" in out

    for root in (ours_root, theirs_root):
        names = evidence.official(root)
        assert locked_deadline(root) == DEADLINE
        assert len(names) == FILES == len(set(names))
        assert sum(name.startswith("declaration_") for name in names) == 1
        assert sum(name.startswith("result_") for name in names) == 1
        for family in ("config_", "log_"):
            got = sorted(name for name in names if name.startswith(family))
            assert len(got) == GAMES
            assert all(f"_g0{index}." in name for index, name in enumerate(got, start=1))

    for log in sorted(path for path in ours_root.iterdir() if path.name.startswith("log_")):
        document = json.loads(log.read_text(encoding="utf-8"))
        assert document["audit"]["semantic"]["verdict"] == "CONSISTENT"
    result = json.loads((ours_root / evidence.official(ours_root)[-1]).read_text(encoding="utf-8"))
    assert result["mutual_agreement"]
