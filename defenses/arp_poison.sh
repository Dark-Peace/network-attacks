# for ws2 and ws3
nft add table arp filter
nft add chain arp filter input '{type filter hook input priority 0; policy accept;}'
nft add rule arp filter input type arp request limit rate 5/minute accept