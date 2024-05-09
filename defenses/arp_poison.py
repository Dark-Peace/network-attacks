from topo import net
from mininet.log import info

if __name__ == "__main__":
    for pc in ["ws2","ws3"]:
        info(net[pc].cmd("nft add table arp filter"))
        info(net[pc].cmd("nft add chain arp filter input {type filter hook input priority 0; policy accept;}"))
        info(net[pc].cmd("nft add rule arp filter input type arp request limit rate 5/minute accept"))