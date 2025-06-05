import os
import re
import random
import time
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import PhotoStrippedSize

# === CONFIG ===
api_id = 24797759
api_hash = '4778e4d11c63dc6f6085876fe586b81d'
LOG_GROUP_ID = -4699934526
chatid = -4831451271  # For Pokémon guessing
SESSION = '1BVtsOHwBu0QiHpqN-S4rPoYBEf9mDkEdJxrk0BRWtHqa0NKaDh9SUybTlqmoSI0F3MDRoiMsdV_OwkkC3OQ7oYrIVCsUkuieY4vxRes8VJjIpQfAERIKRD7kez6fAcZRmUdvO-ieD02mibnpqHgRjNjKsufzs27a8os_dMlVL4CabBF46IZAzZU7Y1uaEVND1z-OcnIXWVJGGZNE-WQGSi4KVvGbBSGH5V2ZBiw5oj3m7Gl_f1DZ_C40EADkMiBN6gygiU7JRTyrHLP-MmS8fsZLowUloufqxrbFynjqXy-Hj9z37J7OPkrBIxMQ1YTDgX7ZiknDXeeX3yW192mqygZWCajC2sc='
temp_cache_size = None
# Create a single shared client instance
client = TelegramClient(StringSession(SESSION), api_id, api_hash)

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
                        await self.client.send_message(self.bot_entity, '/explore')
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
                    if self.failed_attempts >= 50:
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
        self.pause_event.set()
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
                await self.client.send_message(LOG_GROUP_ID, "@peeekahboo shiny found da")
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
                    await self.client.send_message(LOG_GROUP_ID, "bot ded @peeekahboo (hunting)")
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

# === Pokémon Guessing ===
os.makedirs("cache", exist_ok=True)
os.makedirs("../../saitama", exist_ok=True)
last_guess_time = 0
guess_timeout = 5
pending_guess = False
retry_lock = asyncio.Lock()
reward_count = 0
correct_guess_count = 0
pause_mode = False
guess_fail_count = 0
guess_fail_threshold = 10

async def send_guess_command():
    global last_guess_time, pending_guess, pause_mode
    if pause_mode:
        print("Paused. Skipping /guess.")
        return
    try:
        await client.send_message(entity=chatid, message='/guess')
        print("Sent /guess command.")
        last_guess_time = time.time()
        pending_guess = True
    except Exception as e:
        print(f"Error in sending /guess: {e}")
        await asyncio.sleep(3)
        await send_guess_command()

@client.on(events.NewMessage(from_users=572621020, pattern="Who's that pokemon?", chats=chatid))
async def guess_pokemon(event):
    global last_guess_time, pending_guess, reward_count, correct_guess_count, guess_fail_count
    pending_guess = False
    for size in event.message.photo.sizes:
        if isinstance(size, PhotoStrippedSize):
            size = str(size)
            for file in os.listdir("cache/"):
                with open(f"cache/{file}", 'r') as f:
                    if f.read() == size:
                        name = file.replace(".txt", "")
                        await client.send_message(chatid, "Type: null" if name == "Type_ Null" else name)
                        reward_count += 5
                        correct_guess_count += 1
                        guess_fail_count = 0
                        await asyncio.sleep(3)
                        await send_guess_command()
                        return
            global temp_cache_size
            temp_cache_size = size

@client.on(events.NewMessage(from_users=572621020, pattern="The pokemon was ", chats=chatid))
async def save_pokemon(event):
    global pending_guess, guess_fail_count
    pending_guess = False
    name = ((event.message.text).split("The pokemon was **")[1]).split("**")[0]
    global temp_cache_size
    with open(f"cache/{name}.txt", 'w') as file:
        file.write(temp_cache_size)
    temp_cache_size = None
    guess_fail_count = 0
    await send_guess_command()

@client.on(events.NewMessage(pattern=r"\.guess", chats=chatid))
async def manual_guess(event):
    await send_guess_command()

@client.on(events.NewMessage(pattern=r"\.pauseguess", chats=chatid))
async def toggle_pause(event):
    global pause_mode
    pause_mode = not pause_mode
    await client.send_message(chatid, f"[Bot] Auto-guessing is now **{'PAUSED' if pause_mode else 'RESUMED'}**.")

async def monitor_responses():
    global pending_guess, last_guess_time, guess_fail_count, pause_mode
    while True:
        if pending_guess and (time.time() - last_guess_time > guess_timeout):
            guess_fail_count += 1
            if guess_fail_count >= guess_fail_threshold:
                pause_mode = True
                await client.send_message(chatid, "[Bot] Paused after 10 failed /guess attempts.")
                pending_guess = False
            else:
                await send_guess_command()
        await asyncio.sleep(3)

async def display_stats():
    while True:
        print(f"Total rewards: {reward_count} | Correct guesses: {correct_guess_count}")
        await asyncio.sleep(30)

# === Main Runner ===
async def main():
    await client.start()
    print("Bot started.")
    await send_guess_command()
    fishing_bot = FishingBot(client)
    hunting_bot = HuntingBot(client)
    await asyncio.gather(
        fishing_bot.start_fishing(),
        hunting_bot.start_hunting(),
        monitor_responses(),
        display_stats(),
        client.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(main())
