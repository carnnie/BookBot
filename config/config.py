from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tgBot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(tgBot=TgBot(token=env("BOT_TOKEN"), admin_ids=list(map(int, env("ADMIN_IDS")))))
