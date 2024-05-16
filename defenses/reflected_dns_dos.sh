nft add chain inet dns_filter input '{type filter hook input priority 0; policy accept;}'
nft add rule inet dns_filter input udp dport 53 limit rate over 3/minute burst 1 packets counter drop
