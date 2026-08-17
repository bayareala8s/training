import paramiko
import os

def list_sftp_recursive(sftp, remote_path, file_list):
    for item in sftp.listdir_attr(remote_path):
        item_path = os.path.join(remote_path, item.filename).replace("\\", "/")
        if stat.S_ISDIR(item.st_mode):  # ✅ Use stat.S_ISDIR here
            file_list.append(f"[DIR]  {item_path}")
            list_sftp_recursive(sftp, item_path, file_list)
        else:
            file_list.append(f"[FILE] {item_path}")

def main():
    hostname = "sftp.example.com"
    port = 22
    username = "your_username"
    password = "your_password"  # Or use private key

    output_file = "sftp_listing.txt"

    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    file_list = []
    list_sftp_recursive(sftp, "/", file_list)

    with open(output_file, "w", encoding="utf-8") as f:
        for line in file_list:
            f.write(line + "\n")

    print(f"✔️ SFTP file list saved to {output_file}")

    sftp.close()
    transport.close()

if __name__ == "__main__":
    main()
