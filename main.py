import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw import functions
from pyrogram.raw.types import InputPeerChannel, ReactionEmoji

# ==================== CONFIGURATION ====================
API_ID =  38822592         # Ganti dengan API ID kamu (integer)
API_HASH = '9af6135950acf29e7038d48c435d1f0d' # Ganti dengan API Hash kamu (string)
SESSION_STRING = 'BQJQYsAACJjHiakcg1k0yU9DnqThrewI6b5v6wZeJ68yoKMTefoHuFL0vcILBdFndm4TT2QvXaMC9PHJtonsAAtOmai2OKr8bX_HZFPrN1fN9fclxwET6DbALIfs0PH4pUcZJWsAyQa_Ye4wuLHcsSgLS_ny-M_E5Ce0F9ooAOMY7LC3PdEtHyzfRCxS1MG36hYRVSZu2yoGm551qj-z6w6DZFrpmj_8HaH6ScuAHA88oenTrbGMOjqFBpEEgZvRWqJnqT41TuCJ6aVdHgcTHFAYI4oBpfAGbhC4gDF21KDE1TdnOxlstIStevCagDlv3W53U4w7lX1O3d_vZohNWde1flca0QAAAAHUe5liAA' # Tempel kode Session String kamu di sini

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
                
                # --- LOGIKA PENARIKAN USERNAME / DN ---
                username = None
                if getattr(raw_user, "username", None):
                    username = raw_user.username
                elif getattr(raw_user, "usernames", None):
                    for u in raw_user.usernames:
                        if getattr(u, "active", False) or getattr(u, "editable", False):
                            username = u.username
                            break
                
                if username:
                    user_mention = f"@{username}"
                else:
                    user_mention = raw_user.first_name if raw_user.first_name else "No Name"
                
                # --- PERBAIKAN FILTER EMOJI (Deteksi Multi-Karakter Love) ---
                if isinstance(r.reaction, ReactionEmoji):
                    emoji = r.reaction.emoticon
                    
                    if emoji == "🔥":
                        pemberi_ma.append(user_mention)
                    # Mendeteksi segala jenis variasi emoji Love merah di Telegram
                    elif emoji in ["❤️", "♥️", "\u2764\ufe0f", "\u2764"]:
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
