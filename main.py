from plugin import api_id, api_hash, bot_token
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

app = Client(name="unit_converter_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Conversion type variable
conversion_type = None


@app.on_message(filters.command("start"))
def start_command(client: Client, message: Message):
    global conversion_type
    welcome_message = "به ربات  تبدیل واحد خوش آمدید. \n\n" \
                      "منوی اصلی:\n" \
                      "لطفاً نوع تبدیل موردنظر خود را انتخاب کنید.\n" \
                      "تبدیل دما از سانتی گراد به فارنهایت و برعکس\n" \
                      "تبدیل ارتفاع از متر به فوت و برعکس\n" \
                      "تبدیل وزن از کیلو گرم به پوند و برعکس\n"

    buttons = [
        InlineKeyboardButton("تبدیل ارتفاع", callback_data="convert_height"),
        InlineKeyboardButton("تبدیل وزن", callback_data="convert_weight"),
        InlineKeyboardButton("تبدیل دما", callback_data="convert_temperature"),
    ]

    keyboard = InlineKeyboardMarkup(
        [buttons[i:i + 1] for i in range(0, len(buttons), 1)]

    )

    message.reply_text(welcome_message, reply_markup=keyboard)


@app.on_message(filters.command("about"))
def about_bot_command(client: Client, message: Message):
    about_message = "این ربات توسط سیدمحمدصالح مصطفایی و مهدی آقائی توسعه داده شده است."
    message.reply_text(about_message)


@app.on_callback_query()
def button_pressed(_, callback: CallbackQuery):
    global conversion_type
    conversion_type = callback.data

    callback.message.edit_text(
        f"لطفاً مقدار مورد نظر خود را وارد کنید فرقی نداره کدوم واحد رو وارد میکنی ما جفتشو تبدیل میکنیم.")


def convert_height(value):
    try:
        value = float(value)
        if value >= 0:
            feet = value * 3.28084
            return f"{value} متر برابر {feet} فوت است."
        else:
            return "فرمت عدد وارد شده نادرست است."
    except ValueError:
        return "فرمت عدد وارد شده نادرست است."


def convert_weight(value):
    try:
        value = float(value)
        if value >= 0:
            pounds = value * 2.20462
            return f"{value} کیلوگرم برابر {pounds} پوند است."
        else:
            return "فرمت عدد وارد شده نادرست است."
    except ValueError:
        return "فرمت عدد وارد شده نادرست است."


def convert_temperature(value):
    try:
        value = float(value)
        fahrenheit = (value * 9 / 5) + 32
        return f"{value} درجه سلسیوس معادل {fahrenheit} درجه فارنهایت است."
    except ValueError:
        return "فرمت عدد وارد شده نادرست است."


# Reverse conversion functions
def reverse_convert_height(value):
    try:
        value = float(value)
        if value >= 0:
            meters = value / 3.28084
            return f"{value} فوت برابر {meters} متر است."
        else:
            return "فرمت عدد وارد شده نادرست است."
    except ValueError:
        return "فرمت عدد وارد شده نادرست است."


def reverse_convert_weight(value):
    try:
        value = float(value)
        if value >= 0:
            kilograms = value / 2.20462
            return f"{value} پوند برابر {kilograms} کیلوگرم است."
        else:
            return "فرمت عدد وارد شده نادرست است."
    except ValueError:
        return "فرمت عدد وارد شده نادرست است."


def reverse_convert_temperature(value):
    try:
        value = float(value)
        celsius = (value - 32) * 5 / 9
        return f"{value} درجه فارنهایت معادل {celsius} درجه سلسیوس است."
    except ValueError:
        return "فرمت عدد وارد شده نادرست است."


@app.on_message(filters.text)
def handle_user_input(_, message: Message):
    global conversion_type

    if conversion_type:
        value = message.text

        # Perform the conversion based on the selected type
        if conversion_type == "convert_height":
            result = convert_height(value)
            reverse_result = reverse_convert_height(value)
        elif conversion_type == "convert_weight":
            result = convert_weight(value)
            reverse_result = reverse_convert_weight(value)
        elif conversion_type == "convert_temperature":
            result = convert_temperature(value)
            reverse_result = reverse_convert_temperature(value)
        else:
            result = "نوع تبدیل ناشناخته است."
            reverse_result = "نوع تبدیل ناشناخته است."

        message.reply_text(f"تبدیل معمولی: {result}\nتبدیل برعکس: {reverse_result}")

        conversion_type = None
    else:
        message.reply_text("متوجه منظور شما نشدم.")


app.run()
