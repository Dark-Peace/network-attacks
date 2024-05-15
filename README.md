# network-attacks
# attacks
## ftp bruteforce
This attack was easier to implement with python standard library ftplib as it spared us from crafting packets by hand with Scapy. Furthermore, when doing the attack with scapy the 3whs was reseted by the (we think) the kernel as the connection was launched from user space and running it with sudo wouldn't change anything.

The idea behind is very simple, we will try a password list with the username mininet until it works. To launch the attack, (from the internet)
```sh
python fpt_bruteforce.py
```
# defenses
## Network scans
Protection against port scan is already builtin in the base firewall rules that were asked as for resuming normal functions of the DMZ servers, we must leave open the used ports. To do so, we use a policy drop and accept only the required ports
```sh
nft add rule inet ${HOST}_filter ${HOST}_output sport ${ALLOW_LIST_PORTS} accept
nft add rule inet ${HOST}_filter ${HOST}_output dport ${ALLOW_LIST_PORTS} accept
```
