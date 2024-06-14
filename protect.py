from dotenv import load_dotenv
import os

from asyncio import sleep
from pyrogram import Client, filters

from pyrogram.types import EmojiStatus, MessageEntity
from pyrogram import types
from pyrogram.enums import MessageEntityType, ChatType
from pyrogram.raw import functions
from pyrogram.errors.exceptions.bad_request_400 import ReactionInvalid, MessageTooLong *



@PY.UBOT("adduser")
async def add_user_to_blacklist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(f"{batal}**gunakan format** : `adduser` **user id atau balas ke pesan untuk menambahkan ke daftar antigcast {Q}**", quote=True)
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        user_id = int(m.command[1])

    user_ids = await get_user_ids(c.me.id)
    if user_id not in user_ids:
        user_ids.append(user_id)
        await user_collection.update_one({"_id": c.me.id}, {"$set": {"user_dia": user_ids}}, upsert=True)
        await m.reply_text(f"{Q}**user dengan id** `{user_id}` **telah ditambahkan ke daftar antigcast** {dn}", quote=True)
    else:
        await m.reply_text(f"{dn}**user tersebut sudah ada dalam daftar antigcast {Q}**", quote=True)

@PY.UBOT("listuser")
async def display_blacklist(client, message):
    user_ids = await get_user_ids(client.me.id)
    await message.reply_text(f"{dftr} ini hasilnya : `{user_ids}`\n", quote=True)

@PY.UBOT("rmuser")
async def remove_user_from_blacklist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(f"{batal}**gunakan format** : `rmuser` **user id atau balas ke pesan untuk menghapus dari daftar antigcast {Q}**", quote=True)
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        user_id = int(m.command[1])

    user_ids = await get_user_ids(c.me.id)
    if user_id in user_ids:
        user_ids.remove(user_id)
        await user_collection.update_one({"_id": c.me.id}, {"$set": {"user_dia": user_ids}}, upsert=True)
        await m.reply_text(f"{Q}**user dengan id** `{user_id}` **telah dihapus dalam daftar antigcast** {dn}", quote=True)
    else:
        await m.reply_text(f"{Q}**user tersebut tidak ada dalam daftar antigcast {gagal}**", quote=True)

@PY.UBOT("lihat")
async def checkstatus(client, message):
    cek = await get_blacklist_status(client.me.id)
    if cek == True:
        await message.reply_text(f"{Q}**anda sudah mengaktifkan antigcast**{dn}", quote=True)
    else:
        await message.reply_text(f"{Q}**anda belum mengaktifkan antigcast**{gagal}", quote=True)        

@PY.UBOT("on")
async def enable_blacklist(c, m):
    await set_blacklist_status(c.me.id, True)
    await m.reply_text(f"{Q}**antigcast user berhasil di aktifkan** {on}", quote=True)

@PY.UBOT("off")
async def disable_blacklist(c, m):
    await set_blacklist_status(c.me.id, False)
    await m.reply_text(f"{Q}**antigcast user berhasil di matikan** {off}", quote=True)

@PY.UBOT("addgp")
async def add_group_to_antigcast(c, m):
    type = (ChatType.GROUP, ChatType.SUPERGROUP)

    if m.chat.type not in type:
        await m.reply_text(f"{gagal}gunakan fitur ini di grup!")
        return

    user_id = m.chat.id
    chat_ids = await get_chat_ids(c.me.id)
    if user_id not in chat_ids:
        chat_ids.append(user_id)
        await gc.update_one({"_id": c.me.id}, {"$set": {"grup": chat_ids}}, upsert=True)
        await m.reply_text(f"{Q}**grup dengan id** `{user_id}` **telah ditambahkan ke daftar antigcast** {dn}", quote=True)
    else:
        await m.reply_text(f"{dn}**grup tersebut sudah ada dalam daftar antigcast {Q}**", quote=True)

