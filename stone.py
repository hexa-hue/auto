from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 20405128
api_hash = '9cfe367412e0a6f6ddda736fed9cb770'

with TelegramClient('session.+916380102489', api_id, api_hash) as client:
    print('Your StringSession:')
    print(StringSession.save(client.session))
