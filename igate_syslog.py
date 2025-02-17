import socket
import re
import requests
import datetime

# Configurazione
UDP_IP = "0.0.0.0"                      # Ascolta su tutte le interfacce
UDP_PORT = 9999
TELEGRAM_BOT_TOKEN = "INSERT-YOUR-TOKEN"
TELEGRAM_CHAT_ID = "INSERT-YOUR-CHAT-ID"
FILTER_PATTERN = r" / MESSAGE / "       # pattern desiderato
FILTER_CALL = r"---> IK5XMK"            # ulteriore filtro all'interno del pattern
LOG_FILE = "syslog.log"                 # nome del file syslog
LOG_ENABLED = True                      # True per abilitare la registrazione su file, False per disattivarla
LOG_ONLY_FILTERED = True                # True per salvare solo i messaggi filtrati, False per tutti

def log_message(message):
    """Salva il messaggio nel file di log se LOG_ENABLED è True."""
    if LOG_ENABLED:
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"[{timestamp}] {message}\n")

def send_telegram_message(message):
    """Invia un messaggio al bot Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Errore Telegram: {response.text}")
    except Exception as e:
        print(f"Errore nell'invio a Telegram: {e}")

def extract_message_after_pattern(message):
    """Estrae la parte del messaggio dopo il pattern trovato."""
    # RX / MESSAGE / IK5XMK-15 ---> IK5XMK-6  :test / -116dBm / -1.00dB / -221Hz
    # RX / MESSAGE / IK5ZXH-10 ---> IK5WJG-11:PARM.V_Batt,V_Ext / -117dBm / -2.50dB / 249Hz
    # RX / MESSAGE / IK5ZXH-10 ---> IK5XMK-15:Ppppppppppp{45 / -118dBm / -2.50dB / 123Hz
    # RX / MESSAGE / IK5XMK-15 ---> IK5XMK-7 :ack46 / -116dBm / -1.75dB / 216Hz
    # TX / MESSAGE / IZ5YBK-10 ---> IK5XMK-15:Qwerty{49
    match = re.search(FILTER_PATTERN, message)
    if match:
        if ( (len(FILTER_CALL)>1) & (FILTER_CALL in message) ): # c'è il secondo filtro e lo trova
            return message[message.index(FILTER_CALL):].strip()

        if (len(FILTER_CALL)>1): # c'è il secondo filtro e NON lo trova
            return None

        return message[match.end():].strip()  # NON c'è il secondo filtro impostato, ma il pattern coincide
    return None

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Ascolto sulla porta UDP {UDP_PORT} per messaggi syslog...")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8', errors='ignore').strip()
        log_entry = f"Syslog da {addr}: {message}"
        print(log_entry)

        # Log dei messaggi (tutti o solo quelli filtrati)
        if LOG_ENABLED and (not LOG_ONLY_FILTERED or re.search(FILTER_PATTERN, message)):
            log_message(log_entry)

        # Se il messaggio corrisponde al filtro, invialo a Telegram (solo parte successiva al pattern)
        filtered_message = extract_message_after_pattern(message)
        if filtered_message:
            send_telegram_message(filtered_message)

if __name__ == "__main__":
    main()
