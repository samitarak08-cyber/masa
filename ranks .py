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
    chat_id, user_id = str(chat_id), int(user_id)
    
    # رتبة المطور (خارج التصنيف لأنك المبرمج)
    if user_id == DEV_ID:
        return "المطور"
    
    data = load_ranks()
    chat_data = data.get(chat_id, {})
    
    # جلب الرتبة من الملف، إذا مو موجود يكون "عضو"
    return chat_data.get(str(user_id), "عضو")

def handle_ranks(bot, message):
    text = message.text
    chat_id = str(message.chat.id)
    user_id = message.from_user.id
    user_rank = get_user_rank(chat_id, user_id)
    
    if not message.reply_to_message:
        return

    target_id = str(message.reply_to_message.from_user.id)
    target_name = message.reply_to_message.from_user.first_name
    
    data = load_ranks()
    if chat_id not in data: data[chat_id] = {}

    # مصفوفة الرتب للمقارنة (مين يقدر يرفع مين)
    hierarchy = ["عضو", "مميز", "ادمن", "مدير", "مالك", "مالك اساسي", "المطور"]

    def can_promote(promoter_rank, rank_to_give):
        try:
            return hierarchy.index(promoter_rank) > hierarchy.index(rank_to_give)
        except: return False

    # --- أوامر الرفع ---
    ranks_to_set = {
        "رفع مميز": "مميز",
        "رفع ادمن": "ادمن",
        "رفع مدير": "مدير",
        "رفع مالك": "مالك",
        "رفع مالك اساسي": "مالك اساسي"
    }

    if text in ranks_to_set:
        new_rank = ranks_to_set[text]
        if can_promote(user_rank, new_rank) or user_rank == "المطور":
            data[chat_id][target_id] = new_rank
            save_ranks(data)
            bot.reply_to(message, f"🎖 تم رفع {target_name} إلى رتبة **{new_rank}**!")
        else:
            bot.reply_to(message, "⚠️ رتبتك ما تسمح لك ترفع لهالرتبة!")

    # --- أوامر التنزيل ---
    if text.startswith("تنزيل") and text != "تنزيل":
        if user_rank in ["مالك اساسي", "مالك", "المطور"]:
            if target_id in data[chat_id]:
                del data[chat_id][target_id]
                save_ranks(data)
                bot.reply_to(message, f"❌ تم تنزيل {target_name} إلى رتبة عضو.")
            else:
                bot.reply_to(message, "👤 العضو رتبته أصلاً عضو!")
