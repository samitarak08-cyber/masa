import random
from telebot import types
import json
import os

# قائمة كلام حلو عشوائي
SWEET_WORDS = [
    "يا زين هالطله والله ✨", "جمالك يغطي على الكل 💅", "منور الجروب بوجودك يا عسل 🍯",
    "نجم ساطع في سماءنا 🌟", "يا حظنا فيك وبوجودك 🤍", "طلتك تجيب السعادة 🌸"
]

def load_stats():
    if os.path.exists('stats.json'):
        with open('stats.json', 'r') as f: return json.load(f)
    return {}

def get_ranking(chat_id, user_id):
    """حساب ترتيب الشخص بين المتفاعلين"""
    stats = load_stats()
    chat_stats = stats.get(str(chat_id), {})
    if not chat_stats: return "الأول"
    
    # ترتيب المستخدمين حسب عدد الرسائل
    sorted_users = sorted(chat_stats.items(), key=lambda x: x[1], reverse=True)
    for index, (uid, count) in enumerate(sorted_users):
        if uid == str(user_id):
            return index + 1
    return "غير مصنف"

def handle_id(bot, message, user_rank, fun_rank):
    text = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "لا يوجد"
    
    if text in ["ايدي", "ا", "id"]:
        # 1. جلب عدد الرسائل
        stats = load_stats()
        count = stats.get(str(chat_id), {}).get(str(user_id), 0)
        
        # 2. جلب الترتيب
        rank_num = get_ranking(chat_id, user_id)
        
        # 3. جلب البايو
        try:
            chat_member = bot.get_chat(user_id)
            bio = chat_member.bio if chat_member.bio else "لا يوجد بايو"
        except:
            bio = "مخفي أو غير متوفر"

        # 4. تنسيق الرسالة
        caption = f"""
✷ {random.choice(SWEET_WORDS)}
┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉
✿ اسمك: {user_name}
❀ يوزرك: {username}
✿ ايديك: `{user_id}`
❀ رتبتك: {user_rank}
🎭 لقبك: {fun_rank}
✿ تفاعلك: {count} رسالة
❀ ترتيبك: {rank_num}
✿ بايو: {bio}
┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉
        """

        # 5. جلب الأفتار وإرسال الآيدي
        try:
            photos = bot.get_user_profile_photos(user_id)
            if photos.total_count > 0:
                bot.send_photo(chat_id, photos.photos[0][-1].file_id, caption=caption, parse_mode="Markdown")
            else:
                bot.reply_to(message, caption, parse_mode="Markdown")
        except:
            bot.reply_to(message, caption, parse_mode="Markdown")
                             
