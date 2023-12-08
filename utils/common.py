from functools import wraps
from inspect import signature
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


def abort_on_failure(text: str = "Непредвиденная ошибка: {}", exception=Exception, format_with_args: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except exception as e:
                if format_with_args:
                    info = signature(func).bind(*args, **kwargs).arguments
                    cli_exception(text.format(**info))

                else:
                    cli_exception(text)

        return wrapper

    return decorator


def format_bytes(size: int) -> Tuple[int, str]:
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G"}
    while size > power:
        size /= power
        n += 1
    return f"{int(size)} {power_labels[n]}B"
