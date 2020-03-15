import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import numpy as np

rp = scpi.scpi('192.168.128.1')
rp.tx_txt('ACQ:START')
rp.tx_txt('ACQ:SOUR1:DATA?')
str = rp.rx_txt()

measRes = np.fromstring(str[1:-1],dtype=float,sep=',')
plt.plot(measRes)
plt.pause(1)