import asyncio
from telethon import TelegramClient, events
import random
from telethon.errors import MessageIdInvalidError

api_id = 24797759
api_hash = '4778e4d11c63dc6f6085876fe586b81d'

async def main():
    client = TelegramClient('zorolol', api_id, api_hash)
    print('''started''')

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if "Monster" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  # Add a delay of 0.5 seconds
                await event.click(1, 0)  # Click the ultimate button (index 1, row 0)

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if "otherwise" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  # Add a delay of 0.5 seconds
                await event.click(2)
                await asyncio.sleep(1)
                await event.click(4)
                await event.client.send_message(-4699934526,"Captcha came @ibangchildren @isaaac_newton")

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if "1 tries" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(1)  # Add a delay of 0.5 seconds
                await event.client.send_message(-4699934526,"Me Nahi Kar sakta Captcha @Ibangchildren @isaaac_newton")
                await event.client.send_message(5364964725, "/explore")

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        if "Monster" in event.raw_text:
            try:
                await asyncio.sleep(0.5)  # Add a delay of 0.5 seconds
                await event.click(0)  # Click the regular button (index 0)
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        if "Unfortunately" in event.raw_text:
            try:
                await asyncio.sleep(0.5)  # Add a delay of 0.5 seconds
                await event.click(0)  # Click the regular button (index 0)
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        if "killed" in event.raw_text:
            try:
                await asyncio.sleep(1)
                await event.client.send_message(-4699934526, "Captcha Done Explore Restart")
                await event.client.send_message(5364964725, "/explore")
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.NewMessage(from_users=5416991774))
    async def _(event):
        if "challenged you !" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
            return

    @client.on(events.NewMessage(from_users=5416991774))
    async def _(event):
        if "HP" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
                #await message.click(row, column) ye hoga yaad rkahna hai
            return

    @client.on(events.MessageEdited(from_users=5416991774))
    async def _(event):
        if "HP" in event.raw_text:
            try:
                await asyncio.sleep(random.random() + 1)
                await event.click(0)
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.MessageEdited(from_users=5416991774))
    async def _(event):
        if "got defeated !" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
            return

    @client.on(events.NewMessage(from_users=5416991774))
    async def _(event):
        if "has appeared !" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)

    @client.on(events.MessageEdited(from_users=5416991774))
    async def _(event):
        if "jutsu" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(2)

    @client.on(events.MessageEdited(from_users=5416991774))
    async def handle_message(event):
        if "failed" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(2)
    
    @client.on(events.NewMessage(from_users=5416991774))
    async def handle_message(event):
        if "Death's Gambit" in event.raw_text:
            async for message in client.iter_messages(event.chat_id, limit=1):
                if message.reply_markup and message.reply_markup.rows:
                    found_data = None
                    for row in message.reply_markup.rows:
                        for button in row.buttons:
                            if button.data and len(button.data) == 33:
                                found_data = button.data
                                break
                        if found_data:
                            break

                    if found_data:
                        await asyncio.sleep(random.random() + 1)
                        await event.click(data=found_data)

    @client.on(events.MessageEdited(from_users=5416991774))
    async def _(event):
        if any(keyword in event.raw_text for keyword in ["You have defeated"]):
            await asyncio.sleep(random.random() + 1)
            await event.client.send_message(5416991774, "/explore")

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if any(keyword in event.raw_text for keyword in ["You found one pearl while exploring"]):
            await asyncio.sleep(random.random() + 1)
            await event.client.send_message(5364964725, "/explore")
            
    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if any(keyword in event.raw_text for keyword in ["You found 2 tickets 🎟 while exploring!"]):
            await asyncio.sleep(random.random() + 1)
            await event.client.send_message(5364964725, "/explore")

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if any(keyword in event.raw_text for keyword in ["You found 1 tickets 🎟 while exploring!"]):
            await asyncio.sleep(random.random() + 1)
            await event.client.send_message(5364964725, "/explore")

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if "Monster" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(1, 0)  

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        if "Monster" in event.raw_text:
            try:
                await asyncio.sleep(0.5)  
                await event.click(0)  
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if "Wishing" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0) 
                await event.client.send_message(5364964725, "/explore")

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if "Level" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0)

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if "offers?" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0) 

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        try:
            if "Offers you" in event.raw_text:
                per_pearl = None
                per_ticket = None
                contains_other_items = False

                
                for line in event.raw_text.split("\n"):
                    if "pearls for" in line:
                        per_pearl = int(line.split("for")[1].split("coins per")[0].strip())
                    elif "tickets for" in line:
                        per_ticket = int(line.split("for")[1].split("coins per")[0].strip())
                    elif any(item in line for item in ["rope", "net", "large net", "chain", "tranquilizer", "freeze ray"]):
                        contains_other_items = True

                if per_pearl and per_pearl > 220:
                    await asyncio.sleep(0.5) 
                    await event.client.send_message(5364964725, "/explore")
                elif per_ticket and per_ticket > 400:
                    await asyncio.sleep(0.5)  
                    await event.client.send_message(5364964725, "/explore")
                elif contains_other_items:
                    await asyncio.sleep(0.5)  
                    await event.client.send_message(5364964725, "/explore")
                elif per_pearl and per_pearl <= 250:
                    await asyncio.sleep(0.5)  
                    await event.click(0, 0) 
                elif per_ticket and per_ticket <= 400:
                    await asyncio.sleep(0.5)  
                    await event.click(0)  
        except (asyncio.TimeoutError, MessageIdInvalidError):
            pass

    @client.on(events.NewMessage(from_users=5364964725))
    async def _(event):
        if any(keyword in event.raw_text for keyword in ["coins and grant", "Common", "Rare"]):
            await asyncio.sleep(0.5)  
            await event.client.send_message(5364964725, "/explore")

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        if "traded" in event.raw_text:
            await asyncio.sleep(1)
            await event.client.send_message(5364964725, "/explore")

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        if "You found one pearl while exploring" in event.raw_text:
            await asyncio.sleep(1)
            await event.client.send_message(5364964725, "/explore")

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        if "You found 1 tickets 🎟 while exploring!" in event.raw_text:
            await asyncio.sleep(1)
            await event.client.send_message(5364964725, "/explore")

    @client.on(events.MessageEdited(from_users=5364964725))
    async def _(event):
        if "You found 2 tickets 🎟 while exploring!" in event.raw_text:
            await asyncio.sleep(1)
            await event.client.send_message(5364964725, "/explore")

    @client.on(events.MessageEdited(from_users=6149996968))
    async def handle_message_edited(event):
        if "HP" in event.raw_text:
            try:
                await asyncio.sleep(random.random() + 1)  
                await event.click(0, 0)
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.NewMessage(from_users=6149996968))
    async def handle_new_message(event):
        if "level" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)  
                await event.click(0)
            return

    @client.on(events.NewMessage(from_users=6149996968))
    async def handle_quota(event):
        if "QUOTA" in event.raw_text:
            await asyncio.sleep(random.random() + 1)  
            await event.client.send_message(6149996968, "/enter_dungeon")

    @client.on(events.NewMessage(from_users=6149996968))
    async def handle_hell(event):
        if "HELL" in event.raw_text:
            await asyncio.sleep(random.random() + 1)  
            await event.click(1)
        return

    @client.on(events.NewMessage(from_users=6149996968))
    async def handle_defeated(event):
        if any(keyword in event.raw_text for keyword in ["DED", "defeated", "entered"]):
            await asyncio.sleep(random.random() + 1)  
            await event.client.send_message(6149996968, "/explore")

    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())

