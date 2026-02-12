def handle_avatar(bot, message):
    text = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id

    # الأوامر اللي يستجيب لها الملف
    if text in ["صورتي", "افتاري", "الافتار", "بروفايلي"]:
        try:
            # جلب صور البروفايل الخاصة بالمستخدم
            photos = bot.get_user_profile_photos(user_id)
            
            if photos.total_count > 0:
                # أخذ آخر صورة وضعها المستخدم (أحدث أفتار) بأعلى دقة
                file_id = photos.photos[0][-1].file_id
                
                # إرسال الصورة مع نص حلو
                caption = f"✨ تفضل عيني هذي صورتك:\n👤 المستخدم: {message.from_user.first_name}"
                bot.send_photo(chat_id, file_id, caption=caption, reply_to_message_id=message.message_id)
            else:
                bot.reply_to(message, "❌ ما لقيت لك صورة بروفايل، شكلك حاط صورة افتراضية!")
        
        except Exception as e:
            bot.reply_to(message, "⚠️ حصل خطأ أثناء جلب الصورة، حاول مرة ثانية.")

    # ميزة إضافية: لو يبي يشوف صورة شخص ثاني بالرد
    elif text in ["صورته", "افتاره"] and message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        target_name = message.reply_to_message.from_user.first_name
        try:
            photos = bot.get_user_profile_photos(target_id)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                bot.send_photo(chat_id, file_id, caption=f"✨ هذي صورة {target_name}", reply_to_message_id=message.message_id)
            else:
                bot.reply_to(message, "❌ هالعضو مو حاط صورة!")
        except:
            bot.reply_to(message, "⚠️ تعذر جلب الصورة.")
          
