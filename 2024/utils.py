import sys
import time
from contextlib import contextmanager
from pathlib import Path

DATA_DIR = Path(__file__).parent

def read_input(day: int) -> str:
    with open(DATA_DIR / f"day{day}/input.txt", encoding="utf-8") as f:
        return f.read()


@contextmanager
def timer():
    time_start = time.perf_counter()
    try:
        yield
    finally:
        print(f"[{time.perf_counter() - time_start:.3f} seconds]", file=sys.stderr)
