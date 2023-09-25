from logging import Logger
import subprocess
import os
from flask import Flask, jsonify, request
from threading import Thread

from Logger import DataLogger
from LogParser import LogParser

INDEX_PACKET_LENGTH_OFFSET = 4
 
# creating a Flask app
app = Flask(__name__)
logger = DataLogger()
data_parser = LogParser()  
  
@app.route('/sensor_data', methods = ['GET'])
def sendor_data():
  pkg_in_json = []
  #Reading collected binary
  collected_binary = logger.read()
  total_data_length = len(collected_binary)

  if(total_data_length > 0):

    remaining_data = collected_binary
    remaining_data = remaining_data[:-1] if remaining_data[-1] == '\n' else remaining_data

    length_of_packets_parsed = 0

    while length_of_packets_parsed < total_data_length:

        current_packet_length = int.from_bytes(remaining_data[:INDEX_PACKET_LENGTH_OFFSET], 'big', signed=False)

        if current_packet_length > len(remaining_data):
                partial_packet = remaining_data
                print('partial_packet - ', partial_packet)
                break

        packet = remaining_data[:current_packet_length]

        pkg_in_json.append(data_parser.parse_packet(packet))

        length_of_packets_parsed += current_packet_length
        remaining_data = remaining_data[current_packet_length:]
    
  else:
      print("payload is empty")
        
  return jsonify(pkg_in_json)
  
def read_sensor_data():
    sensor_data_binary_read = b'' 
 

    directory = os.getcwd()
    command = directory+"\sensor-server\simulation\sensor_data.x86_64-pc-windows-gnu.exe",
    print("Sensor simulator started at: ", command)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


    while True:
        sensor_data_binary_read = process.stdout.readline()

        logger.write(sensor_data_binary_read)        
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            for stdio in process.stdout.readlines():
                print(stdio.strip())
                if stdio != '':
                    logger.write(stdio)

            break

  
if __name__ == '__main__':
    #Starting sensor simulation on background thread to let flask server running in main thread
    thread = Thread(target=read_sensor_data,)
    thread.daemon = True
    thread.start()
    #Since it is the assignment , I am hosting server in HTTP, can be configured as https if needed.
    app.run(host='0.0.0.0', debug=True)
