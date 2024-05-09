from scapy.all import ARP, Ether, srp

network = '10.1.0.0/24'

def arp_scan():
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network)
    result = srp(arp_request, iface="eth0", timeout=1, verbose=False)[0]

    for device in result:
        print(device[1].psrc, device[1].hwsrc)

if __name__ == "__main__":
    print("Scanning network...")
    scan_results = arp_scan()
    print("Scan complete.")