from common import abort_on_failure
from docker import DockerClient
from docker import from_env as get_docker
from docker.errors import DockerException, ImageNotFound
from docker.models.images import Image


@abort_on_failure("Не удалось подключиться к докеру\nПроверьте, запущен ли Docker Desktop?", DockerException)
def setup_docker() -> DockerClient:
    return get_docker()


@abort_on_failure('Образ [bold blue]"{image}"[/] не найден!', ImageNotFound, format_with_args=True)
def get_image(image: str) -> Image:
    return docker.images.get(image)


@abort_on_failure(exception=DockerException)
def build_image(*args, **kwargs) -> Image:
    return docker.images.build(*args, **kwargs)


if __name__ != "__main__":
    docker: DockerClient = setup_docker()
