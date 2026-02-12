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
    """جلب رتبة التسلية للشخص"""
    data = load_fun_ranks()
    return data.get(str(user_id), "لا يوجد لقب")

def handle_fun_promotion(bot, message):
    text = message.text
    chat_id = str(message.chat.id)
    
    # التأكد أن الأمر (رفع + لقب) وبالرد على الشخص
    if text.startswith("رفع ") and message.reply_to_message:
        # استخراج اللقب (مثلاً: رفع مطنوخ -> يأخذ كلمة مطنوخ)
        title = text.replace("رفع ", "").strip()
        
        # قائمة الرتب الإدارية عشان ما نلخبط بينهم
        admin_ranks = ["مدير", "ادمن", "مميز", "مالك", "مالك اساسي"]
        if title in admin_ranks:
            return # نترك المعالجة لملف ranks.py

        target_id = str(message.reply_to_message.from_user.id)
        target_name = message.reply_to_message.from_user.first_name
        
        data = load_fun_ranks()
        data[target_id] = title
        save_fun_ranks(data)
        
        bot.reply_to(message, f"🎭 تم منح {target_name} رتبة تسلية: **{title}**")

    # أمر حذف رتبة التسلية
    elif text == "تنزيل الكل" and message.reply_to_message:
        target_id = str(message.reply_to_message.from_user.id)
        data = load_fun_ranks()
        if target_id in data:
            del data[target_id]
            save_fun_ranks(data)
            bot.reply_to(message, "✨ تم حذف ألقاب التسلية للعضو.")
          
