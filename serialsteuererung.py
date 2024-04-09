import serial
import time

# Verbindung herstellen (angepasst je nach Ihrem Setup)
ser = serial.Serial('COM6', 115200) # Anpassen Sie den Port und die Baudrate entsprechend

try:
    while True:
        # Daten vom Benutzer eingeben
        data_to_send = input("Enter data to send: ")
        
        # Daten an Arduino senden
        ser.write(data_to_send.encode())
        
        # Kurze Verzögerung, um Zeit für die Verarbeitung auf Arduino-Seite zu geben
        time.sleep(0.1)
        

        response = ""
        while response != "gedreht":
            response = ser.readline().decode().strip()
            time.sleep(0.1) 

        print("Response from Arduino:", response)

except KeyboardInterrupt:
    ser.close()
    print("Program terminated.")