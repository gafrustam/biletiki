from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler


def read_table(filename):
    first_map = dict()
    others_map = dict()
    for line in open(filename):
        l = line.strip().split(",")
        first_map[l[0]] = l[1]
        if l[2] == "":
            others_map[l[0]] = l[1]
        else:
            others_map[l[0]] = l[2]
    return first_map, others_map


def transliteration(s):
    first = True
    s = s.lower()
    res = ""
    for c in s:
        if c == " ":
            res += " "
            first = True
            continue
        if first:
            res += first_map[c]
        else:
            res += others_map[c]
        first = False
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


first_map, others_map = read_table("table.csv")
app = ApplicationBuilder().token("5816063178:AAFTFqc-SWGrqXQUXzX3ZCofHKNgOI9PbWo").build()
app.add_handler(CommandHandler("start", hello))
app.add_handler(MessageHandler(None, process_message))
app.run_polling()