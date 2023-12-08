from math import ceil
from typing import Generator

from paramiko import Channel
from rich.progress import track
from typer import Option, run
from typing_extensions import Annotated, Optional

from utils import Config, connect, get_image
from utils.common import format_bytes

config = Config()


def send(host: str, image: str) -> None:
    channel: Channel = connect(host)

    image = get_image(image)
    image_size = image.__dict__["attrs"]["Size"]
    image_stream: Generator = image.save(named=True)
    total = ceil(image_size / 32768)

    channel.set_combine_stderr(True)
    channel.exec_command("docker load")

    for chunk in track(
        image_stream,
        description=f"Отправляем [bold blue]{format_bytes(image_size)}[/] на сервер [bold blue]{host}[/]:     ",
        total=total,
    ):
        channel.sendall(chunk)

    channel.shutdown_write()

    r = channel.recv(640 * 10)
    status = channel.recv_exit_status()

    if status != 0:
        raise Exception("Ошибка на сервере:  " + r.decode("utf-8"))


def main(
    image: str,
    host: Annotated[Optional[str], Option("-h", "--host")] = config["default"],
) -> None:
    send(host, image)


if __name__ == "__main__":
    run(main)
