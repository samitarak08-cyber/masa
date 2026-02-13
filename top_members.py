import telebot
import json
import os

def handle_top(bot, message):
    if message.text == "الافضل":
        bot.reply_to(message, "📊 هذه الميزة ستتوفر قريباً بعد تجميع البيانات!")
      
