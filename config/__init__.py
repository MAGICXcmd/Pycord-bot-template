from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
OWNER_ID = env.int("OWNER_ID")
MAIN_GUILD_ID = env.int("MAIN_GUILD_ID")
INFORMATION_CHANNEL_ID = env.int("INFORMATION_CHANNEL_ID")