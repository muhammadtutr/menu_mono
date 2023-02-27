import telebot
import datetime

TOKEN = '6292995887:AAH109q8qeYXlXonXO-PbJ3kcEPkYq0APds'
ADMIN_USER_ID = '827112414'

bot = telebot.TeleBot(TOKEN)

feedbacks = []

@bot.message_handler(commands=['start'])
def start(message):
    """Отправляет приветственное сообщение пользователю при запуске бота"""
    bot.send_message(chat_id=message.chat.id, text="Привет! Напишите /feedback, чтобы оставить отзыв о нашем кальянном мастере.")

@bot.message_handler(commands=['feedback'])
def feedback(message):
    """Предлагает пользователю оставить отзыв"""
    bot.send_message(chat_id=message.chat.id, text="Пожалуйста, напишите свой отзыв о кальянном мастере в следующем сообщении:")
    bot.register_next_step_handler(message, get_feedback_text)

def get_feedback_text(message):
    """Получает текст отзыва от пользователя"""
    feedback_text = message.text
    user_id = message.from_user.id
    feedbacks.append({'user_id': user_id, 'feedback_text': feedback_text})
    bot.send_message(chat_id=message.chat.id, text="Спасибо за ваш отзыв! Мы отправили его администратору на рассмотрение.")
    bot.send_message(chat_id=message.chat.id, text="Пожалуйста, введите рейтинг от 1 до 5. Вы можете это сделать, написав цифру от 1 до 5 в следующем сообщении")
    bot.register_next_step_handler(message, get_feedback_rating)

def get_feedback_rating(message):
    """Получает рейтинг от пользователя"""
    feedback_rating = message.text
    if feedback_rating.isdigit() and int(feedback_rating) in range(1, 6):
        user_id = message.from_user.id
        feedbacks[-1]['feedback_rating'] = feedback_rating
        feedbacks[-1]['feedback_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bot.send_message(chat_id=message.chat.id, text="Спасибо за вашу оценку!")
        send_feedback_to_admin(message)
    else:
        bot.send_message(chat_id=message.chat.id, text="Рейтинг можно указать от 1 до 5, укажите рейтинг написав цифру от 1 до 5 в следующем сообщении")
        bot.register_next_step_handler(message, get_feedback_rating)

def send_feedback_to_admin(message):
    """Отправляет отзыв и рейтинг администратору"""
    user_id = message.from_user.id
    user_name = message.from_user.username
    feedback_text = feedbacks[-1]['feedback_text']
    feedback_rating = feedbacks[-1]['feedback_rating']
    feedback_time = feedbacks[-1]['feedback_time']
    feedback_str = f"Новый отзыв от пользователя {user_id} (@{user_name}):\n\n{feedback_text}\n\nРейтинг: {feedback_rating}\nДата и время: {feedback_time}"
    bot.send_message(chat_id = ADMIN_USER_ID, text = feedback_str)

@bot.message_handler(commands=['info_admin'])
def feedbacks_admin(message):
    """Отправляет администратору список всех оставленных отзывов"""
    if str(message.from_user.id) == ADMIN_USER_ID:
        if len(feedbacks) == 0:
            bot.send_message(chat_id=message.chat.id, text="Пока нет ни одного отзыва.")
        else:
            for feedback in feedbacks:
                user_id = feedback['user_id']
                user_name = bot.get_chat_member(message.chat.id, user_id).user.username
                feedback_text = feedback['feedback_text']
                feedback_rating = feedback['feedback_rating']
                feedback_time = feedback['feedback_time']
                feedback_str = f"Отзыв от пользователя {user_id} (@{user_name}):\n\n{feedback_text}\n\nРейтинг: {feedback_rating}\nДата: {feedback_time}"
                bot.send_message(chat_id=message.chat.id, text=feedback_str)
    else:
        bot.send_message(chat_id=message.chat.id, text="Вы не являетесь администратором.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я не понимаю, что вы от меня хотите. Напишите /start, чтобы начать.")

if __name__ == '__main__':
    bot.polling(none_stop=True)