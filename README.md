# igate_syslog
Receives syslog data from an iGate LoRa APRS and stores it, and sends searched texts to a Bot

This exercise code receives syslog data from an iGate by [CA2RXU](https://github.com/richonguzman/LoRa_APRS_iGate)<br>

It is possible to set a search pattern on the received data (for example for messages) and send the filtered content (for example by specifying a hamradio callsign) to a telegram bot. The same can be used for igate_frombot. You need to edit the code in the configuration section and specify the token and chat id of the bot, and other customizations. I dati ricevuti dal gateway/digipeater possono essere salvati in un file. Alla fine metti in esecuzione il codice con il comando **nohup python3 igate_syslog.py &**<br>

iGate LoRa also needs to be configured with the IP and port of the syslog listening of the small server.<br>

When the given pattern is found in the received data this text will be sent to the bot (from the pattern to the end of the line). A practical use is to receive messages from APRS (which will be sent to the iGate callsign) on telegram.
