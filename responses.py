import random

# --- قائمة الردود ---

MASA_LIST = [
    "عيون ماسا", "سمي يعيوني", "تفضللل", "حبيتتتت قال ماسا",
    "لا يناديني حد بعدك يعمري", "احبك 👈🏻👉🏻", "يعمرييييييي"
]

BOT_LIST = [
    "بوت وش؟", "م ا س ا وين الصعب؟!!", "اسمي ماسا يا عم",
    "بدعي عليك تصير بوت!!!", "لا تحكي وياي", "ترا بزعل!!", "عقوبال لك"
]

SALAM_LIST = [
    "وعليكم السلام حياك الله", "وعليكم السلام يوههه طل القمر",
    "وعليكم السلام نورتنا", "وعليكم السلام يعيوني",
    "وعليكم السلام والله زمان عنك", "وعليكم السلام"
]

LOVE_LIST = [
    "احبك الله في الذي احببتني فيه 🤍", "يعمرييي",
    "الله يديمكم لبعض 🌸", "حبيتتتتكمم"
]

BYE_LIST = ["لاءءء ضل معانا بالله", "ترا الملل بدونك", "وين رايح ارجع...", "تعااا"]

OUT_LIST = ["الله معو", "وين تطلع ؟؟", "ضل الجو ما يحلى بدونك", "وين وين؟"]

HI_LIST = ["هايات يعيوني", "هايي", "وش هاي قول السلام عليكم"]

# --- دالة معالجة الردود الذكية ---

def handle_text_responses(bot, message):
    text = message.text.strip()

    if text == "ماسا":
        bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji("🎉")])
        bot.reply_to(message, random.choice(MASA_LIST))

    elif text == "بوت":
        bot.reply_to(message, random.choice(BOT_LIST))

    elif text == "السلام عليكم":
        bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji("❤️")])
        bot.reply_to(message, random.choice(SALAM_LIST))

    elif text == "احلف":
        bot.reply_to(message, random.choice(["والله", "تراه يكذب مافي داعي يحلف"]))

    elif text == "احبك":
        bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji("❤️")])
        bot.reply_to(message, random.choice(LOVE_LIST))

    elif text == "باي":
        bot.reply_to(message, random.choice(BYE_LIST))

    elif text == "بطلع":
        bot.reply_to(message, random.choice(OUT_LIST))

    elif text == "هاي":
        bot.reply_to(message, random.choice(HI_LIST))

    elif text == "هلا":
        bot.reply_to(message, "هلوات يعيني")

    elif text == "الوان":
        bot.reply_to(message, "اح اسغفر الله وش قاعدين تقولو")

    elif text == "اح":
        bot.reply_to(message, "احااتت")

    elif text == "احا":
        bot.reply_to(message, "احااتتت مش احا واحد")

    elif text == "حبيت":
        bot.reply_to(message, "ياي كيوت")
