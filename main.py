import telebot
import json
import os

# --- الإعدادات التي زودتني بها ---
TOKEN = "8280371843:AAGSN3yBIkKWT8uXpC0JxsAPCGZHpx6wFPU"
DEV_ID = 8436415733
# ------------------------------

# استيراد كافة الملفات البرمجية التي صنعناها
import responses
import games
import bank
import ai_logic
import whisper
import protection
import ranks
import fun_ranks
import identity
import top_members
import avatar
import individual_info
import bot_commands

# تشغيل البوت باستخدام التوكن
bot = telebot.TeleBot(TOKEN)

# دالة تحديث إحصائيات الرسائل (لنظام المتفاعلين)
def update_stats(chat_id, user_id):
    stats_file = 'stats.json'
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as f:
            try:
                stats = json.load(f)
            except: stats = {}
    else:
        stats = {}

    c_id, u_id = str(chat_id), str(user_id)
    if c_id not in stats: stats[c_id] = {}
    stats[c_id][u_id] = stats[c_id].get(u_id, 0) + 1

    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

# المعالج الرئيسي لجميع رسائل المجموعات والخاص
@bot.message_handler(func=lambda m: True, content_types=['text', 'photo', 'video', 'forward', 'document'])
def main_router(message):
    # 1. تحديث التفاعل (فقط في المجموعات)
    if message.chat.type in ['group', 'supergroup']:
        update_stats(message.chat.id, message.from_user.id)

    # 2. فحص نظام الحماية (قفل الروابط، الصور، الخ)
    protection.check_content(bot, message)

    # إذا كانت الرسالة ليست نصية، نتوقف هنا
    if not message.text:
        return

    # 3. تشغيل كافة ملفات البوت بالترتيب الصحيح
    protection.handle_protection(bot, message)      # أوامر المدير للقفل والفتح
    ranks.handle_ranks(bot, message)               # رفع وتنزيل الإدارة
    fun_ranks.handle_fun_promotion(bot, message)    # ألقاب التسلية (رفع مطنوخ..)
    bank.handle_bank(bot, message)                  # نظام البنك والراتب
    ai_logic.handle_ai(bot, message)                # ذكاء ماسو (AI)
    whisper.handle_whisper(bot, message)            # نظام الهمس السري
    top_members.handle_top(bot, message)            # توب المتفاعلين
    avatar.handle_avatar(bot, message)              # أوامر صورتي وافتاري
    individual_info.handle_individual_commands(bot, message) # بايو، يوزري، تفاعلي
    bot_commands.handle_commands_display(bot, message) # قائمة الأوامر (م1)
    responses.handle_responses(bot, message)        # الردود الآلية والكلمات

    # 4. معالجة أمر "الايدي" المطور (عرض البيانات الكاملة بالأفتار)
    if message.text in ["ايدي", "ا", "id"]:
        user_rank = ranks.get_user_rank(message.chat.id, message.from_user.id)
        fun_r = fun_ranks.get_user_fun_rank(message.from_user.id)
        identity.handle_id(bot, message, user_rank, fun_r)

# معالج الأزرار (ضروري لنظام الهمس التفاعلي)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("show_w_"):
        whisper.handle_whisper_callback(bot, call)

# تشغيل البوت والاستمرار في العمل
if __name__ == "__main__":
    print("---------------------------------")
    print("✅ بوت ماسا يعمل الآن بنجاح!")
    print(f"👤 المطور الرئيسي: {DEV_ID}")
    print("---------------------------------")
    bot.infinity_polling()
