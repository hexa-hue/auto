import asyncio
import re
from collections import deque
from telethon import TelegramClient, events
from telethon.errors import DataInvalidError

# === CONFIG ===
api_id = 24797759
api_hash = '4778e4d11c63dc6f6085876fe586b81d'
client = TelegramClient('stonehunt', api_id, api_hash)
pok_name="none"
HEXAMON_BOT_ID = 572621020
LOG_GROUP_ID = -4699934526
curr="Blissey"
regular_ball = {"Fennekin", "Braixen", "Froakie", "Mareep","Duraludon","Aron"}
repeat_ball = { "Aerodactyl", "Delphox", "Frogadier", "Greninja", "Moltres", "Mewtwo",
               "Raikou", "Entei",
               "Suicune", "Lugia", "Ho-oh", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon",
               "Rayquaza", "Uxie", "Mesprit",
               "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Cobalion", "Terrakion",
               "Virizion", "Tornadus",
               "Thundurus", "Landorus", "Reshiram", "Zekrom", "Kyurem", "Xerneas", "Yveltal", "Zygarde", "Tapu Koko",
               "Tapu Lele", "Tapu Bulu",
               "Tapu Fini", "Solgaleo", "Lunala", "Necrozma", "Zacian", "Zamazenta", "Eternatus", "Regieleki",
               "Regidrago", "Glastrier", "Spectrier",
               "Calyrex", "Enamorus"}

# === STATE FLAGS ===
in_battle = False
hunt_in_progress = False
button_operation_in_progress = False
low_lvl = False
response_received = False
cooldown = 3
last_two_messages = deque(maxlen=2)


async def wait_for_bot_response(timeout=4):
    """Waits for a new message or edit from HEXAMON_BOT_ID signaling bot response."""
    event_received = asyncio.Event()

    async def handler(event):
        event_received.set()

    client.add_event_handler(handler, events.NewMessage(from_users=HEXAMON_BOT_ID))
    client.add_event_handler(handler, events.MessageEdited(from_users=HEXAMON_BOT_ID))

    try:
        await asyncio.wait_for(event_received.wait(), timeout)
        return True
    except asyncio.TimeoutError:
        return False
    finally:
        client.remove_event_handler(handler, events.NewMessage(from_users=HEXAMON_BOT_ID))
        client.remove_event_handler(handler, events.MessageEdited(from_users=HEXAMON_BOT_ID))


async def send_hunt(retries=0):
    global hunt_in_progress, response_received

    if hunt_in_progress:
        return

    hunt_in_progress = True
    response_received = False

    print("Sending /hunt command...")
    await client.send_message(HEXAMON_BOT_ID, '/hunt')

    await asyncio.sleep(3)  # wait for response

    if not response_received:
        print("No response detected after /hunt. Retrying...")
        hunt_in_progress = False
        if retries < 5:
            await send_hunt(retries + 1)
        else:
            await client.send_message(LOG_GROUP_ID, "@ibangchildren @isaaac_newton bot ded")
    else:
        hunt_in_progress = False


@client.on(events.NewMessage(from_users=HEXAMON_BOT_ID))
async def on_new_message(event):
    global in_battle, response_received, low_lvl
    text = event.raw_text
    last_two_messages.append(text)

    if "Daily hunt limit reached" in text:
        print("[Exit] Limit reached.")
        await client.disconnect()
        return

    if "✨ Shiny Pokémon found!" in text:
        print("[Shiny] Found!")
        await client.send_message(LOG_GROUP_ID, "@ibangchildren @isaaac_newton shiny poke da")
        await client.disconnect()
        return

    if "A wild" in text:
        global hunt_in_progress,pok_name
        response_received = True
        pok_name = text.split("wild ")[1].split(" (")[0]
        print(f"[Wild] {pok_name} appeared")
        if pok_name in regular_ball or pok_name in repeat_ball:
            try:
                button = find_button(event, "Battle")
                if button:
                    await asyncio.sleep(1)
                    await event.click(text="Battle")
                    in_battle = True
                    print("[Click] Battle button")
                else:
                    print("[Error] Battle button not found.")
            except Exception as e:
                print(f"[Error] Battle click failed: {e}")
        else:
            print("[Skip] Not a target Pokémon.")
            hunt_in_progress = False
            await asyncio.sleep(cooldown)
            await send_hunt()
        return

    if any(word in text.lower() for word in ["expert"]):
        response_received = True
        in_battle = False
        low_lvl = False
        print(f"[Battle Result] {text.strip()}")
        await asyncio.sleep(cooldown)
        await send_hunt()


