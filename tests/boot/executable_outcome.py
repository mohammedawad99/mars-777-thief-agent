"""How a real process ended, judged from outside it.

A finished run is an exit status, two streams and a duration, and the questions
worth asking of it are narrow: did it stop cleanly, did it crash, which status
wins when two processes disagree, and did the one we are waiting for reach the
point we are waiting for. Nothing here starts anything.
"""

import http.client
import subprocess
import time

from boot_builders import HOST
from executable_process import CONNECTION_REPORT, FAILURE, MCP_PATH, POLL_SECONDS, READY_TIMEOUT


def crashed(err: str) -> bool:
    """True when *err* names an exception that is not a connection report."""
    for line in err.splitlines():
        found = FAILURE.match(line)
        if found and not any(known in line for known in CONNECTION_REPORT):
            return True
    return False


def await_application(child: "subprocess.Popen[str]", port: int) -> int:
    """Return the status of the first HTTP response the **application** produced.

    A TCP connect proves nothing: R6 binds and listens itself, so the kernel
    accepts into the backlog while no server exists and holds the request
    unanswered - which is the window that made CI red. Only a parsed status line
    proves the ASGI stack is running.
    """
    deadline = time.monotonic() + READY_TIMEOUT
    while time.monotonic() < deadline:
        if child.poll() is not None:
            raise AssertionError(f"the agent exited early: {child.communicate()[1]}")
        connection = http.client.HTTPConnection(HOST, port, timeout=1.0)
        try:
            connection.request("GET", MCP_PATH)
            return int(connection.getresponse().status)
        except (OSError, http.client.HTTPException):
            time.sleep(POLL_SECONDS)
        finally:
            connection.close()
    raise AssertionError("the agent never answered an HTTP request")
