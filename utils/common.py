from os import PathLike
from os.path import expanduser
from typing import Tuple

LOCAL = True


def userpath(path: str) -> PathLike:
    if LOCAL:
        return path.replace("~", ".")
    else:
        return expanduser(path)


def cli_exception(reason):
    print(reason)
    exit(code=1)


def format_bytes(size: int) -> Tuple[int, str]:
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G"}
    while size > power:
        size /= power
        n += 1
    return f"{int(size)} {power_labels[n]}B"