def find_button(event, button_text):
    """Searches the message for a specific button by partial text match."""
    for row in event.message.buttons:
        for button in row:
            if button_text.lower() in button.text.lower():  # Allow partial match
                return button
    return None


'''async def safe_click(event, button_text, retries=3, delay=2):
    """Attempts to click a button and retries if it's not found, while checking available buttons dynamically."""
    for attempt in range(retries):
        if event.message.buttons:
            button_texts = [button.text for row in event.message.buttons for button in row]
            print(f"[Available Buttons]: {button_texts}")
        else:
            print("[Warning] No buttons available.")

        button = find_button(event, button_text)

        if button:
            print(f"[Click] Attempting '{button_text}' (Try {attempt + 1})")
            await event.click(text=button_text)
            return True

        print(f"[Warning] Button '{button_text}' not found. Retrying in {delay} sec...")
        await asyncio.sleep(delay)

    print(f"[Error] Button '{button_text}' not found after {retries} attempts.")
    return False'''
@client.on(events.MessageEdited(from_users=HEXAMON_BOT_ID))
@client.on(events.NewMessage(from_users=HEXAMON_BOT_ID))
async def handle_battle(event):
    global in_battle, low_lvl, response_received, pok_name

    if not in_battle:
        return

    text = event.raw_text.lower()

    # Battle End Detection
    if any(x in text for x in ["fled", "💵"]) or ("caught" in text):
        print("[Battle] Ended.")
        in_battle = False
        response_received = True
        await asyncio.sleep(2)
        await send_hunt()
        return

    # Extract HP and Pokémon Name
    match = re.search(r"hp (\d+)/(\d+)", text)
    pok_match = re.search(r"wild (\w+)", text)
    if match and pok_match:
        current_hp, max_hp = map(int, match.groups())
        hp_percent = (current_hp / max_hp) * 100

        try:
            # Decide Catch Attempt
            if low_lvl or hp_percent <= 40 or max_hp <= 60:
                #await asyncio.sleep()
                '''button = find_button(event,"Poke Balls")
                if button:'''

                print(f"[Catch] {pok_name} at {hp_percent:.0f}% HP")
                print(pok_name,"POK_NAME")
                print("POKE BALL")
                await asyncio.sleep(1)  # Wait for UI change
                sure = await button_exists(event,"Poke Balls")
                if sure:
                    await event.click(text="Poke Balls")
                    ball_type = "Repeat" if pok_name in repeat_ball else "Regular"
                    print("Used",ball_type)
                    await asyncio.sleep(1)
                    really=await button_exists(event,ball_type)
                    if really:
                        await event.click(text=ball_type)
            else:
                print(f"[Attack] {pok_name} at {hp_percent:.0f}% HP")
                await attack(event)
        except Exception as e:
            print(f"[Battle Error] {e}")
            return
async def button_exists(event, button_text):
    return any(button_text in button.text for row in event.message.buttons for button in row)
async def attack(event):
    await asyncio.sleep(1)
    global curr
    if curr=="Blissey":
        await event.click(0, 0)
    elif curr=="Sofa" or curr=="Magearna" or curr=="Thala":
        await event.click(1,0)
    elif curr=="Aaa train":
        await event.click(0, 1)

@client.on(events.MessageEdited(from_users=HEXAMON_BOT_ID))
async def switch_pokemon(event):
    """Handles choosing the next Pokémon during battle."""
    global in_battle, button_operation_in_progress, curr

    if "Choose your next pokemon." in event.raw_text:
        in_battle = True
        button_operation_in_progress = True
        print("[Switch] Choosing next Pokémon...")

        try:
            selected = False
            pokemon_list = ["Sofa", "Aaa train", "Vulpix", "Magearna", "Thala"]
            global curr
            # Ensure the event contains buttons before interacting
            if event.message.buttons:
                for row in event.message.buttons:
                    for button in row:
                        if button.text in pokemon_list:  # Check if it's a valid choice
                            curr = button.text
                            await asyncio.sleep(1)
                            await event.click(text=button.text)
                            print(f"[Switch] Selected Pokémon: {button.text}")
                            selected = True
                            break
                    if selected:
                        break

            if not selected:
                print("[Error] No valid Pokémon found!")
                return  # Exit without sending a hunt

        except DataInvalidError as e:
            print(f"[Switch Error] Button expired or invalid: {e}")
            return
        except Exception as e:
            print(f"[Switch Error] Unexpected error: {e}")
            return

        await asyncio.sleep(2)
        button_operation_in_progress = False

async def main():
    await client.start()
    await client.catch_up()
    print("[Startup] Connected. Sending initial /hunt.")
    await send_hunt()
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())