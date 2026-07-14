from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetMessageReactionsListRequest
from telethon.tl.types import ReactionEmoji

# --- DATA API & SESSION KAMU ---
API_ID = 38822592          
API_HASH = '9af6135950acf29e7038d48c435d1f0d' 
SESSION_STRING = '1BVtsOLUBuzry0mdizKodbyidX8rGJVVXK1Jc38WJRD8-KUmQG2Xszj9rfdlab8rkSudnEX7DA2lmM78WU9X2rHZmQHJED339rCECidPzxT7dFzvtIgrwMQAoF-yp5lvgofOWAFy-BFBMwg581T_mOeqLudIbxaCOrla-p_iHXca9bUZikd0TU6K4Fi0HgpyC157d1N-JdEKB_UbVFrPqfOI6IVMVJI1TjciSoN3C-9IW-S1QDoJdgYrFinB9R8V_ZQ5bOzaDLrmigLvPzgHzHRFbV6hl4xMcmeE5wri1BL64oHYX2uHSB99SWd8Axch5uvbLU0FMHuK1y8F5KLmfaF_W_niUp10=' 
# --------------------------------------

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r'^/(done|doni)$'))
async def hitung_reaksi(event):
    if not event.is_reply:
        await event.reply("Rep pesan yg ingin dihitung reactnya")
        return

    command = event.pattern_match.group(1).lower()
    reply_msg = await event.get_reply_message()
    
    pemberi_ma = [] # React 🔥
    pemberi_sa = [] # React ❤️

    try:
        # Menggunakan Raw API Telethon untuk mengambil daftar pereaksi
        # Limit maksimal dari Telegram adalah 100 per request
        reaction_list = await client(GetMessageReactionsListRequest(
            peer=event.chat_id,
            id=reply_msg.id,
            limit=100
        ))
        
        # Buat kamus (dictionary) untuk mencocokkan ID User dengan datanya
        users_dict = {u.id: u for u in reaction_list.users}
        
        # Iterasi setiap detail reaksi
        for r in reaction_list.reactions:
            user_id = r.peer_id.user_id
            user = users_dict.get(user_id)
            
            if not user:
                continue
                
            # Tentukan format mention
            if user.username:
                user_mention = f"@{user.username}"
            else:
                user_mention = f"[{user.first_name}](tg://user?id={user.id})"
            
            # Cek emojinya
            if isinstance(r.reaction, ReactionEmoji):
                emoji = r.reaction.emoticon
                if emoji == "🔥":
                    pemberi_ma.append(user_mention)
                elif emoji == "❤️" or emoji == "♥️":
                    pemberi_sa.append(user_mention)
                    
    except Exception as e:
        await event.reply(f"❌ Error: {e}")
        return

    # Jika sama sekali tidak ada react MA maupun SA
    if not pemberi_ma and not pemberi_sa:
        await event.reply("Gak ada react")
        return

    # --- PROSES PERINTAH /done ---
    if command == "done":
        bagian_hasil = []
        if pemberi_ma:
            str_ma = " ".join(pemberi_ma)
            bagian_hasil.append(f"{str_ma} ({len(pemberi_ma)} MA)")
        if pemberi_sa:
            str_sa = " ".join(pemberi_sa)
            bagian_hasil.append(f"{str_sa} ({len(pemberi_sa)} SA)")
            
        teks_akhir = f"`{' '.join(bagian_hasil)}`"
        await event.reply(teks_akhir, parse_mode='markdown')
        
    # --- PROSES PERINTAH /doni ---
    elif command == "doni":
        bagian_doni = []
        if pemberi_ma:
            str_ma = ", ".join(pemberi_ma)
            bagian_doni.append(f"{str_ma} ({len(pemberi_ma)} MA)")
        if pemberi_sa:
            str_sa = ", ".join(pemberi_sa)
            bagian_doni.append(f"{str_sa} ({len(pemberi_sa)} SA)")
            
        teks_reaksi = " ".join(bagian_doni)

        template_pesan = (
            "```\n"
            "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n"
            "As osmanthus drifts gently upon an autumn breeze, several members of our "
            "household have already completed their subscriptions in accordance with our exchange. "
            f"{teks_reaksi} has subscribed yours. "
            "We would be most grateful if the aforementioned accounts could also be included "
            "within your mensive through [https://t.me/Louzhens/6](https://t.me/Louzhens/6) at your convenience. "
            "This allows us to maintain proper records and ensure that everything proceeds "
            "harmoniously between our households. 📨\n\n"
            "With regards,\n"
            "@HeavenOfLouzhen\n"
            "```"
        )
        await event.reply(template_pesan, parse_mode='markdown', link_preview=False)

print("Userbot Publik (V1 Fix) Aktif!")
client.start()
client.run_until_disconnected()