import asyncio
from telethon import TelegramClient, events
import random
from telethon.errors import MessageIdInvalidError

api_id = 24797759
api_hash = '4778e4d11c63dc6f6085876fe586b81d'

async def main():
    client = TelegramClient('zorolol', api_id, api_hash)
    print('''lol ''')

    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if "You've encountered a Common Villain" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  # Add a delay of 0.5 seconds
                await event.click(2, 0)  # Click the constrictor button (index 1, row 0)

    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if "You've encountered a Common Villain" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
            return

    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if "HP" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
                #await message.click(row, column) ye hoga yaad rkahna hai
            return

    @client.on(events.MessageEdited(from_users=6741533520))
    async def _(event):
        if "HP" in event.raw_text:
            try:
                await asyncio.sleep(random.random() + 1)
                await event.click(0)
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if " Have No More Slug's To Battle And You Won* " in event.raw_tex:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0) 
                await event.client.send_message(6741533520, "/explore" )
                
    @client.on(events.MessageEdited(from_users=6741533520))
    async def _(event):
        if "Have No More Slug's To Battle And You Won" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
            return

    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if "Have No More Slug's To Battle And You Won*" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0) 
                await event.client.send_message(6741533520, "/explore")
                
    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if "You've encountered a Boss Villain" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0) 
                await event.client.send_message(6741533520, "/explore")
                
    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if "You've encountered a Rare Villain" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0) 
                await event.client.send_message(6741533520, "/explore")
                
    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if "Your Invincible Gang Got" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0) 
                await event.client.send_message(6741533520, "/explore")
                             
    @client.on(events.NewMessage(from_users=6741533520))
    async def _(event):
        if "You were exploring villains having a purpose of defeating them but suddenly you came across a person named " in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0.5)  
                await event.click(0) 
                await event.client.send_message(6741533520, "/explore" )

    @client.on(events.NewMessage(from_users=6741533520))
    async def handle_defeated(event):
        if any(keyword in event.raw_text for keyword in ["Your Invincible Gang Got", "Defeating" , "You Found A Key 🔑 While Exploring" , "You were exploring villains having a purpose of defeating them but suddenly you came across a person named"]):
            await asyncio.sleep(random.random() + 1)  
            await event.client.send_message(6741533520, "/explore")

    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())