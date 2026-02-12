import json
import os

# ملف حفظ إعدادات القفل والفتح للجروبات
LOCKS_FILE = 'locks_data.json'

def load_locks():
    if os.path.exists(LOCKS_FILE):
        with open(LOCKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_locks(data):
    with open(LOCKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def handle_protection(bot, message):
    text = message.text
    chat_id = str(message.chat.id)
    user_id = message.from_user.id
    
    # تحميل الإعدادات
    locks = load_locks()
    if chat_id not in locks:
        locks[chat_id] = {"links": "open", "photos": "open", "forward": "open"}

    # --- أوامر القفل والفتح (للمدراء فقط) ---
    # ملاحظة: التحقق من الرتبة يفضل يكون في ملف الرتب، هنا سأضع الأساس
    if text in ["قفل الروابط", "تعطيل الروابط"]:
        locks[chat_id]["links"] = "lock"
        save_locks(locks)
        bot.reply_to(message, "🔒 تم قفل الروابط بنجاح.")
        
    elif text in ["فتح الروابط", "تفعيل الروابط"]:
        locks[chat_id]["links"] = "open"
        save_locks(locks)
        bot.reply_to(message, "🔓 تم فتح الروابط بنجاح.")

    elif text == "قفل الصور":
        locks[chat_id]["photos"] = "lock"
        save_locks(locks)
        bot.reply_to(message, "🔒 تم قفل إرسال الصور.")

    elif text == "فتح الصور":
        locks[chat_id]["photos"] = "open"
        save_locks(locks)
        bot.reply_to(message, "🔓 تم فتح إرسال الصور.")

    elif text == "قفل التوجيه":
        locks[chat_id]["forward"] = "lock"
        save_locks(locks)
        bot.reply_to(message, "🔒 تم قفل التوجيه (Forward).")

    elif text == "فتح التوجيه":
        locks[chat_id]["forward"] = "open"
        save_locks(locks)
        bot.reply_to(message, "🔓 تم فتح التوجيه.")

# --- دالة فحص الرسائل (Check Content) ---
def check_content(bot, message):
    chat_id = str(message.chat.id)
    locks = load_locks()
    
    if chat_id not in locks: return

    # فحص الروابط
    if locks[chat_id].get("links") == "lock":
        if "t.me/" in message.text or "http" in message.text:
            bot.delete_message(message.chat.id, message.message_id)
            # bot.send_message(message.chat.id, f"⚠️ ممنوع إرسال الروابط!") # اختيارية

    # فحص الصور
    if locks[chat_id].get("photos") == "lock":
        if message.content_type == 'photo':
            bot.delete_message(message.chat.id, message.message_id)

    # فحص التوجيه
    if locks[chat_id].get("forward") == "lock":
        if message.forward_from or message.forward_from_chat:
            bot.delete_message(message.chat.id, message.message_id)
