import asyncio
import random
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = 20405128
api_hash = '9cfe367412e0a6f6ddda736fed9cb770'
LOG_GROUP_ID = -4699934526  # Replace with your log group ID

# === Fishing Bot ===
class FishingBot:
    def __init__(self, client):
        self.client = client
        self.stop_fishing = False
        self.pause_event = asyncio.Event()
        self.pause_event.set()
        self.response_received = False
        self.failed_attempts = 0
        self.fishing_task = None
        self.bot_entity = None

    async def start_fishing(self):
        self.bot_entity = await self.client.get_entity('@roronoa_zoro_robot')
        self.client.add_event_handler(self.command_handler, events.NewMessage)
        self.fishing_task = asyncio.create_task(self.fishing_loop())

    async def fishing_loop(self):
        while not self.stop_fishing:
            await self.pause_event.wait()

            for _ in range(10):
                self.response_received = False
                await self.client.send_message(self.bot_entity, '/fish')
                await asyncio.sleep(random.uniform(2, 5))

                messages = await self.client.get_messages(self.bot_entity, limit=2)
                for message in messages:
                    msg_text = message.message.lower()

                    if 'your rod is broken' in msg_text:
                        cooldown_time = self.extract_cooldown_time(msg_text)
                        await self.client.send_message(self.bot_entity, '/dart')
                        await asyncio.sleep(cooldown_time)
                        self.response_received = True
                        break

                    if '/stopfish' in msg_text:
                        await self.client.send_message(self.bot_entity, '/stopfish')
                        await asyncio.sleep(random.uniform(3, 6))
                        self.response_received = True
                        break

                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                await message.click(0)
                                await asyncio.sleep(random.uniform(2, 4))
                                self.response_received = True

                if self.response_received:
                    self.failed_attempts = 0
                else:
                    self.failed_attempts += 1
                    print(f"[FishingBot] No response, failed_attempts = {self.failed_attempts}")
                    if self.failed_attempts >= 5:
                        await self.client.send_message(LOG_GROUP_ID, "bot ded @peeekahboo (fishing)")
                        self.stop_fishing = True
                        break

    def extract_cooldown_time(self, text):
        match = re.search(r'(\d+)m[: ]?(\d+)s', text)
        if match:
            return int(match.group(1)) * 60 + int(match.group(2))
        match = re.search(r'(\d+)s', text)
        return int(match.group(1)) if match else 60

    async def command_handler(self, event):
        text = event.raw_text.lower()

        if text == ".startfishing":
            if self.fishing_task is None or self.fishing_task.done():
                print("[Command] Restarting fishing loop")
                self.stop_fishing = False
                self.pause_event.set()
                self.fishing_task = asyncio.create_task(self.fishing_loop())
            else:
                print("[Command] Resuming fishing loop")
                self.stop_fishing = False
                self.pause_event.set()

        elif text == ".pausefishing":
            print("[Command] Pausing fishing")
            self.pause_event.clear()

# === Hunting Bot ===
class HuntingBot:
    def __init__(self, client):
        self.client = client
        self.stop_hunting = False
        self.pause_event = asyncio.Event()
        self.pause_event.set()  # Unpaused by default
        self.response_received = False
        self.failed_attempts = 0
        self.hunting_task = None
        self.bot_entity = None

    async def start_hunting(self):
        self.bot_entity = await self.client.get_entity('@HeXamonbot')
        self.client.add_event_handler(self.command_handler, events.NewMessage)
        self.hunting_task = asyncio.create_task(self.hunting_loop())

    async def hunting_loop(self):
        while not self.stop_hunting:
            await self.pause_event.wait()

            last_messages = await self.client.get_messages(self.bot_entity, limit=2)
            shiny_found = any('✨' in message.message.lower() for message in last_messages)

            if shiny_found:
                self.stop_hunting = True
                await self.client.send_message(-4699934526, "@peeekahboo shiny found da")
                print('Shiny Pokémon found! Pausing hunting...')
                break

            self.response_received = False
            for message in last_messages:
                await self.handle_message(message)

            if self.response_received:
                self.failed_attempts = 0
            else:
                self.failed_attempts += 1
                print(f"[HuntingBot] No response, failed_attempts = {self.failed_attempts}")
                if self.failed_attempts >= 5:
                    await self.client.send_message(-4699934526, "bot ded @peeekahboo (hunting)")
                    self.stop_hunting = True
                    break

            if not self.stop_hunting:
                await self.client.send_message(self.bot_entity, '/hunt')
                await asyncio.sleep(random.randint(2, 6))

    async def handle_message(self, message):
        stop_keywords = ["✨ shiny", "daily hunt limit reached"]
        if any(keyword in message.message.lower() for keyword in stop_keywords):
            self.stop_hunting = True
            print(f"[Stop] Found stop keyword: {message.message}")
        elif 'wild' in message.message.lower() or 'has appeared' in message.message.lower():
            self.response_received = True
            print(f"[Hunt Message] {message.message}")

    async def command_handler(self, event):
        text = event.raw_text.lower()

        if text == ".start":
            if self.hunting_task is None or self.hunting_task.done():
                print("[Command] Restarting hunting loop")
                self.stop_hunting = False
                self.pause_event.set()
                self.hunting_task = asyncio.create_task(self.hunting_loop())
            else:
                print("[Command] Resuming hunting loop")
                self.stop_hunting = False
                self.pause_event.set()

        elif text == ".pause":
            print("[Command] Pausing hunting")
            self.pause_event.clear()

# === Main Runner ===
async def main():
    client = TelegramClient(
        StringSession('1BVtsOHwBuxGUAgfewg2-D9euQZF29QYlz1iSqnauguaGs0GelNXs6VpXBx3Przr1bih5dUmPqJijLPMe0bAkVN3qgM31-z-t-bng4TTbix3wSRGn0SzgHn8GD7aCSQUjlCkZJfTaJ73HM21nf2ytrbSY6VH965HfMX8x4z_iM09TpebotmH9svBH5WDqS67kyDDQ4vNIa_xW2SoHKOMIjXFMRhd1S_WGFdehK5D4SnCV1Jqu3OMb8d3Vuqvqur-LMJKOjSmPD15kkAmPMaOipKEXRQmq16iWQt_FvE1QYiDYI1ADP9YEa7JzORmgkm6s6zYXQHzVI7zRRzBapuKhDKJDtHMCax0='),
        api_id, api_hash
    )
    await client.start()

    fishing_bot = FishingBot(client)
    hunting_bot = HuntingBot(client)

    await asyncio.gather(
        fishing_bot.start_fishing(),
        hunting_bot.start_hunting()
    )

if __name__ == '__main__':
    asyncio.run(main())
