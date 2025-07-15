
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
import json
import os

API_ID = 12345678  # Replace with your API ID
API_HASH = "your_api_hash"  # Replace with your API Hash
BOT_TOKEN = "YOUR_BOT_TOKEN"

GROUP_ID = -1002740358553
REQUIRED_ADDS = 5

if not os.path.exists("user_data.json"):
    with open("user_data.json", "w") as f:
        json.dump({}, f)

app = Client("force_add_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def load_data():
    with open("user_data.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("user_data.json", "w") as f:
        json.dump(data, f)

@app.on_message(filters.new_chat_members & filters.chat(GROUP_ID))
def new_member_handler(client, message):
    new_members = message.new_chat_members
    inviter = message.from_user

    if not inviter or inviter.id == new_members[0].id:
        return

    data = load_data()
    inviter_id = str(inviter.id)
    if inviter_id not in data:
        data[inviter_id] = {"count": 0, "unlocked": False}

    data[inviter_id]["count"] += len(new_members)

    if data[inviter_id]["count"] >= REQUIRED_ADDS:
        data[inviter_id]["unlocked"] = True
        try:
            client.restrict_chat_member(GROUP_ID, inviter.id, ChatPermissions(can_send_messages=True))
            client.send_message(GROUP_ID, f"🔓 {inviter.mention} ka moksha safal hua! You can now send messages.")
        except:
            pass
    else:
        remaining = REQUIRED_ADDS - data[inviter_id]["count"]
        client.send_message(GROUP_ID,
            f"🕉️ Ahem... Brahmāsmi, {inviter.mention}

"
            f"Abhi tak tumne {data[inviter_id]['count']} / {REQUIRED_ADDS} sathiyon ko bulaya hai.
"
            f"Aur {remaining} aur chahiye moksha ke liye.

"
            "🔒 Tab tak tumhare liye group band hai."
        )
        try:
            client.restrict_chat_member(GROUP_ID, inviter.id, ChatPermissions(can_send_messages=False))
        except:
            pass

    save_data(data)

@app.on_message(filters.command("start") & filters.private)
def start_handler(client, message):
    message.reply("Bot is active and tracking invites. Jai Guruji 🙏")

app.run()
