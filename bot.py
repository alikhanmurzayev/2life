import telebot

import config
import database
import voice

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
    msg = bot.send_message(message.chat.id, 'Какой болезни вы подвержены?', reply_markup=user_markup)
    bot.register_next_step_handler(msg, setDisease)
def setDisease(message):
    database.set_param(message, database.users_t, 'disease')
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    ######
    user_markup.row('Рассказать о своем Самочувствии')
    user_markup.row('Сдать отчет')
    ######
    msg = bot.send_message(message.chat.id, 'Регистрация в системе успешно пройдена. Вы можете:', reply_markup=user_markup)
    bot.register_next_step_handler(msg, text_messages)

def setFeeling(message):
    if message.voice:
        message.text = str(voice.voice_to_text(message))
        if message.text:
            database.set_feeling(message)
            bot.send_message(message.chat.id, 'Сохранен отчет: ' + message.text)
        else:
            msg = bot.send_message(message.chat.id, 'Отправьте сообщение еще раз')
            bot.register_next_step_handler(msg, setFeeling)
            return
    elif message.text:
        database.set_feeling(message)
        bot.send_message(message.chat.id, 'Сохранен отчет: ' + message.text)
    else:
        msg = bot.send_message(message.chat.id, 'Отправьте сообщение еще раз')
        bot.register_next_step_handler(msg, setFeeling)
        return
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    ######
    user_markup.row('Рассказать о своем Самочувствии')
    user_markup.row('Сдать отчет')
    ######
    msg = bot.send_message(message.chat.id, 'Вот, что Вы можете сделать:', reply_markup=user_markup)
    bot.register_next_step_handler(msg, text_messages)


@bot.message_handler(content_types=['text'])
def text_messages(message):
    text = message.text
    if text == 'Рассказать о своем Самочувствии':
        msg = bot.send_message(message.chat.id, 'Как Вы себя чувствуете? Можете написать или отправить голосовое сообщение')
        bot.register_next_step_handler(msg, setFeeling)
    elif text == 'Сдать отчет':
        database.set_param(message, database.report_t, 'date')
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('Да', 'Нет')
        msg = bot.send_message(message.chat.id, 'Является-ли гипертония хранической?', reply_markup=user_markup)
        bot.register_next_step_handler(msg, setChronic)
    else:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        ######
        user_markup.row('Рассказать о своем Самочувствии')
        user_markup.row('Сдать отчет')
        ######
        msg = bot.send_message(message.chat.id, 'Выберите одну опцию', reply_markup=user_markup)
        bot.register_next_step_handler(msg, text_messages)
def setChronic(message):
    database.set_param(message, database.report_t, 'chronic')
    msg = bot.send_message(message.chat.id, 'Какие медикаменты Вы употребляли?')
    bot.register_next_step_handler(msg, setMedicine)
def setMedicine(message):
    database.set_param(message, database.report_t, 'medicine')
    msg = bot.send_message(message.chat.id, 'Введите кровяное давление')
    bot.register_next_step_handler(msg, setBloodPressure)
def setBloodPressure(message):
    database.set_param(message, database.report_t, 'bp')
    msg = bot.send_message(message.chat.id, 'Оставьте свои контакты, пожалуйста')
    bot.register_next_step_handler(msg, setContacts)
def setContacts(message):
    database.set_param(message, database.report_t, 'contacts')
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    ######
    user_markup.row('Рассказать о своем Самочувствии')
    user_markup.row('Сдать отчет')
    ######
    msg = bot.send_message(message.chat.id, 'Спасибо, отчет сохранен и будет обработан в ближайшее время', reply_markup=user_markup)
    bot.register_next_step_handler(msg, text_messages)


bot.polling(none_stop=True)