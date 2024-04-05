import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
from qrcode import create_qrcode_from_link
from datetime import datetime
import pytz
import textwrap
import os
import re
from vintedpars import get_item_info
from photo import round_image

TOKEN = ""
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Сессия
user_sessions = {}

# шрифты
font_regular = ImageFont.truetype('reg2.otf', 48)
font_medium2 = ImageFont.truetype('med3.otf', 46)
semi = ImageFont.truetype('norm.otf', 46)

country_timezones = {
    'England': 'America/New_York',
    'France': 'Europe/Paris',
    'Spain': 'Europe/Madrid'
}

def get_current_time_in_timezone(timezone_name):
    timezone = pytz.timezone(timezone_name)
    current_time = datetime.now(timezone)
    return current_time.strftime('%H:%M')

# Функции утилиты
def is_valid_url(url):
    regex_pattern = r'^(https?://|www\.)'
    return re.match(regex_pattern, url) is not None

def get_current_time_in_timezone(timezone_name):
    timezone = pytz.timezone(timezone_name)
    current_time = datetime.now(timezone)   
    return current_time.strftime('%H:%M')

def format_price(price):
    return f"{price}{' €' if '.' in price or ',' in price else ',00 €'}"

def wrap_text(draw, text, font, width, position, fill_color):
    wrapped_text = textwrap.fill(text, width=width)
    draw.text(position, wrapped_text, font=font, fill=fill_color)

# старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇺🇸 Америка", callback_data='England'))
    markup.add(types.InlineKeyboardButton("🇫🇷 Франция", callback_data='France'))
    markup.add(types.InlineKeyboardButton("🇪🇸 Испания", callback_data='Spain'))
    bot.send_message(message.chat.id, "👋 Привет!\n\nДля какой страны генерируем QR-code?", reply_markup=markup)

    # Инициализация сессии
    user_sessions[message.chat.id] = {'state': 'SELECT_COUNTRY'}

# выбора страны
@bot.callback_query_handler(func=lambda call: user_sessions[call.message.chat.id]['state'] == 'SELECT_COUNTRY')
def handle_country_selection(call):
    country = call.data
    user_sessions[call.message.chat.id] = {'state': 'ENTER_AD_LINK', 'country': country}
    bot.answer_callback_query(call.id, "Выбрана страна: " + country)
    bot.send_message(call.message.chat.id, '🔗 Отправьте ссылку на объявление')

# ввода ссылки на объявление
@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('state') == 'ENTER_AD_LINK')
def handle_ad_link(message):
    if not is_valid_url(message.text):
        bot.send_message(message.chat.id, '❌ Введена некорректная ссылка. Пожалуйста, введите корректную ссылку на объявление.')
        return

    user_sessions[message.chat.id]['ad_link'] = message.text
    user_sessions[message.chat.id]['state'] = 'ENTER_FISH_LINK'
    bot.send_message(message.chat.id, '🔗 Отправьте ФИШ ссылку')

# ввода FISH ссылки и генерация QR кода
@bot.message_handler(func=lambda message: user_sessions.get(message.chat.id, {}).get('state') == 'ENTER_FISH_LINK')
def handle_fish_link(message):
    session_data = user_sessions.get(message.chat.id, {})
    user_sessions[message.chat.id]['fish_link'] = message.text
    if not is_valid_url(message.text):
        bot.send_message(message.chat.id, '❌ Введена некорректная FISH ссылка. Пожалуйста, введите корректную FISH ссылку.')
        return

    # Генерация QR кода и отправка изображения 
    bot.send_message(message.chat.id, '⏳ Генерирую QR-code...')
    country = user_sessions[message.chat.id]['country']
    ad_link = user_sessions[message.chat.id]['ad_link']
    link2 = user_sessions[message.chat.id]['fish_link']
    img = f"image_{country}.jpg"

    match = re.search(r'/(\d+)-', ad_link)
    item_id = match.group(1)
    item_data = get_item_info(item_id)
    title = item_data[0].get('title', 'Unknown Title')
    login = item_data[0].get('username', 'Unknown Title')
    price = item_data[0].get('price', 'Unknown Title')
    url = item_data[0].get('url', 'Unknown Title') 
    image = Image.open(img)
    draw = ImageDraw.Draw(image)
    timezone_name = country_timezones.get(country, 'UTC')
    time = get_current_time_in_timezone(timezone_name)
    print(time)


    wrap_text(draw, time, semi, 30, (90, 45), (0, 0, 0))
    wrap_text(draw, title, font_medium2, 100, (215, 670), (0, 0, 0))
    wrap_text(draw, format_price(price), font_regular, 30, (215, 735), (0, 0, 0))
    wrap_text(draw, login, font_medium2, 30, ((1170 - draw.textbbox((0, 0), login, font=font_medium2)[2]) // 2, 510), (0, 119, 130))

    create_qrcode_from_link(link2)
    qr_image = Image.open("qrcode.png").convert('RGBA')
    qr_position = (260, 1060)
    image.paste(qr_image, qr_position)
    round_image(url)
    id_image = Image.open("output_rounded.png").convert('RGBA')
    id_position = (40, 660)
    image.paste(id_image, id_position)

    image.save('result.jpg')

    bot.send_photo(message.chat.id, photo=open('result.jpg', 'rb'))
    #os.remove("qrcode.png")
    #os.remove("result.jpg")
    os.remove("output_rounded.png")

    # Сброс состояния пользователя
    del user_sessions[message.chat.id]


bot.infinity_polling()