@PY.UBOT("rmgp")
async def remove_group_from_antigcast(c, m):
    type = (ChatType.GROUP, ChatType.SUPERGROUP)
    if m.chat.type not in type:
        await m.reply_text(f"{gagal} Gunakan fitur ini di grup atau berikan ID grup", quote=True)
        return

    chat_id = None
    if len(m.command) >= 2:
        try:
            chat_id = int(m.command[1])
        except ValueError:
            await m.reply_text(f"{gagal} ID grup tidak valid", quote=True)
            return

    if not chat_id:
        chat_id = m.chat.id

    chat_ids = await get_chat_ids(c.me.id)
    if chat_id in chat_ids:
        chat_ids.remove(chat_id)
        await gc.update_one({"_id": c.me.id}, {"$set": {"grup": chat_ids}}, upsert=True)
        await m.reply_text(f"{Q} Grup dengan ID {chat_id} telah dihapus dari daftar antigcast {dn}", quote=True)
    else:
        await m.reply_text(f"{Q} Grup dengan ID {chat_id} tidak ada dalam daftar antigcast {gagal}", quote=True)


@PY.UBOT("listgp")
async def display_antigcast(c, m):
    user_ids = await get_chat_ids(c.me.id)
    await m.reply_text(f"{dftr}**daftar grup antigcast** : `{user_ids}` \n", quote=True)

@PY.UBOT("bl")
async def add_pesan(c, m):
    _rply = m.reply_to_message
    if not _rply:
        await m.reply(f"mohon balas ke pengguna")
        return    
    user_text = _rply.text
    msg_ids = await get_msg_ids(c.me.id)
    if user_text not in msg_ids:
        msg_ids.append(user_text)
        await psnz.update_one({"_id": c.me.id}, {"$set": {"msg_text": msg_ids}}, upsert=True)
        sukses = await m.reply_text(f"pesan {user_text} berhasil di tambahkan ke database{dn}", quote=True)
        await _rply.delete()
        await purge(m)
        await sukses.delete()
    else:
        x = await m.reply_text(f"pesan sudah ada di dalam database{gagal}", quote=True)
        await asyncio.sleep(0.5)
        await x.delete()

@PY.UBOT("strdb")
async def strdb(client, message):
    pesan = await get_msg_ids(client.me.id)
    try:
        await message.reply_text(pesan)
    except MessageTooLong:
        with open("db.txt", "a", encoding="utf-8") as file:
            file.write(f"{pesan}\n")
        kirim = await message.reply_document(db.txt)
        if kirim:
            os.remove("db.txt")

@PY.UBOT("rmkat")
async def remove_kata_from_blacklist(c, m):
    if len(m.command) != 2 and not m.reply_to_message:
        await m.reply_text(f"{batal}**gunakan format** : `rmkat` **user id atau balas ke pesan untuk menghapus dari daftar antigcast {Q}**", quote=True)
        return

    if m.reply_to_message:
        user_id = m.reply_to_message.text
    else:
        user_id = " ".join(m.command[1:])

    user_ids = await get_msg_ids(c.me.id)
    if user_id in user_ids:
        user_ids.remove(user_id)
        await psnz.update_one({"_id": c.me.id}, {"$set": {"msg_text": user_ids}}, upsert=True)
        await m.reply_text(f"{Q}**berhasil menghapus** `{user_id}` **dari daftar kata antigcast** {dn}", quote=True)
    else:
        await m.reply_text(f"{Q}**kata tersebut tidak ada dalam daftar antigcast {gagal}**", quote=True)


@Bot.on_message(filters.group & ~filters.private & ~filters.me)
async def delete_messages(client, message):
    try:
        chat_ids = await get_chat_ids(client.me.id)
        if message.chat.id not in chat_ids:
            return    
        blacklist_status = await get_blacklist_status(client.me.id)
        if blacklist_status:
            sys = client.me.id
            user_ids = await get_user_ids(sys)
            user_msg = await get_msg_ids(sys)
            if message.from_user.id in user_ids:
                await message.delete()
            else:
                try:
                    for pattern in user_msg:
                        if re.search(pattern, message.text, re.IGNORECASE):
                            await message.delete()
                            break
                except:
                    pass
    except:
        pass
