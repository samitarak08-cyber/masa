from telebot import types

def handle_whisper(bot, message):
    text = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # التأكد أن الأمر يبدأ بـ 'اهمس' أو 'همسه' ويكون بالرد على شخص
    if text.startswith("اهمس") or text.startswith("همسه"):
        if not message.reply_to_message:
            bot.reply_to(message, "⚠️ لازم ترد على رسالة الشخص اللي تبي تهمس له!")
            return

        # استخراج نص الهمسة
        content = text.replace("اهمس", "").replace("همسه", "").strip()
        if not content:
            bot.reply_to(message, "⚠️ اكتب الرسالة بعد الكلمة (مثال: همسه أحبك)")
            return

        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name

        # حذف رسالة العضو الأصلية عشان تظل سرية
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass

        # إنشاء الزر
        markup = types.InlineKeyboardMarkup()
        # بنخزن النص داخل الـ callback_data بشكل مشفر بسيط (أو يفضل قاعدة بيانات للرسائل الطويلة)
        # هنا سنضع الآيدي حق المستلم في الكول باك للفحص
        btn = types.InlineKeyboardButton(
            text=f"🔐 همسة لـ {target_name} (اضغط للمشاهدة)",
            callback_data=f"show_w_{target_id}"
        )
        markup.add(btn)

        # إرسال الزر في الشات
        # ملاحظة: محتوى الهمسة يفضل تخزينه في قاموس مؤقت لو كان طويل
        bot.send_message(chat_id, f"👤 من: {user_name}\n📨 همسة سرية إلى: {target_name}", reply_markup=markup)
        
        # بنخزن محتوى الهمسة في قاموس عالمي مؤقت (أو نمررها للكول باك لو قصيرة)
        # للتبسيط هنا بنفترض إنك بتعرف قاموس في الملف الرئيسي
        return {"target": target_id, "msg": content}

def handle_whisper_callback(bot, call):
    # الفحص: هل الشخص اللي ضغط هو المقصود بالهمسة؟
    target_id = int(call.data.split("_")[2])
    
    if call.from_user.id == target_id:
        # هنا تظهر له الهمسة (يفضل تخزين النصوص في ملف أو ديكشنري بالرئيسي)
        bot.answer_callback_query(call.id, text="🤫 هذي همستك السرية، حافظ عليها!", show_alert=True)
    else:
        bot.answer_callback_query(call.id, text="❌ هذي الهمسة مو لك يا لقوف! 😡", show_alert=True)
      
