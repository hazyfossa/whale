from os import PathLike
from os.path import isfile
from tomllib import load as load_toml

from attrs import define as setting
from .common import cli_exception, userpath
from rich.prompt import Prompt
from tomli_w import dump as dump_toml

# TODO recreate this
# with open(userpath("~/.ssh/config"), "r") as f:
#     ssh_config: SSHConfig = SSHConfig.from_file(f)


# TODO normalize + type
@setting
class Host:
    hostname: str
    username: str
    password: str
    port: int = 22


def wizard():
    print("Создаём конфиг...")
    p = Prompt()

    hostname = p.ask("Введите ваш домен или IP адрес: ")
    username = p.ask("Введите имя пользователя: ")
    password = p.ask("Введите пароль: ", password=True)
    name = p.ask("Назовите этот сервер: ")

    new_config = {
        "default": name,
        name: {"hostname": hostname, "username": username, "password": password},
    }

    return new_config


class Config:
    def __init__(self, autowrite=True, path="~/.whale.toml", wizard=wizard) -> None:
        self.path: PathLike = userpath(path)

        if not isfile(self.path):
            self.create_with(wizard())

        self.autowrite = autowrite
        self.raw = self.read()

    def __getitem__(self, key):
        return self.raw[key]

    def __setitem__(self, key, value) -> None:
        self.raw[key] = value

        if self.autowrite:
            self.write()

    @property
    def default_host(self):
        return self.raw[self.raw["default"]]

    def get_host(self, host: str):
        if host:
            try:
                return self[host]
            except KeyError as e:
                cli_exception(f"Не найдена конйигурация для хоста {e}")
        else:
            return self.default_host

    # TODO exclude top-level settings from autocomplete
    # def autocomplete_hosts(self, incomplete: str) -> str:
    #     completion = []
    #     for name in self.raw.items():
    #         if name.startswith(incomplete):
    #             completion.append(name)
    #     return completion

    def read(self):
        with open(self.path, "rb") as f:
            return load_toml(f)

    def write(self) -> None:
        with open(self.path, "rb") as f:
            dump_toml(self.raw, f)

    def create_with(self, data) -> None:
        with open(self.path, "+xb") as f:
            dump_toml(data, f)
            self.raw = data
