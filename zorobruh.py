import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession
import re

api_id = 20405128
api_hash = '9cfe367412e0a6f6ddda736fed9cb770'
class FishingBot:
    def __init__(self):
        self.client = TelegramClient(StringSession('1BVtsOHYBuzLu1UrJ0Behet64EDvSwcbM8uW67Dnifk5oDxYaxzxRGHvsSUigQuvQP-5CIjqK7jlmh0GnB_hbD4iZ5piPO9Tsd1wK1B0e7sUgRchz-r4dzA3vdr1a5sMoYHo8P-SvRLOOHUorOXeT32kIuEE0-io1WSi_p2dOQ75E6qUgTDlqkRCvPedgKX9Ni23Or5uuYuoEiVaq2y7edBj9J22NC_6SzCElo4NT39DgKROCN6IiVsW7rYSOU3dQrRrSBnL9uZ19ufeXJNDmhtCGOp_k2jyIL_GuSt0_zg7WcQ6X_u_EEgf8Ov8GTx_0FKxw4hhHpQg7n2EOvnImQo2eij7ccgA='), api_id, api_hash)
        self.stop_fishing = False

    async def start_fishing(self):
        async with self.client:
            bot_entity = await self.client.get_entity('@roronoa_zoro_robot')

            while not self.stop_fishing:
                for _ in range(10):
                    await self.client.send_message(bot_entity, '/fish')
                    await asyncio.sleep(random.randint(2, 5))

                    last_messages = await self.client.get_messages(bot_entity, limit=2)

                    # Check for cooldown immediately
                    for message in last_messages:
                        msg_text = message.message.lower()
                        if 'your rod is broken' in msg_text:
                            print(f"Cooldown message detected: {msg_text}")
                            match = re.search(r'(\d+)m[: ]?(\d+)s', msg_text)
                            if match:
                                minutes = int(match.group(1))
                                seconds = int(match.group(2))
                                cooldown_time = (minutes * 60) + seconds
                            else:
                                match = re.search(r'(\d+)s', msg_text)
                                if match:
                                    cooldown_time = int(match.group(1))
                                else:
                                    cooldown_time = 60  # fallback
                            print(f"Waiting for {cooldown_time} seconds due to cooldown.")
                            await self.client.send_message(bot_entity, '/bal')
                            await asyncio.sleep(cooldown_time)

                            # Check if "/stopfish" is needed
                    for message in last_messages:
                        if "You're already fishing!" in message.message:
                            print("Already fishing detected! Sending /stopfish.")
                            await self.client.send_message(bot_entity, '/stopfish')
                            await asyncio.sleep(random.randint(3, 6))

                    # Check bot response
                    last_messages = await self.client.get_messages(bot_entity, limit=2)
                    for message in last_messages:
                        if message.buttons:
                            for row in message.buttons:
                                for button in row:
                                    print("Clicking button:", button.text)
                                    await message.click(0)
                                    await asyncio.sleep(random.randint(2, 5))


                # Detect proper cooldown message
    async def connect(self):
        await self.client.start()

    def close(self):
        self.stop_fishing = True
        self.client.disconnect()

async def main():
    bot = FishingBot()
    await bot.connect()
    await bot.start_fishing()
    bot.close()
    print("Fishing script stopped.")

if __name__ == "__main__":
    asyncio.run(main())
