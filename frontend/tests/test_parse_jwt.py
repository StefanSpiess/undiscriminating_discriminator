import subprocess  # nosec B404
from pathlib import Path


def test_node_parse_jwt():
    script = Path(__file__).resolve().parents[1] / "test_parse_jwt.js"
    result = subprocess.run(  # nosec B607 B603
        ["node", str(script)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr  # nosec B101
