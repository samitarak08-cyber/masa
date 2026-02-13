import telebot
import json
import os

# --- الإعدادات الأساسية ---
TOKEN = "8280371843:AAGSN3yBIkKWT8uXpC0JxsAPCGZHpx6wFPU"
DEV_ID = 8436415733

# --- استيراد الملفات (تأكدي أن الأسماء في GitHub مطابقة تماماً) ---
import responses, games, bank, ai_logic, whisper, protection, fun_ranks, identity, avatar, individual_info, bot_commands
import level        # ملف الرتب (level.py)
import top_members  # الملف اللي سويتيه الحين (top_members.py)

bot = telebot.TeleBot(TOKEN)

def update_stats(chat_id, user_id):
    stats_file = 'stats.json'
    if os.path.exists(stats_file):
        with open(stats_file, 'r', encoding='utf-8') as f:
            try: stats = json.load(f)
            except: stats = {}
    else: stats = {}
    c_id, u_id = str(chat_id), str(user_id)
    if c_id not in stats: stats[c_id] = {}
    stats[c_id][u_id] = stats[c_id].get(u_id, 0) + 1
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

@bot.message_handler(func=lambda m: True, content_types=['text', 'photo', 'video', 'forward', 'document'])
def main_router(message):
    if message.chat.type in ['group', 'supergroup']:
        update_stats(message.chat.id, message.from_user.id)
        
        try:
            bot_member = bot.get_chat_member(message.chat.id, bot.get_me().id)
            if bot_member.status != 'administrator':
                bot.send_message(message.chat.id, "❌ لازم أكون مشرف عشان أقدر أخدمكم! بطلع الآن.")
                bot.leave_chat(message.chat.id)
                return
        except:
            pass

    protection.check_content(bot, message)

    if not message.text: return

    # توزيع المهام على جميع الملفات
    try:
        protection.handle_protection(bot, message)
        level.handle_ranks(bot, message) 
        fun_ranks.handle_fun_promotion(bot, message)
        bank.handle_bank(bot, message)
        ai_logic.handle_ai(bot, message)
        whisper.handle_whisper(bot, message)
        top_members.handle_top(bot, message) # تفعيل ملف أفضل الأعضاء
        avatar.handle_avatar(bot, message)
        individual_info.handle_individual_commands(bot, message)
        bot_commands.handle_commands_display(bot, message)
        responses.handle_responses(bot, message)
    except Exception as e:
        print(f"Error in handlers: {e}")

    if message.text in ["ايدي", "ا", "id"]:
        user_rank = level.get_user_rank(message.chat.id, message.from_user.id)
        fun_r = fun_ranks.get_user_fun_rank(message.from_user.id)
        identity.handle_id(bot, message, user_rank, fun_r)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("show_w_"):
        whisper.handle_whisper_callback(bot, call)

if __name__ == "__main__":
    print("✅ Masa Bot is Fully Online!")
    bot.infinity_polling()
          
