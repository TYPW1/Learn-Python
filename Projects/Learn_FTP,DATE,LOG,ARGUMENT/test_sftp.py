import pysftp

# Connection details
HOST = "test.rebex.net"
USER = "demo"
PASS = "password"

# we need this line to avoid a host key error
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

print(f"Connecting to {HOST} as {USER}")

# Use 'with' to ensure the connection is closed after use or auto-connect and auto-disconnect
try:
    with pysftp.Connection(HOST, username=USER, password=PASS, cnopts=cnopts) as sftp:
        print("Connection successfull")

        # 1. List the directories/files in the remote home folder
        print("Remote directory listing:")
        files = sftp.listdir()
        for f in files:
            print(f" - {f}")
        
        # 2. Download a file from the remote server
        
except Exception as e:
    print(f"An error occurred: {e}")
    print(f"Failed to connect to {HOST} as {USER}")

print("Script finished.")