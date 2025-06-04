import asyncio
import random
import re
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon import events
api_id = 20405128
api_hash = '9cfe367412e0a6f6ddda736fed9cb770'
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
        self.pause_event = asyncio.Event()
        self.pause_event.set()  # Unpaused by default

    async def start_hunting(self):
        # Register the command handler here using Telethon's event system
        self.client.add_event_handler(self.command_handler, events.NewMessage)

        bot_entity = await self.client.get_entity('@HeXamonbot')
        while not self.stop_hunting:
            await self.pause_event.wait()  # Pauses here if `.pause` was issued

            last_messages = await self.client.get_messages(bot_entity, limit=2)
            shiny_found = any('✨' in message.message.lower() for message in last_messages)
            if shiny_found:
                self.stop_hunting = True
                await self.client.send_message(-4699934526, "@ibangchildren shiny found da")
                print('Shiny Pokémon found! Pausing hunting...')
                break

            for message in last_messages:
                await self.handle_message(message)

            if not self.stop_hunting:
                await self.client.send_message('@HeXamonbot', '/hunt')

            await asyncio.sleep(random.randint(2, 6))

    async def handle_message(self, message):
        stop_keywords = ["✨ Shiny", "Daily hunt limit reached"]
        if any(keyword in message.message for keyword in stop_keywords):
            self.stop_hunting = True
            print(f"[Stop] Found stop keyword: {message.message}")
        else:
            print(f"[Hunt Message] {message.message}")

    async def command_handler(self, event):  # This now only handles text messages
        text = event.raw_text.lower()

        if text == ".start":
            print("[Command] Received .start — resuming hunt.")
            self.pause_event.set()
        elif text == ".pause":
            print("[Command] Received .pause — pausing hunt.")
            self.pause_event.clear()

    async def connect(self):
        await self.client.start()


async def main():
    client = TelegramClient(StringSession('1BVtsOHwBuxGUAgfewg2-D9euQZF29QYlz1iSqnauguaGs0GelNXs6VpXBx3Przr1bih5dUmPqJijLPMe0bAkVN3qgM31-z-t-bng4TTbix3wSRGn0SzgHn8GD7aCSQUjlCkZJfTaJ73HM21nf2ytrbSY6VH965HfMX8x4z_iM09TpebotmH9svBH5WDqS67kyDDQ4vNIa_xW2SoHKOMIjXFMRhd1S_WGFdehK5D4SnCV1Jqu3OMb8d3Vuqvqur-LMJKOjSmPD15kkAmPMaOipKEXRQmq16iWQt_FvE1QYiDYI1ADP9YEa7JzORmgkm6s6zYXQHzVI7zRRzBapuKhDKJDtHMCax0='), api_id, api_hash)
    await client.start()

    fishing_bot = FishingBot(client)
    hunting_bot = HuntingBot(client)

    await asyncio.gather(
        fishing_bot.start_fishing(),
        hunting_bot.start_hunting()
    )

if __name__ == '__main__':
    asyncio.run(main())
