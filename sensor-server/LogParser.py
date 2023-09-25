from datetime import datetime
from decimal import Decimal
from datetime import timedelta
from datetime import timezone
import time

SIZE_HUMIDITY = 2
SIZE_TEMPERATURE = 3
SIZE_HUMIDITY_AND_TEMP = 5
INDEX_NAME_START = 13
INDEX_TIMESTAMP = 12
INDEX_PACKET_LENGTH = 4


class LogParser:

    def __init__(self):
        pass

    def parse_packet(self, packet):
        log_entry = {}

        timestamp = parse_timestamp(packet)
        log_entry['timestamp'] = timestamp

        name_length = None
        try:
            name_length = packet[INDEX_TIMESTAMP]
        except IndexError as ex:
            print(ex, ', ', packet, ', ', INDEX_TIMESTAMP)

        name = packet[INDEX_NAME_START: INDEX_NAME_START + name_length].decode()
        name = name.strip()
        log_entry['name'] = name

        current_index = INDEX_NAME_START + name_length

        remaining_packet_size = len(packet[current_index:])

        if SIZE_HUMIDITY_AND_TEMP == remaining_packet_size or SIZE_TEMPERATURE == remaining_packet_size:
            temperature = parse_temperature(current_index, packet)
            log_entry['temperature'] = temperature
            if remaining_packet_size == SIZE_HUMIDITY_AND_TEMP:
                current_index += SIZE_TEMPERATURE

        if SIZE_HUMIDITY_AND_TEMP == remaining_packet_size or SIZE_HUMIDITY == remaining_packet_size:
            humidity = parse_humidity(current_index, packet)
            log_entry['humidity'] = humidity

        return log_entry


def parse_timestamp(packet):
    b_timestamp = packet[INDEX_PACKET_LENGTH:INDEX_TIMESTAMP]
    timestamp = convert_timestamp(b_timestamp)
    return timestamp


def convert_timestamp(b_timestamp):
    tzone = current_tz()
    s_timestamp = get_byteorder(b_timestamp)
    timestamp = datetime.fromtimestamp(s_timestamp / 1000, tzone).replace(microsecond=0).isoformat()
    return timestamp


def get_byteorder(b_packet_length):
    return int.from_bytes(b_packet_length, 'big', signed=False)


def parse_temperature(current_index, packet):
    b_temperature = packet[current_index:current_index + SIZE_TEMPERATURE]
    temperature = convert_temperature(b_temperature)
    return temperature


def convert_temperature(b_temperature):
    temperature_in_kalvin = get_byteorder(b_temperature)
    temperature_in_celsius = float((Decimal(str(temperature_in_kalvin/100)) - 273)
                                   .quantize(Decimal('0.01')).to_eng_string())
    return temperature_in_celsius


def parse_humidity(current_index, packet):
    b_humidity = packet[current_index:]
    humidity = convert_humidity(b_humidity)
    return humidity


def convert_humidity(b_humidity):
    humidity = get_byteorder(b_humidity)
    return float(Decimal(str(humidity / 10)).quantize(Decimal('.1')).to_eng_string())

def current_tz():
    if time.daylight:
        return timezone(timedelta(seconds=-time.altzone),time.tzname[1])
    else:
        return timezone(timedelta(seconds=-time.timezone),time.tzname[0])

