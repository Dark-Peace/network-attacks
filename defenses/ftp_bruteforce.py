from topo import net
from mininet.log import info

if __name__ == "__main__":
    info(net['ftp'].cmd("nft add chain inet filter input_ftp {type filter hook input priority 0;}"))
    info(net['ftp'].cmd("nft add rule inet filter input_ftp tcp dport 21 limit rate over 3/minute burst 1 packets counter drop"))