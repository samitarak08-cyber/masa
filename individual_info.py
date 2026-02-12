import json
import os
from bank import get_balance
from ranks import get_user_rank

def load_stats():
    if os.path.exists('stats.json'):
        with open('stats.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def handle_individual_commands(bot, message):
    text = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # 1. أمر بايو
    if text == "بايو":
        try:
            chat_member = bot.get_chat(user_id)
            bio = chat_member.bio if chat_member.bio else "ما عندك بايو يا عيني"
            bot.reply_to(message, f"📝 بايو بروفايلك:\n\n`{bio}`", parse_mode="Markdown")
        except:
            bot.reply_to(message, "⚠️ ما قدرت أسحب البايو، تأكد إنك مو مسوي له إخفاء.")

    # 2. أمر يوزري
    elif text == "يوزري":
        username = f"@{message.from_user.username}" if message.from_user.username else "ما عندك يوزر"
        bot.reply_to(message, f"👤 يوزرك هو: `{username}`", parse_mode="Markdown")

    # 3. أمر تفاعلي
    elif text == "تفاعلي":
        stats = load_stats()
        count = stats.get(str(chat_id), {}).get(str(user_id), 0)
        bot.reply_to(message, f"📊 مجموع رسائلك هنا: `{count}` رسالة")

    # 4. أمر فلوسي (إضافة للأمر اللي في ملف البنك)
    elif text == "فلوسي":
        money = get_balance(user_id)
        bot.reply_to(message, f"💰 رصيدك الحالي: `{money}` ريال")

    # 5. أمر رتبتي
    elif text == "رتبتي":
        rank = get_user_rank(chat_id, user_id)
        bot.reply_to(message, f"🎖 رتبتك في هذي المجموعة: **{rank}**")
        
    # 6. أمر ايدي (فقط الرقم)
    elif text == "ايديه":
        bot.reply_to(message, f"🆔 ايديك هو: `{user_id}`", parse_mode="Markdown")
      
