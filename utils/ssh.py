from paramiko import AuthenticationException, AutoAddPolicy, SSHClient

from .common import cli_exception


def setup_ssh() -> SSHClient:
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()

    return client


def connect(host=None) -> SSHClient:
    from whale import config as global_config

    if host:
        config: dict = global_config[host]
    else:
        config: dict = global_config.default_host

    # config.update(ssh_config.lookup(hostname)) TODO

    client = setup_ssh()

    try:
        client.connect(**config)
    except AuthenticationException:
        cli_exception("Не пройдена аутентификация SSH.\nПроверьте правильность пароля.")

    return client.get_transport().open_session()
