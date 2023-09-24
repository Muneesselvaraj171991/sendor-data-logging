from datetime import date, datetime, timezone
from decimal import Decimal
import pytz

# packet position constants
SIZE_HUMIDITY = 2
SIZE_TEMPERATURE = 3
SIZE_HUMIDITY_AND_TEMP = 5
INDEX_NAME_START = 13
INDEX_TIMESTAMP = 12
INDEX_PACKET_LENGTH = 4

DEFAULT_TIMEZONE = 'Europe/Stockholm'

class LogParser:

    def __init__(self):
        pass


    def parse_packet(self, packet):
        log_entry = {}

        timestamp = _parse_timestamp(packet)
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
            temperature = _parse_temperature(current_index, packet)
            log_entry['temperature'] = temperature
            if remaining_packet_size == SIZE_HUMIDITY_AND_TEMP:
                current_index += SIZE_TEMPERATURE

        if SIZE_HUMIDITY_AND_TEMP == remaining_packet_size or SIZE_HUMIDITY == remaining_packet_size:
            humidity = _parse_humidity(current_index, packet)
            log_entry['humidity'] = humidity

        return log_entry


def _parse_packet_length(packet):
    b_packet_length = packet[:INDEX_PACKET_LENGTH]
    packet_length = _convert_packet_length(b_packet_length)
    return packet_length


def _parse_timestamp(packet):
    b_timestamp = packet[INDEX_PACKET_LENGTH:INDEX_TIMESTAMP]
    timestamp = _convert_timestamp(b_timestamp)
    return timestamp


def _convert_timestamp(b_timestamp):
    tzone = pytz.timezone(DEFAULT_TIMEZONE)
    s_timestamp = int.from_bytes(b_timestamp, 'big', signed=False)
    timestamp = datetime.fromtimestamp(s_timestamp / 1000, tzone).replace(microsecond=0).isoformat()
    # print(timestamp)
    return timestamp


def _convert_packet_length(b_packet_length):
    return int.from_bytes(b_packet_length, 'big', signed=False)


def _parse_temperature(current_index, packet):
    b_temperature = packet[current_index:current_index + SIZE_TEMPERATURE]
    temperature = _convert_temperature(b_temperature)
    return temperature


def _convert_temperature(b_temperature):
    temperature_in_kalvin = int.from_bytes(b_temperature, 'big', signed=False)
    temperature_in_celsius = float((Decimal(str(temperature_in_kalvin/100)) - 273)
                                   .quantize(Decimal('0.01')).to_eng_string())
    return temperature_in_celsius


def _parse_humidity(current_index, packet):
    b_humidity = packet[current_index:]
    humidity = _convert_humidity(b_humidity)
    return humidity


def _convert_humidity(b_humidity):
    humidity = int.from_bytes(b_humidity, 'big', signed=False)
    return float(Decimal(str(humidity / 10)).quantize(Decimal('.1')).to_eng_string())
