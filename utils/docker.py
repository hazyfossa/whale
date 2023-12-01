from docker import DockerClient
from docker import from_env as get_docker
from docker.models.images import Image
from docker.errors import DockerException

from .common import cli_exception


def setup_docker() -> DockerClient:
    try:
        return get_docker()
    except DockerException:
        cli_exception(
            "Не удалось подключиться к докеру\nПроверьте, запущен ли Docker Desktop?"
        )


def get_image(image: str) -> Image:
    try:
        return docker.images.get(image)
    except DockerException:
        cli_exception(f"Образ {image} не найден!")


if __name__ != "__main__":
    docker = setup_docker()
