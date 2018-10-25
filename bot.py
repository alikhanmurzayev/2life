import telebot

import config
import database

bot = telebot.TeleBot(config.token)



@bot.message_handler(commands=['start'])
def start(message):
    database.add_user(message)
    msg = bot.send_message(message.chat.id, 'Введите имя')
    bot.register_next_step_handler(msg, setName)
def setName(message):
    database.set_param(message, database.users_t, 'name')
    msg = bot.send_message(message.chat.id, 'Введите фамилию')
    bot.register_next_step_handler(msg, setSurname)
def setSurname(message):
    database.set_param(message, database.users_t, 'surname')
    msg = bot.send_message(message.chat.id, 'Сколько Вам лет?')
    bot.register_next_step_handler(msg, setAge)
def setAge(message):
    database.set_param(message, database.users_t, 'age')
    msg = bot.send_message(message.chat.id, 'Введите неделю беременности')
    bot.register_next_step_handler(msg, setWeek)
def setWeek(message):
    database.set_param(message, database.users_t, 'week')
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы курите?', reply_markup=user_markup)
    bot.register_next_step_handler(msg, setSmoke)
def setSmoke(message):
    database.set_param(message, database.users_t, 'smoke')
    msg = bot.send_message(message.chat.id, 'Сколько сигарет в день вы выкуриваете?')
    bot.register_next_step_handler(msg, setCigNumber)
def setCigNumber(message):
    database.set_param(message, database.users_t, 'cig_number')
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Да', 'Нет')
    msg = bot.send_message(message.chat.id, 'Вы употребляете алкоголь?', reply_markup=user_markup)
    bot.register_next_step_handler(msg, setAlcohol)
def setAlcohol(message):
    database.set_param(message, database.users_t, 'alcohol')
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    ######
    user_markup.row('Гипертония')
    user_markup.row('Ожирение')
    user_markup.row('Стенокардия')
    user_markup.row('Плохое зрение')
    ######
    msg = bot.send_message(message.chat.id, 'Какой хранической болезни вы подвержены?', reply_markup=user_markup)
    bot.register_next_step_handler(msg, text_messages)


@bot.message_handler(content_types=['text'])
def text_messages(message):
    print('in text messages')

bot.polling(none_stop=True)