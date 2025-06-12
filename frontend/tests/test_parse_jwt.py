import subprocess
from pathlib import Path


def test_node_parse_jwt():
    script = Path(__file__).resolve().parents[1] / "test_parse_jwt.js"
    result = subprocess.run(["node", str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
