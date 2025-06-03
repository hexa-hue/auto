import asyncio
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# === Account Configurations ===
accounts = [
    {
        'name': 'peeekahboo',
        'api_id': 24797759,
        'api_hash': '4778e4d11c63dc6f6085876fe586b81d',
        'session': '1BVtsOHkBu6FnOuPGRIGUkAGAr5Zmy25XWz6V1axPx6bAAOSh4t83KznquSJEmkhloAmTQAL-uh7DDtBHG-eP32LEQvny7isYOcwdwTfsWVbFHIqNkEkPlzJ6RpFMZ-MgzR8BksE38ve_3NaafyALWcQf4k1wW1SI5zGLx2JzfEzSSm64_SRaebFLKDn3kLYHgWFQsoXTHB6mTtxp--G66DtfvXgWUyZjaKdeB7KZzO4GScyi1n7ptqC8ArbI2Ol2kLmfiCSDOQCMUATF6X_n61yc4ZoF870CiyyJHNbCyfa7tcemca0SED8BfxWp2v1fsqR-Zgt5dfthMzDBzIKaklXecVtIz-c=',
        'watch_username': 'isaaac_newton'
    },
    {
        'name': 'isaaac_newton',
        'api_id': 20405128,
        'api_hash': '9cfe367412e0a6f6ddda736fed9cb770',
        'session': '1BVtsOI0Bu7IRsHBa1gVleukpWhdS4ciCr3woFHIgO8VBFltYDrBBOfYnTovlQ6zsdG0W6CsyQZYaolrgQ5iR08phSsvu1QpkCtQm68Bg0TKNeiXJKp3K2GVZRgTNcbPwDf_Wp3zOyEIzmdQZUz8JUxyZwxYCU9svITuYXg6MyeqhaEvdfuWHZSGQkN0xEZnlXcC5GFT0Q1sbtlN8W_Hr9wXm213--cns_Gpd8zfkY99BcUF4mfySOKwZRGsZ1YGi53Dnw3k2tUFK_vPr2VoBWYje1gn1IvCIEhYrlldYuKfLUpGFB1XpkwibhX6IC87hvjNUXH3hlEvTEB3tT7srI3odaNWpsGg=',
        'watch_username': 'peeekahboo'
    }
]

groups = [-1001782914048]  # Add more groups as needed
trigger_words = ['hi', 'how are you', 'nig', 'ga']
clients = []

async def stop_all_clients():
    print("Stopping all clients due to 'Not found'...")
    await asyncio.gather(*(client.disconnect() for client in clients))
    exit(0)

async def setup_client(account):
    client = TelegramClient(StringSession(account['session']), account['api_id'], account['api_hash'])

    @client.on(events.NewMessage(chats=groups))
    async def message_handler(event):
        sender = await event.get_sender()
        text = event.raw_text.lower()
        if sender.username == account['watch_username'] and text in trigger_words:
            print(f"[{account['name']}] Trigger '{text}' in group {event.chat_id}")
            delay = random.uniform(3, 8)
            await asyncio.sleep(delay)
            reply_text = random.choice(trigger_words)
            do_reply = random.choice([True, False])
            if do_reply:
                try:
                    async for msg in client.iter_messages(event.chat_id, limit=10):
                        if msg.sender_id != (await client.get_me()).id:
                            print(f"[{account['name']}] Replying to message ID {msg.id}")
                            await client.send_message(event.chat_id, reply_text, reply_to=msg.id)
                            break
                except Exception as e:
                    print(f"[{account['name']}] Error in reply mode: {e}")
                    await client.send_message(event.chat_id, reply_text)
            else:
                print(f"[{account['name']}] Sending message: {reply_text}")
                await client.send_message(event.chat_id, reply_text)

    # This section runs only for '@peeekahboo' account
    if account['name'] == 'peeekahboo':
        message_origin_map = {}

        @client.on(events.NewMessage(
            from_users=["Waifu_Grabber_Bot", "Husbando_Grabber_Bot"],
            chats=groups))
        async def forward_images_to_target(event):
            # Check if message contains photo and specific symbols in text
            if event.photo and any(symbol in (event.raw_text or "") for symbol in ['🔮', '💮']):
                try:
                    forwarded = await client.forward_messages("collect_waifu_cheats_bot", event.message)
                    message_origin_map[forwarded.id] = event.chat_id
                    print("[Blood_demonartz] Forwarded image to @collect_waifu_cheats_bot")
                    await asyncio.sleep(10)
                    await client.delete_messages("collect_waifu_cheats_bot", forwarded.id)
                    print("[Blood_demonartz] Deleted forwarded message")
                except Exception as e:
                    print(f"[Blood_demonartz] Error forwarding/deleting: {e}")

        @client.on(events.NewMessage(from_users="collect_waifu_cheats_bot"))
        async def send_humanizer_to_group(event):
            text = event.raw_text or ""
            reply_to = await event.get_reply_message()
            origin_chat_id = message_origin_map.get(reply_to.id) if reply_to else None
            if "not found" in text.lower():
                print("[Blood_demonartz] 'Not found' detected. Shutting down.")
                await stop_all_clients()
                return
            if origin_chat_id:
                for line in text.splitlines():
                    if line.strip().startswith("Humanizer:"):
                        command = line.split(":", 1)[1].strip()
                        try:
                            await client.send_message(origin_chat_id, command)
                            print(f"[Blood_demonartz] Sent command: {command} to group {origin_chat_id}")
                        except Exception as e:
                            print(f"[Blood_demonartz] Error sending command: {e}")
                        break

    await client.start()
    print(f"[{account['name']}] Client started.")
    return client

async def main():
    global clients
    clients = await asyncio.gather(*(setup_client(acc) for acc in accounts))
    await asyncio.gather(*(client.run_until_disconnected() for client in clients))

if __name__ == '__main__':
    asyncio.run(main())
