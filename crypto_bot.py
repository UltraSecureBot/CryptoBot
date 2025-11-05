import telebot
from datetime import datetime, timezone

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


KEY_FLAG = '****************'
KEYS = []

def gen_keys():
    K = [int(''.join(i).encode('utf-8').hex(), 16) for i in grouper(KEY_FLAG, 2)]

    KEYS.append(K[0]^K[2]^K[3]^K[6])
    KEYS.append(K[4]^K[0]^K[5]^K[7])
    KEYS.append(K[6]^K[7]^K[1]^K[4])
    KEYS.append(K[1]^K[3]^K[5])
    KEYS.append(K[5]^K[6]^K[7])
    KEYS.append(K[7]^K[6]^K[1])


def encrypt(string):
    blocks = [int(''.join(i).encode('utf-8').hex(), 16) for i in grouper(string, 2)]

    c = []
    i = 0
    v = datetime.now(timezone.utc).replace(second=0, microsecond=0, tzinfo=None)
    hour = str(int(v.strftime("%H")) + 3) # For GMT+3 time!!!!
    minute = v.strftime("%M")
    time = hour + ":" + minute
    for block in blocks:
        if (i == 0):
            timestamp = int(v.timestamp())
            bcipher = block ^ KEYS[i%6] ^ timestamp
            c.append(bcipher)
            i+=1
            continue
        bcipher = block ^ KEYS[i%6] ^ bcipher
        c.append(bcipher)
        i += 1

    c_hex = []
    for item in c:
        item = hex(item)[2:]
        c_hex.append(item)

    c_hex = "".join(c_hex)
    return time + " - " + c_hex


bot = telebot.TeleBot('tg token')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Используй меня для шифрования пароля от своего криптокошелька)')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, encrypt(message.text))

gen_keys()
bot.polling(none_stop=True, interval=0)
