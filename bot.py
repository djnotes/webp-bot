from pyrogram import Client, idle
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler 
from myhandlers import handle_updates
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
import configparser
import pyrogram.filters as filters

from myhandlers import handle_callback_query, handle_image

import os

api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')
ADMIN_ID = os.environ.get('ADMIN_ID')
proxy_scheme=os.environ.get('scheme')
proxy_hostname= os.environ.get('hostname')
proxy_port = os.environ.get('port')
proxy_on = os.environ.get('proxy_on')

# If we are not inside a container, thus not getting ini info automatically
conf = configparser.ConfigParser()
if not api_id:
    conf.read('env.ini')
    api_id = conf['bot']['api_id']
    api_hash = conf['bot']['api_hash']
    bot_token = conf['bot']['bot_token']
    ADMIN_ID = conf['bot']['ADMIN_ID']

    proxy_scheme = conf['proxy']['scheme']
    proxy_hostname = conf['proxy']['hostname']
    proxy_port = int(conf['proxy']['port'])
    proxy_on = conf['proxy']['proxy_on']

app_proxy = {
    'scheme': proxy_scheme,
    'hostname': proxy_hostname,
    'port': int(proxy_port)
}    
    
    


app = Client(
    name = "session/myapp",
    api_id = api_id,
    api_hash = api_hash,
    bot_token=bot_token,
    proxy = app_proxy if proxy_on else None
)


# @app.on_message()
# app.add_handler(MessageHandler(handle_updates))
# app.add_handler(CallbackQueryHandler(handle_callback_query))

app.add_handler(MessageHandler(handle_image, filters.photo | filters.document))


app.start()
 
info = app.get_me()

try:
    app.send_message(chat_id = int(ADMIN_ID), text = f"{info.first_name} started")
except Exception as e:
    print('Error sending message: {}'.format(e))

idle()

app.stop()
