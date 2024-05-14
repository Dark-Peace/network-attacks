from scapy.all import IP, UDP, DNS, DNSQR, send

if __name__ == "__main__":
    req = IP(dst="10.12.0.20", src="10.1.0.2") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="example.com"))
    send(req, count=100)
