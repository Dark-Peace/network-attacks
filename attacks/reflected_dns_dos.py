from scapy.all import IP, UDP, DNS, DNSQR, send

if __name__ == "__main__":
    req = IP(dst="10.12.0.20", src="10.1.0.2") / UDP() / DNS(rd=1,qd=DNSQR(qname="10.1.0.3", qtype='PTR'))
    send(req)
