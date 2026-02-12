import json
import os

FUN_DATA_FILE = 'fun_ranks_data.json'

def load_fun_ranks():
    if os.path.exists(FUN_DATA_FILE):
        with open(FUN_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_fun_ranks(data):
    with open(FUN_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user_fun_rank(user_id):
    data = load_fun_ranks()
    return data.get(str(user_id), "عضو متواضع ✨")

def handle_fun_promotion(bot, message):
    text = message.text
    
    # ميزة الرفع الحر (أي شخص يقدر يرفع نفسه أو غيره)
    if text.startswith("رفع ") and len(text.split()) > 1:
        # استخراج اللقب المطلوب
        new_title = text.replace("رفع ", "").strip()
        
        # حماية بسيطة: نمنعهم من رفع رتب إدارية حقيقية
        protected_ranks = ["مدير", "ادمن", "مالك", "مطور", "مالك اساسي", "مميز"]
        if new_title in protected_ranks:
            bot.reply_to(message, "❌ هذي رتبة إدارية يا نصاب، ما تقدر ترفعها لنفسك!")
            return

        # إذا رفع بالرد على شخص
        if message.reply_to_message:
            target_id = str(message.reply_to_message.from_user.id)
            target_name = message.reply_to_message.from_user.first_name
            data = load_fun_ranks()
            data[target_id] = new_title
            save_fun_ranks(data)
            bot.reply_to(message, f"🤣 أبشر، تم منح {target_name} لقب: **{new_title}**")
        
        # إذا كتب "رفع [اللقب]" بدون رد، يرفع نفسه
        else:
            user_id = str(message.from_user.id)
            data = load_fun_ranks()
            data[user_id] = new_title
            save_fun_ranks(data)
            bot.reply_to(message, f"🎖️ كفو، الحين رتبتك صارت: **{new_title}**")

    # أمر حذف اللقب
    elif text == "حذف لقبي":
        user_id = str(message.from_user.id)
        data = load_fun_ranks()
        if user_id in data:
            del data[user_id]
            save_fun_ranks(data)
            bot.reply_to(message, "✅ تم حذف لقبك بنجاح.")
