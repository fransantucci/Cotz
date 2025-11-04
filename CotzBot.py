import asyncio
import os
import requests
# from telegram import Bot # para versiones viejas de telegram
from telegram.ext import ApplicationBuilder
from datetime import datetime
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

# buscar datos index brasil
urlindexes = 'https://iol.invertironline.com/titulo/cotizacion/BCBA/EWZ/ETF-ISHARES-MSCI-BRAZIL'
response = requests.get(urlindexes)
tree = html.fromstring(response.content)
ewz = tree.xpath('//*[@id="variacionUltimoPrecio"]/span/span[3]/span/text()')

# buscar datos index QQQ
urlindexes = 'https://iol.invertironline.com/titulo/cotizacion/BCBA/QQQ/ETF-INVESCO-QQQ-TRUST'
response = requests.get(urlindexes)
tree = html.fromstring(response.content)
qqq = tree.xpath('//*[@id="variacionUltimoPrecio"]/span/span[3]/span/text()')

# buscar datos index SPY
urlindexes = 'https://iol.invertironline.com/titulo/cotizacion/BCBA/SPY/ETF-SPDR-S-P-500'
response = requests.get(urlindexes)
tree = html.fromstring(response.content)
spy = tree.xpath('//*[@id="variacionUltimoPrecio"]/span/span[3]/span/text()')


timestamp = datetime.now()
timestamp = timestamp.strftime("%H:%M:%S")

usdoficial = usd[1].split(',')[0]
usdmep = usd[5].split(',')[0]

if (usdmep * 1.2) > usd:
    text = (
        f"Cotz V2.1\n\n"
        f"💵 Dolar Oficial: ${usdoficial}\n"
        f"📊 Caucion: {cauc[0]}%\n\n"
        f"🇦🇷 Merval: {merv[0]}%\n"
        f"🇧🇷 EWZ: {ewz[0]}%\n"
        f"🇺🇸 QQQ: {qqq[0]}%\n"
        f"🇺🇸 SPY: {spy[0]}%\n"
        f"🕒 Actualizado: {timestamp} hs\n"
        f"\n🔗 Fuente: IOL"
    )
else:
    text = (
        f"Cotz V2.1\n\n"
        f"💵 Dolar Oficial: ${usdoficial}\n"
        f"💵 Dolar MEP: ${usdmep}\n\n"
        f"📊 Caucion: {cauc[0]}%\n\n"
        f"🇦🇷 Merval: {merv[0]}%\n"
        f"🇧🇷 EWZ: {ewz[0]}%\n"
        f"🇺🇸 QQQ: {qqq[0]}%\n"
        f"🇺🇸 SPY: {spy[0]}%\n"
        f"🕒 Actualizado: {timestamp} hs\n"
        f"\n🔗 Fuente: IOL"
    )

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
async def enviar_mensaje():
    await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

# async def enviar_mensaje():
#     bot = Bot(token=TELEGRAM_TOKEN)
#     mensaje = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
#     # print(f"✅ Mensaje enviado. ID: {mensaje.message_id}")

# print(f"✅ Mensaje enviado. ID: {indexes[0]}")

# Ejecutar la función asíncrona
asyncio.run(enviar_mensaje())