import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw import functions
from pyrogram.raw.types import InputPeerChannel, ReactionEmoji

# ==================== CONFIGURATION ====================
API_ID = 32500857         
API_HASH = "777a8c5d7b009d027a2d3b64b67652f1"  
SESSION_STRING = "BQHv7HkABfcNqruKJmIqHXxLaI_b5OXfnjp6xLx43mZXc9Jc-0f_oVCEAL5_xIzHrfP1dx-EQhu3vVWeVwKJhOeAZKOMHz1YRmub0HNTyfwKP034CMZjdGgmtQrVDS_bXLGv5JqARuXlpu2Tpx1UX-qNxtHY1WXU1pCzpKhQNxrWeyEwSKRNbdwfr7APjpZvwv058cS7sVJGbhhp5HHQXjoGE67Y6LuElYtRMg4Je28m3rkj2rHReVtZ1L1pso5kH7ZJoCq6MEFZxxxzMs_W0OUktEEBXP_NXy356DPxYf8yPEYjGH4C-O--ZRTcauPwdwwKo-I7GkIfDhvbvN9IIRUKJU5dlQAAAAH62YR3AA"

app = Client("my_userbot11", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

async def process_reaction_list(client: Client, message: Message):
    """Memproses reaksi secara mendalam untuk memisahkan MA (🔥) dan SA (❤️)"""
    target_msg = message.reply_to_message
    pemberi_ma = [] # 🔥
    pemberi_sa = [] # ❤️

    try:
        # 1. Bypass MSG_ID_INVALID untuk Supergroup/Channel
        if message.chat.type in ["supergroup", "channel"]:
            channel_id = int(str(message.chat.id).replace("-100", ""))
            resolved_peer = await client.resolve_peer(message.chat.id)
            access_hash = getattr(resolved_peer, "access_hash", 0)
            chat_peer = InputPeerChannel(channel_id=channel_id, access_hash=access_hash)
        else:
            chat_peer = await client.resolve_peer(message.chat.id)
        
        # 2. Ambil list pereaksi mentah dari server Telegram
        raw_reply = await client.invoke(
            functions.messages.GetMessageReactionsList(
                peer=chat_peer,
                id=target_msg.id,
                limit=100
            )
        )
        
        # Buat mapping ID User ke Objek User agar mudah dicari
        users_map = {u.id: u for u in raw_reply.users}
        
        # 3. Iterasi setiap reaksi yang masuk
        if hasattr(raw_reply, "reactions"):
            for r in raw_reply.reactions:
                user_id = getattr(r.peer_id, "user_id", None)
                if not user_id:
                    continue
                    
                raw_user = users_map.get(user_id)
                if not raw_user:
                    continue
                
                # --- LOGIKA PENARIKAN USERNAME / DN (Sesuai Permintaan) ---
                username = None
                if getattr(raw_user, "username", None):
                    username = raw_user.username
                elif getattr(raw_user, "usernames", None):
                    for u in raw_user.usernames:
                        if getattr(u, "active", False) or getattr(u, "editable", False):
                            username = u.username
                            break
                
                # Prioritas: Pakai @username, jika tidak ada pakai Display Name (first_name)
                if username:
                    user_mention = f"@{username}"
                else:
                    user_mention = raw_user.first_name if raw_user.first_name else "No Name"
                
                # --- KLASIFIKASI EMOJI ---
                if isinstance(r.reaction, ReactionEmoji):
                    emoji = r.reaction.emoticon
                    if emoji == "🔥":
                        pemberi_ma.append(user_mention)
                    elif emoji == "❤️" or emoji == "❤️":
                        pemberi_sa.append(user_mention)

    except Exception as e:
        print(f"Error: {str(e)}")

    # Bersihkan duplikat
    pemberi_ma = list(set(pemberi_ma))
    pemberi_sa = list(set(pemberi_sa))
    
    return pemberi_ma, pemberi_sa


# ==================== COMMANDS ====================

@app.on_message(filters.command("done", prefixes=["/", "."]) & filters.group)
async def cmd_done(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Rep ke pesan yg ingin dihitung reactnya")
        return

    pemberi_ma, pemberi_sa = await process_reaction_list(client, message)
    
    if not pemberi_ma and not pemberi_sa:
        await message.reply_text("Gak ada react")
        return

    bagian_hasil = []
    if pemberi_ma:
        str_ma = " ".join(pemberi_ma)
        bagian_hasil.append(f"{str_ma} [{len(pemberi_ma)} MA]")
    if pemberi_sa:
        str_sa = " ".join(pemberi_sa)
        bagian_hasil.append(f"{str_sa} [{len(pemberi_sa)} SA]")
        
    teks_akhir = f"`{' '.join(bagian_hasil)}`"
    await message.reply_text(text=teks_akhir)


@app.on_message(filters.command("doni", prefixes=["/", "."]) & filters.group)
async def cmd_doni(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Rep ke pesan yg ingin dihitung reactnya")
        return

    pemberi_ma, pemberi_sa = await process_reaction_list(client, message)
    
    if not pemberi_ma and not pemberi_sa:
        await message.reply_text("Gak ada react")
        return

    bagian_doni = []
    if pemberi_ma:
        str_ma = ", ".join(pemberi_ma)
        bagian_doni.append(f"{str_ma} [{len(pemberi_ma)} MA]")
    if pemberi_sa:
        str_sa = ", ".join(pemberi_sa)
        bagian_doni.append(f"{str_sa} [{len(pemberi_sa)} SA]")
        
    teks_reaksi = " ".join(bagian_doni)

    # Template Estetik Louzhen 
    caption_template = (
        "```\n"
        "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n"
        "As osmanthus drifts gently upon an autumn breeze, several members of our "
        "household have already completed their subscriptions in accordance with our exchange. "
        f"{teks_reaksi} has subscribed yours. "
        "We would be most grateful if the aforementioned accounts could also be included "
        "within your mensive through [https://t.me/Louzhens/6] at your convenience. "
        "This allows us to maintain proper records and ensure that everything proceeds "
        "harmoniously between our households. 📨\n\n"
        "With regards,\n"
        "@HeavenOfLouzhen\n"
        "```"
    )
    
    await message.reply_text(text=caption_template)


print("⚡ Userbot Pyrogram /done & /doni Aktif (Username Fix)!")
app.run()
