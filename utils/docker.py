from docker import DockerClient
from docker import from_env as get_docker
from docker.models.images import Image
from docker.errors import ImageNotFound, DockerException

from .common import abort_on_failure, cli_exception


@abort_on_failure("Не удалось подключиться к докеру\nПроверьте, запущен ли Docker Desktop?", DockerException)
def setup_docker() -> DockerClient:
    return get_docker()


@abort_on_failure('Образ "{image}" не найден!', ImageNotFound, format_with_args=True)
def get_image(image: str) -> Image:
    return docker.images.get(image)


@abort_on_failure(exception=DockerException)
def build_image(*args, **kwargs) -> Image:
    return docker.images.build(*args, **kwargs)


if __name__ != "__main__":
    docker: DockerClient = setup_docker()
