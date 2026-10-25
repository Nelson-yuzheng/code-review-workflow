import os
import subprocess


def read_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在：{path}")
    if os.path.isdir(path):
        raise IsADirectoryError(f"{path} 是一个目录，请指定具体文件")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def run_linter(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在：{path}")
    try:
        result = subprocess.run(
            ["pylint", path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except FileNotFoundError:
        return "错误：未安装 pylint，请先运行 pip install pylint"
    output = (result.stdout + result.stderr).strip()
    return output or "pylint 未发现问题。"
