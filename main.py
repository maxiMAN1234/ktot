import telebot
import google.generativeai as genai
from telebot import types
from keep_alive import keep_alive

TELEGRAM_TOKEN = '7979196477:AAEcZfAxvjFeoAg02zSGbvIv9FcCMKICNyM'
GEMINI_API_KEY = 'AIzaSyBsoDTqFjqA79KvugDoKW-71J-hDjmxpXE'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

vova_intro = """
Ты бот, который имитирует Вову Ревуцкого — DevOps-инженера.
Вова постоянно преувеличивает, использует сарказм, странные аналогии, гиперболизирует и немного несёт чушь.
Он пишет в стиле айтишника, который всё преувеличивает и много иронизирует.

Вот примеры сообщений Вовы:
- "Я вчера деплой делал... чуть Kubernetes не упал, Земля с орбиты не сошла — чудо вообще"
- "Если бы ещё Prometheus с Grafana не отказывались жить — было бы совсем весело"
- "Логи? Ага, сейчас достану из-под подушки рядом с мечом Гэндальфа"
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здарова, я — Вова-бот. Спрашивай что угодно, но готовься к трэшу!")

@bot.message_handler(func=lambda message: True)
def reply_like_vova(message):
    user_input = message.text
    prompt = f"""{vova_intro}

Сообщение пользователя: "{user_input}"
Ответ Вовы:"""
    try:
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так, как обычно в проде...")

keep_alive()
print("Бот запущен")
bot.polling(none_stop=True)