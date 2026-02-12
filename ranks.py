import json
import os
from config import DEV_ID

RANKS_FILE = 'ranks_data.json'

def load_ranks():
    if os.path.exists(RANKS_FILE):
        with open(RANKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_ranks(data):
    with open(RANKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user_rank(chat_id, user_id):
    """دالة لمعرفة رتبة العضو في الجروب"""
    chat_id, user_id = str(chat_id), int(user_id)
    
    # 1. رتبة المطور (ثابتة من ملف config)
    if user_id == DEV_ID:
        return "مطور"
    
    # تحميل الرتب من الملف
    data = load_ranks()
    chat_data = data.get(chat_id, {})
    
    # 2. رتبة المالك أو الرتب المرفوعة بالبوت
    if str(user_id) in chat_data:
        return chat_data[str(user_id)]
    
    return "عضو"

def handle_ranks(bot, message):
    text = message.text
    chat_id = str(message.chat.id)
    
    # التأكد أن الشخص اللي يستخدم الأمر هو (مطور أو مالك أو مدير)
    user_rank = get_user_rank(message.chat.id, message.from_user.id)
    
    if not message.reply_to_message:
        return

    target_id = str(message.reply_to_message.from_user.id)
    target_name = message.reply_to_message.from_user.first_name
    
    data = load_ranks()
    if chat_id not in data: data[chat_id] = {}

    # --- أوامر الرفع والتنزيل ---
    if text == "رفع مدير" and user_rank in ["مطور", "مالك"]:
        data[chat_id][target_id] = "مدير"
        save_ranks(data)
        bot.reply_to(message, f"🎖 تم رفع {target_name} مدير بنجاح!")

    elif text == "تنزيل مدير" and user_rank in ["مطور", "مالك"]:
        if target_id in data[chat_id]:
            del data[chat_id][target_id]
            save_ranks(data)
            bot.reply_to(message, f"❌ تم تنزيل المدير {target_name}.")

    elif text == "رفع ادمن" and user_rank in ["مطور", "مالك", "مدير"]:
        data[chat_id][target_id] = "ادمن"
        save_ranks(data)
        bot.reply_to(message, f"🎖 تم رفع {target_name} ادمن بنجاح!")

    elif text == "رفع مالك" and user_rank == "مطور":
        data[chat_id][target_id] = "مالك"
        save_ranks(data)
        bot.reply_to(message, f"🎖 تم رفع {target_name} مالك الجروب!")
  
