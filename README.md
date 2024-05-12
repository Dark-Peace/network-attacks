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
Only a firewall drop policy is needed such that every request to any port that is not in the white list is rejected :
```sh
nft add rule inet filter input dport {22, 80, 443} accept
```
this rule only accepts packets with port 22,80 or 443 as destination making it impossible for network scans to succeed. We can do the same with the source ports as except for the ones listed before we shouldn't need any other :
```sh
nft add rule inet filter input sport {22, 80, 443} accept
```
