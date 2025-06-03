import asyncio
import random
import re
from telethon import TelegramClient
api_id = 20405128
api_hash = '9cfe367412e0a6f6ddda736fed9cb770'
phone_number = '+916380102489'
session_file = 'bruhboth'

# Shared session for both bots

class FishingBot:
    def __init__(self, client):
        self.client = client
        self.stop_fishing = False

    async def start_fishing(self):
        bot = await self.client.get_entity('@roronoa_zoro_robot')

        while not self.stop_fishing:
            for _ in range(10):
                await self.client.send_message(bot, '/fish')
                await asyncio.sleep(random.uniform(2, 5))

                messages = await self.client.get_messages(bot, limit=2)
                for message in messages:
                    msg_text = message.message.lower()

                    # Cooldown detection
                    if 'your rod is broken' in msg_text:
                        print(f"[Cooldown] {msg_text}")
                        cooldown_time = self.extract_cooldown_time(msg_text)
                        print(f"Waiting {cooldown_time} seconds...")
                        await self.client.send_message(bot, '/dart')
                        await asyncio.sleep(cooldown_time)
                        break

                    # Detect and stop duplicate fishing
                    if '/stopfish' in msg_text:
                        print("[Info] Already fishing. Sending /stopfish.")
                        await self.client.send_message(bot, '/stopfish')
                        await asyncio.sleep(random.uniform(3, 6))
                        break

                    # Click available buttons (e.g., to reel in fish)
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                print(f"[Clicking] {button.text}")
                                await message.click(0)
                                await asyncio.sleep(random.uniform(2, 4))

    def extract_cooldown_time(self, text):
        match = re.search(r'(\d+)m[: ]?(\d+)s', text)
        if match:
            return int(match.group(1)) * 60 + int(match.group(2))
        match = re.search(r'(\d+)s', text)
        return int(match.group(1)) if match else 60


class HuntingBot:
    def __init__(self, client):
        self.client = client
        self.stop_hunting = False

    async def start_hunting(self):
        async with self.client:
            bot_entity = await self.client.get_entity('@HeXamonbot')
            while not self.stop_hunting:
                last_messages = await self.client.get_messages(bot_entity, limit=2)
                shiny_found = any('✨' in message.message.lower() for message in last_messages)
                if shiny_found:
                    self.stop_hunting = True
                    await self.client.send_message(-4699934526, "@ibangchildren shiny found da")
                    print('Shiny Pokemon found in last messages!')
                    break

                for message in last_messages:
                    await self.handle_message(message)

                if not self.stop_hunting:
                    await self.client.send_message('@HeXamonbot', '/hunt')
                gap = random.randint(2, 6)
                await asyncio.sleep(gap)

    async def handle_message(self, message):
        stop_keywords = [
            "✨ Shiny", "Daily hunt limit reached"
        ]

        if any(keyword in message.message for keyword in stop_keywords):
            self.stop_hunting = True
            print(f"Found stopping keyword in message: {message.message}")
        else:
            print(f"Received message: {message.message}")

    async def connect(self):
        await self.client.start()
        # Handle OTP and TFA code if required
        # Your code logic here

    def close(self):
        self.stop_hunting = True
        self.client.disconnect()


async def main():
    client = TelegramClient(session_file, api_id, api_hash)
    await client.start()

    fishing_bot = FishingBot(client)
    hunting_bot = HuntingBot(client)

    await asyncio.gather(
        fishing_bot.start_fishing(),
        hunting_bot.start_hunting()
    )

if __name__ == '__main__':
    asyncio.run(main())
