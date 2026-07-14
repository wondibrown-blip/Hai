from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- MASUKKAN DATA API & SESSION KAMU DI SINI ---
API_ID =  38822592         # Ganti dengan API ID kamu (integer)
API_HASH = '9af6135950acf29e7038d48c435d1f0d' # Ganti dengan API Hash kamu (string)
SESSION_STRING = '1BVtsOLUBuzry0mdizKodbyidX8rGJVVXK1Jc38WJRD8-KUmQG2Xszj9rfdlab8rkSudnEX7DA2lmM78WU9X2rHZmQHJED339rCECidPzxT7dFzvtIgrwMQAoF-yp5lvgofOWAFy-BFBMwg581T_mOeqLudIbxaCOrla-p_iHXca9bUZikd0TU6K4Fi0HgpyC157d1N-JdEKB_UbVFrPqfOI6IVMVJI1TjciSoN3C-9IW-S1QDoJdgYrFinB9R8V_ZQ5bOzaDLrmigLvPzgHzHRFbV6hl4xMcmeE5wri1BL64oHYX2uHSB99SWd8Axch5uvbLU0FMHuK1y8F5KLmfaF_W_niUp10=' # Tempel kode Session String kamu di sini
# --------------------------------------

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r'^/(done|doni)$', outgoing=True))
async def hitung_reaksi(event):
    if not event.is_reply:
        await event.edit("Rep ke pesan yg ingin dihitung reactnya")
        return

    command = event.pattern_match.group(1).lower()
    reply_msg = await event.get_reply_message()
    chat = await event.get_input_chat()
    
    pemberi_ma = [] # React 🔥
    pemberi_sa = [] # React ❤️

    try:
        async for reaction in client.iter_reaction_users(chat, reply_msg.id):
            user = reaction.user
            if user.username:
                user_mention = f"@{user.username}"
            else:
                user_mention = f"[{user.first_name}](tg://user?id={user.id})"

            emoji = reaction.reaction
            
            if emoji == "🔥":
                pemberi_ma.append(user_mention)
            elif emoji == "❤️" or emoji == "♥️":
                pemberi_sa.append(user_mention)
                
    except Exception as e:
        await event.edit(f"❌ *Error {e}")
        return

    # Jika sama sekali tidak ada react MA maupun SA
    if not pemberi_ma and not pemberi_sa:
        await event.edit("Gak ada react")
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
            
        # Gabungkan dan bungkus dengan `agar menjadi mono
        teks_akhir = f"`{' '.join(bagian_hasil)}`"
        await event.edit(teks_akhir, parse_mode='markdown')
        
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

        # Seluruh template dibungkus di dalam triple backtick (```) agar satu pesan full menjadi mono
        template_pesan = (
            "```\n"
            "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ\n"
            "As osmanthus drifts gently upon an autumn breeze, several members of our "
            "household have already completed their subscriptions in accordance with our exchange. "
            f"{teks_reaksi} has subscribed yours. "
            "We would be most grateful if the aforementioned accounts could also be included "
            "within your mensive through https://t.me/Louzhens/6 at your convenience. "
            "This allows us to maintain proper records and ensure that everything proceeds "
            "harmoniously between our households. 📨\n\n"
            "With regards,\n"
            "@HeavenOfLouzhen\n"
            "```"
        )
        await event.edit(template_pesan, parse_mode='markdown', link_preview=False)

print("Userbot mono version aktif!")
client.start()
client.run_until_disconnected()
