from __future__ import print_function

from typing import List, Any, Tuple
from calendar_adt import Calendar
from geolocation import Geolocation
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
update = Updater(token='1134927516:AAE3Bi5dGXbaZWeO_IXIWZjtwMTpzsn6r64')
dispatcher = update.dispatcher

c = Calendar()
g = Geolocation()
dispatcher.add_handler(CommandHandler('start', c.startCommand))
dispatcher.add_handler(CommandHandler('add', c.AddMessage))
dispatcher.add_handler(CommandHandler('delete', c.DeleteMessage))
dispatcher.add_handler(CommandHandler('change', c.ChangeMessage))
dispatcher.add_handler(CommandHandler('check_daily', c.CheckDailyMessage))
dispatcher.add_handler(CommandHandler('check_next_events', c.CheckNextEventsMessage))
dispatcher.add_handler(CommandHandler('route', g.DirectionMessage))
dispatcher.add_handler(CommandHandler('transport', g.TransportMessage))
update.start_polling()
update.idle()