from environs import Env
# from dotenv import load_dotenv
# import os

env = Env()
env.read_env()
BOT_TOKEN=env.str('BOT_TOKEN')
ADMINS=env.list('ADMINS')
CHANNELS=env.list("CHANNELS")

url = env.str("URL")
db = env.str("DB")
username = env.str("USERNAME")
password = env.str("PASSWORD")