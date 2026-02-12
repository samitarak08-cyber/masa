import g4f # مكتبة توفر وصول مجاني لـ ChatGPT
from telebot import types

def ask_ai(prompt):
    """دالة لجلب الجواب من ChatGPT"""
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo, # أو يمكنك استخدام gpt_4
            messages=[{"role": "user", "content": prompt}],
        )
        return response
    except Exception as e:
        return "عذراً يا عيني، عقلي معلق شوي.. حاول مرة ثانية! 🌒"

def handle_ai(bot, message):
    """دالة معالجة أمر 'ماسو'"""
    text = message.text
    
    # التأكد أن الرسالة تبدأ بكلمة 'ماسو'
    if text.startswith("ماسو"):
        # استخراج السؤال (حذف كلمة ماسو من النص)
        user_query = text.replace("ماسو", "").strip()
        
        if not user_query:
            bot.reply_to(message, "هلا عيوني؟ اسألني وش تبغى بعد كلمة ماسو.. مثلاً: ماسو كيف أسوي كيكة؟")
            return

        # إظهار حالة 'يتم الكتابة' عشان العضو يعرف أن البوت يفكر
        bot.send_chat_action(message.chat.id, 'typing')
        
        # جلب الجواب
        answer = ask_ai(user_query)
        
        # تنسيق الرد
        final_response = f"✨ **جواب ماسو الذكية:**\n\n{answer}\n\n┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉"
        
        bot.reply_to(message, final_response, parse_mode="Markdown")
      
