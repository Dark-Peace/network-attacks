# network-attacks
# defense
## Network scans
Only a firewall drop policy is needed such that every request to any port that is not in the white list is rejected :
```sh
nft add rule inet filter input dport {22, 80, 443} accept
```
this rule only accepts packets with port 22,80 or 443 as destination making it impossible for network scans to succeed. We can do the same with the source ports as except for the ones listed before we shouldn't need any other :
```sh
nft add rule inet filter input sport {22, 80, 443} accept
```
