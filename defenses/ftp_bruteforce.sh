# for ftp
nft add chain inet filter input_ftp '{type filter hook input priority 0;}'
nft add rule inet filter input_ftp tcp dport 21 limit rate over 3/minute burst 1 packets counter drop