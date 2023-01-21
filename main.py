from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler


def read_table(filename):
    transliteration_map = dict()
    for line in open(filename):
        l = line.strip().split(",")
        transliteration_map[l[0]] = l[1]
    return transliteration_map


def transliteration(s):
    s = s.lower()
    res = ""
    for c in s:
        if c == " ":
            res += " "
            continue
        res += transliteration_map[c]
    return res.upper()


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    reply = transliteration(input_text)
    await update.message.reply_text(reply)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет, {update.effective_user.first_name}\n'
                                    f'Напиши ФИО в кириллической раскладке, '
                                    f'бот ответит сообщением с рекомендуемым '
                                    f'написанием')


transliteration_map = read_table("table.csv")
app = ApplicationBuilder().token("5816063178:AAFTFqc-SWGrqXQUXzX3ZCofHKNgOI9PbWo").build()
app.add_handler(CommandHandler("start", hello))
app.add_handler(MessageHandler(None, process_message))
app.run_polling()