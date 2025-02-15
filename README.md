# igate_syslog
Receives syslog data from an iGate LoRa APRS and stores it, and sends searched texts to a Bot

This exercise code receives syslog data from an iGate by [CA2RXU](https://github.com/richonguzman/LoRa_APRS_iGate)<br>

It is possible to set a search pattern on the received data (for example for messages) and send the filtered content (for example by specifying a hamradio callsign) to a telegram bot. The same can be used for igate_frombot. You need to edit the code in the configuration section and specify the token and chat id of the bot, and other customizations. The data received from the gateway/digipeater can be saved to a file.<br>
![](https://github.com/ik5xmk/igate_syslog/blob/main/igate_syslog_02.jpg)<br>

Finally run the code with the command **nohup python3 igate_syslog.py &**<br>

iGate LoRa also needs to be configured with the IP and port of the syslog listening of the small server.<br>
![](https://github.com/ik5xmk/igate_syslog/blob/main/igate_syslog_01.jpg)<br>

When the given pattern is found in the received data this text will be sent to the bot (from the pattern to the end of the line). A practical use is to receive messages from APRS (which will be sent to the iGate callsign) on telegram.<br>

![](https://github.com/ik5xmk/igate_syslog/blob/main/igate_syslog_03.jpg)<br>
