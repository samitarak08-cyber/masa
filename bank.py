import json
import os
import random
import time

# ملف حفظ الأموال
BANK_FILE = 'bank_data.json'

def load_bank():
    if os.path.exists(BANK_FILE):
        with open(BANK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_bank(data):
    with open(BANK_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_balance(user_id):
    data = load_bank()
    return data.get(str(user_id), {}).get('money', 0)

def add_money(user_id, amount):
    data = load_bank()
    uid = str(user_id)
    if uid not in data: data[uid] = {'money': 0, 'last_salary': 0}
    data[uid]['money'] += amount
    save_bank(data)

# --- أوامر البنك ---

def handle_bank(bot, message):
    text = message.text
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    # 1. أمر الراتب (كل 24 ساعة)
    if text == "راتب":
        data = load_bank()
        if user_id not in data: data[user_id] = {'money': 0, 'last_salary': 0}
        
        current_time = time.time()
        last_salary = data[user_id].get('last_salary', 0)
        
        if current_time - last_salary > 86400:  # 24 ساعة بالثواني
            salary = random.randint(500, 1500)
            data[user_id]['money'] += salary
            data[user_id]['last_salary'] = current_time
            save_bank(data)
            bot.reply_to(message, f"💰 تم صرف راتبك وقدره: **{salary}** ريال!")
        else:
            remaining = int((86400 - (current_time - last_salary)) / 3600)
            bot.reply_to(message, f"⚠️ أخذت راتبك خلاص، ارجع بعد {remaining} ساعة.")

    # 2. أمر بخشيش
    elif text == "بخشيش":
        tip = random.randint(10, 100)
        add_money(user_id, tip)
        bot.reply_to(message, f"💸 حصلت على بخشيش سري: **{tip}** ريال!")

    # 3. أمر فلوسي (البنك)
    elif text in ["بنك", "فلوسي", "رصيدي"]:
        money = get_balance(user_id)
        bot.reply_to(message, f"🏦 رصيدك في بنك ماسا هو: **{money}** ريال.")

    # 4. أمر تحويل (بالرد)
    elif text.startswith("تحويل") and message.reply_to_message:
        try:
            amount = int(text.split()[1])
            sender_money = get_balance(user_id)
            if sender_money >= amount and amount > 0:
                target_id = message.reply_to_message.from_user.id
                add_money(user_id, -amount)
                add_money(target_id, amount)
                bot.reply_to(message, f"✅ تم تحويل **{amount}** ريال إلى {message.reply_to_message.from_user.first_name}")
            else:
                bot.reply_to(message, "❌ رصيدك ما يكفي أو المبلغ غلط.")
        except:
            bot.reply_to(message, "⚠️ طريقة التحويل: اكتب 'تحويل 100' بالرد على الشخص.")
      
