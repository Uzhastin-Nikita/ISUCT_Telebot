import config
import telebot

bot = telebot.TeleBot(config.TOKEN)


# @bot.message_handler(content_types=['text'])
# def Repeat(message):
#     bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['start'])   
def Welcome(message):
    sti = open('static/ISUCT_start.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n".format(message.from_user, bot.get_me))
    parse_mode = 'html'

#RUN
bot.polling(none_stop=True)