"""
Mimics a small enterprise network, with 2 workstations in a trusted LAN,
and service-providing servers in a DMZ LAN.

Adapted from https://stackoverflow.com/questions/46595423/mininet-how-to-create-a-topology-with-two-routers-and-their-respective-hosts
"""

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.examples.linuxrouter import LinuxRouter
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time


class TopoSecu(Topo):

    def build(self):

        # Add 2 routers in two different subnets
        # Workstation LAN router
        r1 = self.addHost('r1', cls=LinuxRouter, ip=None)
        r2 = self.addHost('r2', cls=LinuxRouter, ip=None)  # Internet router

        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add router-switch links in the same subnet
        self.addLink(s1, r1, intfName2='r1-eth0',
                     params2={'ip': '10.1.0.1/24'})
        self.addLink(s2, r1, intfName2='r1-eth12',
                     params2={'ip': '10.12.0.1/24'})
        self.addLink(s2, r2, intfName2='r2-eth12',
                     params2={'ip': '10.12.0.2/24'})

        # Add outside host
        internet = self.addHost(
            name='internet', ip='10.2.0.2/24', defaultRoute='via 10.2.0.1')
        self.addLink(internet, r2, intfName2='r2-eth0',
                     params2={'ip': '10.2.0.1/24'})

        # Adding hosts specifying the default route
        ws2 = self.addHost(name='ws2', ip='10.1.0.2/24',
                           defaultRoute='via 10.1.0.1')
        ws3 = self.addHost(name='ws3', ip='10.1.0.3/24',
                           defaultRoute='via 10.1.0.1')
        httpServer = self.addHost(
            name='http', ip='10.12.0.10/24', defaultRoute='via 10.12.0.2')
        dnsServer = self.addHost(
            name='dns', ip='10.12.0.20/24', defaultRoute='via 10.12.0.2')
        ntpServer = self.addHost(
            name='ntp', ip='10.12.0.30/24', defaultRoute='via 10.12.0.2')
        ftpServer = self.addHost(
            name='ftp', ip='10.12.0.40/24', defaultRoute='via 10.12.0.2')

        # Add host-switch links
        self.addLink(ws2, s1)
        self.addLink(ws3, s1)
        self.addLink(httpServer, s2)
        self.addLink(dnsServer, s2)
        self.addLink(ntpServer, s2)
        self.addLink(ftpServer, s2)


def add_routes(net):
    ### STATIC ROUTES ###
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.12.0.2 dev r1-eth12"))
    info(net['r2'].cmd("ip route add 10.1.0.0/24 via 10.12.0.1 dev r2-eth12"))


def start_services(net: Mininet) -> None:
    """
    Start services on servers.
    :param net: Mininet network
    """
    # Apache2 HTTP server
    info(net['http'].cmd("/usr/sbin/apache2ctl -DFOREGROUND &"))
    # dnsmasq DNS server
    info(net['dns'].cmd("/usr/sbin/dnsmasq -k &"))
    # NTP server
    info(net['ntp'].cmd("/usr/sbin/ntpd -d &"))
    # FTP server
    info(net['ftp'].cmd("/usr/sbin/vsftpd &"))

    # SSH server on all servers
    cmd = "/usr/sbin/sshd -D &"
    for host in ['http', 'ntp', 'ftp', 'dns']:
        info(net[host].cmd(cmd))

    accepted_ports = {'http': "{22, 80, 443, 6010}", "ntp": "{22, 6010}",
                      "ftp": "{22, 20, 21, 6010}", "dns": "{6010, 22, 5353, 53}"}

    for host in ['http', 'ntp', 'ftp', 'dns']:
        info(net[host].cmd(f"nft add table inet {host}_filter"))
        info(net[host].cmd(f"nft add chain inet {host}_filter {host}_output '{{type filter hook output priority 0; policy drop;}}'"))

        info(net[host].cmd(f"nft add rule inet {host}_filter {host}_output tcp sport {accepted_ports[host]} accept"))
        info(net[host].cmd(f"nft add rule inet {host}_filter {host}_output tcp dport {accepted_ports[host]} accept"))
        info(net[host].cmd(f"nft add rule inet {host}_filter {host}_output udp sport {accepted_ports[host]} accept"))
        info(net[host].cmd(f"nft add rule inet {host}_filter {host}_output udp dport {accepted_ports[host]} accept"))

        info(net[host].cmd(f"nft add rule inet {host}_filter {host}_output ct state {{established, related}} accept"))

        info(net[host].cmd(f"nft add rule inet {host}_filter {host}_output icmp type '{{echo-reply, destination-unreachable}}'"))
        
    info(net['r1'].cmd("nft add table inet r1_filter")) # table
    info(net['r1'].cmd(
        "nft add chain inet r1_filter r1_forward '{type filter hook forward priority 0; policy drop;}'")) # chain
    info(net['r1'].cmd("nft add rule inet r1_filter r1_forward udp dport {53, 5353} accept")) # allowing dns packets
    info(net['r1'].cmd("nft add rule inet r1_filter r1_forward udp sport {53, 5353} accept")) # allowing dns packets

    info(net['r1'].cmd("nft add rule inet r1_filter r1_forward ip saddr 10.1.0.0/24 accept"))
    info(net['r1'].cmd("nft add rule inet r1_filter r1_forward ct state {established, related} accept"))
    info(net['r1'].cmd("nft add rule inet r1_filter r1_forward icmp type {echo-reply, destination-unreachable} accept"))


def stop_services(net: Mininet) -> None:
    """
    Stop services on servers.
    :param net: Mininet network
    """
    # Apache2 HTTP server
    info(net['http'].cmd("killall apache2"))
    # dnsmasq DNS server
    info(net['dns'].cmd("killall dnsmasq"))
    # OpenNTPd NTP server
    info(net['ntp'].cmd("killall ntpd"))
    # FTP server
    info(net['ftp'].cmd("killall vsftpd"))


def run():
    topo = TopoSecu()
    net = Mininet(topo=topo)

    add_routes(net)
    stop_services(net)
    time.sleep(1)
    start_services(net)

    net.start()
    CLI(net)
    stop_services(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
