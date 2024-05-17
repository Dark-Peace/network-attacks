# Network Attacks

By Robin-Gilles Becker (NOMA:70552301 ULBID:521513) and Aguililla Klein Esteban (ULBID:514341, NOMA:31862301)

# Attacks

Attack scripts can be run from a host using the command
```sh
[host] python attacks/[script.py]
```

## FTP bruteforce
This attack was easier to implement with python standard library ftplib as it spared us from crafting packets by hand with Scapy. Furthermore, when doing the attack with scapy the 3whs was reseted by the (we think) the kernel as the connection was launched from user space and running it with sudo wouldn't change anything.

The idea behind is very simple, we will try a password list with the username mininet until it works. To launch the attack, (from the internet)

## ARP Poisoning
ARP Poisoning Ssends fake ARP replies in order for the attacker to forward traffic to its machine. Here we consider the case where ws3 is the malicious entity sending the attack. It spams ws2 and r1 with their ip address associated to ws3's own mac address to make them both think that they're talking to each others. ws3 becomes a man-in-the-middle. Stop the packet spam with CTRL-C.

## ARP Netowrk Scan
This script returns the list of hosts it found on the network. This attack uses the ARP protocol.

## Reflected DNS DOS
The internet can launch this attack by asking the DNS server in the DMZ to resolve any server name and spoofing the source IP to the target : in our case ws2

# Defenses
Most of these attacks cannot be completely prevented, but we can make it more difficult for an attacker to disturb the network.

## Basic
### On the DMZ servers
we used an allow list for outgoing packets with the following rules:
- packets from curated ports (depending on the service eg. for http 22, 80, 443, 6010)
- packet to curated ports (depending on the service eg. for http 22, 80, 443, 6010)
- already established connections 
- ICMP echo-reply and destination-unreachable

we allow 22 and 6010 in order to maintain access to the terminal provided by mininet. In a real network, those ports should not be there.
### Router1
we use an allow list for forwarding:
- packets coming from 10.1.0.0/24
- already established connections 
- ICMP echo-reply and destination-unreachable
- DNS packets

We can check the result of our basic firewall by doing a pingall in mininet.

![image](https://github.com/Dark-Peace/network-attacks/assets/74102789/925c7159-6ebf-45af-b9c5-3a5389ed5cb6)

We can see the DMZ cannot ping anything, but can be pinged by everyone. Workstations can ping everyone but can't be reached by the internet.
Even with the following specific defense scripts active, this pingall doesn't change, proving the normal use of the network is still possible after all our defenses.

Defense scripts can be applied on a host using the command
```sh
[host] ./defenses/[script.sh]
```

## FTP bruteforce
To make the attack harder, we implement rate limiting. It will then be way harder to go through an entire list of common passwords. In order to be a little lenient for people who mistyped their passwords, we allow 3 tries per minute. This nft rule only acts on port 21, the ftp port.
```sh
ftp ./defenses/ftp_bruteforce.sh
```

## ARP Poisoning
The attack is based on the spam of 2 targets. By adding a rate limit rule to potential targets, we lower the chances for the host to fall victim to the attack.
Following the example used above, this rule could be added to ws2
```sh
ws2 ./defenses/arp_poison.sh
```

## Network scans
Protection against port scan is already builtin in the base firewall rules that were asked as for resuming normal functions of the DMZ servers, we must leave open the used ports. To do so, we use a policy drop and accept only the required ports
```sh
nft add rule inet ${HOST}_filter ${HOST}_output sport ${ALLOW_LIST_PORTS} accept
nft add rule inet ${HOST}_filter ${HOST}_output dport ${ALLOW_LIST_PORTS} accept
```

We still added a scan.sh protection for good measure. We thought of adding rate limitting to the router in the forward chain. However, it seemed that forwarding rules aren't supported for arp. Instead, we decided to implement the rate limitting on the hosts that might get hacked and used for network scanning.
```sh
ftp ./defenses/scan.sh
```

## Reflected DNS DOS
In order to defend against a reflected DOS we used rate limitation in the same way as the ftp brute force. This is a tradeoff as the rate is limited for everyone

```sh
nft add chain inet dns_filter input '{type filter hook input priority 0; policy accept;}'
nft add rule inet dns_filter input udp dport 5353 limit rate over 3/minute burst 1 packets counter drop
```

```sh
dns ./defenses/reflected_dns_dos.sh
```
