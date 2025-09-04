import asyncio
import os
import requests
# from telegram import Bot
from telegram.ext import ApplicationBuilder
# from datetime import datetime
from lxml import html

# Configuración
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

# Inicializar bots
# telegram_bot = Bot(token=TELEGRAM_TOKEN)


# buscar datos dolares
urlusd = 'https://iol.invertironline.com/mercado/cotizaciones/argentina/monedas'
response = requests.get(urlusd)
tree = html.fromstring(response.content)

# XPath para encontrar el dato dolares
usd = tree.xpath('//td[@class="tar"]/text()')

# buscar datos cauciones
urlcauc = 'https://iol.invertironline.com/mercado/cotizaciones/argentina/cauciones/todas'
response = requests.get(urlcauc)
tree = html.fromstring(response.content)
cauc = tree.xpath('//td[@class="tac"]/@data-order')

# buscar datos merval
urlindexes = 'https://iol.invertironline.com/mercado/cotizaciones/índices/panel/ee.uu-indices'
response = requests.get(urlindexes)
tree = html.fromstring(response.content)
merv = tree.xpath('//span[@class="tar ml5"]/text()')

# timestamp = datetime.now()
# timestamp = timestamp.strftime("%H:%M:%S")

usdoficial = usd[1].split(',')[0]
usdmep = usd[5].split(',')[0]

text = (
    f"Message Test V1.0\n\n"
    f"💵 Dolar Oficial: ${usdoficial}\n"
    # f"📈 Compra: ${usd[0]}\n"
    # f"📈 Venta: ${usd[1]}\n\n"
    f"💵 Dolar MEP (AL30): ${usdmep}\n\n"
    # f"📈 Compra: ${usd[4]}\n"
    # f"📈 Venta: ${usd[5]}\n\n"
    f"📊 Caucion: {cauc[0]}%\n\n"
    f"📈 Merval: {merv[0]}%\n\n"
    # f"🕒 Actualizado: {timestamp} hs\n"
    f"\n🔗 Fuente: IOL"
)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
async def enviar_mensaje():
    await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

# async def enviar_mensaje():
#     bot = Bot(token=TELEGRAM_TOKEN)
#     mensaje = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
#     # print(f"✅ Mensaje enviado. ID: {mensaje.message_id}")

# Ejecutar la función asíncrona
asyncio.run(enviar_mensaje())