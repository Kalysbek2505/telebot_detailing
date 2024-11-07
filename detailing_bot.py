import telebot
import openai
from telebot import types
import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY


PRICE_LIST = """
🚗 Химчистка с полным разбором:
• Седаны: от 8000 С
• Кроссоверы: от 9000 С
• Джипы: от 10,000 С
🎁 Подарок: 3-х фазная мойка + сухой туман

✨ 3-х этапная полировка + нанесение керамики:
• Седаны: от 7000 С
• Кроссоверы: от 9000 С
• Джипы: от 10,000 С
🎁 Подарок: 3-х фазная мойка + влажная уборка салона

📦 Оклейка:
• от 65,000 С, зависит от машины.
"""

CONTACT_NUMBER = "+996990228885"  

WORK_PROCESS_TEXT = """
🛠 **Как мы работаем?**

1. **Первый контакт** 🗣️  
   При первом контакте с нами вы получите профессиональную консультацию от нашей команды. Мы внимательно выслушаем ваши потребности и цели, а также оценим состояние вашего автомобиля.

2. **Подбор пакета услуг** 🎁  
   Мы предложим вам подходящий пакет услуг, учитывая ваши предпочтения, бюджет и состояние автомобиля. Наши специалисты помогут выбрать оптимальное сочетание услуг для достижения наилучших результатов.

3. **Выполнение услуг** 🚗✨  
   На этом этапе наши опытные мастера приступают к выполнению выбранных услуг. Используются передовые техники, специализированные инструменты и высококачественные материалы для достижения превосходного результата.

4. **Контроль качества** ✅  
   Мы уделяем большое внимание контролю качества каждой услуги. Наши мастера тщательно проверяют и регулярно оценивают результаты, чтобы убедиться, что работа выполнена на самом высоком уровне.

5. **Сдача авто** 🚘🎉  
   По завершении работы мы проведем финальную проверку автомобиля, чтобы убедиться в его безупречном внешнем виде. Затем мы продемонстрируем вам результаты и ответим на все ваши вопросы.
"""

def get_response(prompt):
    topic_prompt = f"""
    Ты эксперт по авто-детейлингу. Отвечай только на вопросы, связанные с этой темой. 
    Если спросят о ценах, укажи их с эмодзи. Если кто-то хочет записаться, дай номер телефона компании: {CONTACT_NUMBER}.
    
    Вот наш прайс:
    {PRICE_LIST}
    
    Вопрос: {prompt}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": topic_prompt}]
    )
    return response.choices[0].message['content']

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_prices = types.KeyboardButton("Цены")
    button_appointment = types.KeyboardButton("Записаться на услугу")
    button_work_process = types.KeyboardButton('Как мы работаем?')
    markup.add(button_prices, button_appointment, button_work_process)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Добрый день я ИИ авто детейлинга. Можете задавать любые вопросы по теме авто-детейлинга",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda message: message.text in ["Цены", "Записаться на услугу", "Как мы работаем?"])
def handle_menu(message):
    if message.text == "Цены":
     
        bot.send_message(message.chat.id, f"Наш прайс-лист:\n{PRICE_LIST}")
    elif message.text == "Записаться на услугу":
       
        bot.send_message(message.chat.id, f"Для записи на услугу, позвоните нам по телефону: {CONTACT_NUMBER} 📞")
    elif message.text == "Как мы работаем?":
        
        bot.send_message(message.chat.id, WORK_PROCESS_TEXT, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.lower()
    
   
    if "записаться" in user_input or "номер" in user_input or "позвонить" in user_input:
        bot.reply_to(message, f"Вы можете записаться по телефону: {CONTACT_NUMBER} 📞")
    else:
        
        response = get_response(message.text)
        bot.reply_to(message, response)

bot.polling()