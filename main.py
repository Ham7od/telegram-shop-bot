from telebot import TeleBot, types
import time
import os

# =============================
# إعدادات البوت (من الاستضافة)
# =============================
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = TeleBot(TOKEN)

# تخزين حالة المستخدم
user_states = {}

# =============================
# القائمة الرئيسية
# =============================
def main_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("📱 شحن التطبيقات", callback_data="apps"),
        types.InlineKeyboardButton("🎮 شحن الألعاب", callback_data="games"),
        types.InlineKeyboardButton("💳 قسم الرصيد", callback_data="balance"),
        types.InlineKeyboardButton("🎟️ قسم البطاقات", callback_data="cards"),
        types.InlineKeyboardButton("📺 اشتراكات الشاشة", callback_data="subscriptions"),
        types.InlineKeyboardButton("💻 برامج الكمبيوتر", callback_data="programs"),
        types.InlineKeyboardButton("✅ توثيق الحسابات", callback_data="verify"),
        types.InlineKeyboardButton("🧾 تسديد الفواتير", callback_data="bills"),
    )
    bot.send_message(chat_id, "⬇️ اختر القسم المناسب", reply_markup=keyboard)

# =============================
# أمر /start
# =============================
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "أهلا وسهلا بكم في متجر اليوسف 🤍\n\n"
        "شحن تطبيقات / ألعاب / برامج\n"
        "برامج كمبيوتر ويندوز\n"
        "توثيق حسابات / رشق مواقع تواصل\n"
        "اشتراكات شاشة برامج افلام ومسلسلات\n"
        "تسديد فواتير وتحويل رصيد\n"
        "بطاقات فيزا كارد صالحة لجميع المواقع\n\n"
        "👨‍💼 المدير: @YoussefMarkeet\n"
        "⚠️ للضرورة فقط: @HamoudYoussef"
    )
    bot.send_message(message.chat.id, text)
    main_menu(message.chat.id)

# =============================
# الأقسام
# =============================
@bot.callback_query_handler(func=lambda call: call.data in [
    "apps","games","balance","cards","subscriptions","programs","verify","bills"
])
def section_handler(call):
    user_states[call.message.chat.id] = call.data

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("🛒 طلب الخدمة", callback_data="order"),
        types.InlineKeyboardButton("🔙 رجوع", callback_data="back")
    )

    bot.send_message(
        call.message.chat.id,
        "اختر طلب الخدمة أو الرجوع 👇",
        reply_markup=keyboard
    )

# =============================
# زر الرجوع
# =============================
@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    main_menu(call.message.chat.id)

# =============================
# زر طلب الخدمة
# =============================
@bot.callback_query_handler(func=lambda call: call.data == "order")
def order(call):
    user_states[call.message.chat.id] = "waiting_order"
    bot.send_message(
        call.message.chat.id,
        "📝 أرسل تفاصيل طلبك الآن:\n\n"
        "• اسم الخدمة\n"
        "• الكمية\n"
        "• الآيدي / الحساب"
    )

# =============================
# استقبال الطلب + إرساله للإدمن
# =============================
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_order")
def receive_order(message):
    order_text = (
        "📩 طلب جديد\n\n"
        f"👤 الاسم: {message.from_user.first_name}\n"
        f"🆔 الآيدي: {message.from_user.id}\n\n"
        f"📝 التفاصيل:\n{message.text}"
    )

    bot.send_message(ADMIN_ID, order_text)
    bot.send_message(message.chat.id, "✅ تم إرسال طلبك للإدارة بنجاح 🤍")

    user_states.pop(message.chat.id, None)

# =============================
# تشغيل البوت (مستقر)
# =============================
while True:
    try:
        print("Bot is running...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print("❌ خطأ اتصال، إعادة التشغيل...")
        time.sleep(5)
