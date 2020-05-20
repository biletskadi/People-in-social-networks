import googlemaps
from datetime import datetime


class Geolocation:
    def __init__(self):
        self.now = datetime.now()

    def DirectionMessage(self, bot, update):
            bot.send_message(chat_id=update.message.chat_id,
                            text="Початкова точка(адреса або назва закладу)?")
            origin = update.message.text
            bot.send_message(chat_id=update.message.chat_id,
                            text="Кінцева точка(адреса або назва закладу)?")
            destination = update.message.text
            directions_result = gmaps.directions(origin,
                                                destination,
                                                mode="transit",
                                                departure_time=self.now)
            bot.send_message(chat_id=update.message.chat_id, text='Відстань до цілі ' + 
            directions_result[0]['legs'][0]['distance']['text'] + 
            '. Якщо хочете дізнатися яким транспортом дістатися до кінчевої точки використайте /transport')

        def TransportMessage(self, bot, update):
            bot.send_message(chat_id=update.message.chat_id,
                            text="Початкова точка(адреса або назва закладу)?")
            origin = update.message.text
            bot.send_message(chat_id=update.message.chat_id,
                            text="Кінцева точка(адреса або назва закладу)?")
            destination = update.message.text
            directions_result = gmaps.directions(origin,
                                                destination,
                                                mode="transit",
                                                departure_time=self.now)
            bot.send_message(chat_id=update.message.chat_id, text='Потрібні автобуси \n' + directions_result[0]['legs'][0]['steps'][1]['transit_details']['line']['short_name'])
