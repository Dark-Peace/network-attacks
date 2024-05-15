nft add chain inet dns_filter dns_input '{type filter hook input priority 0; policy drop;}'
nft add rule inet dns_filter dns_input udp dport 53 limit rate over 3/minute burst 1 packets counter drop
