network = {"1.1": "Agent A", "1.2": "Agent B"}
target = input("Target IP: ")
if target in network:
    print("Sending to " + network[target])
else:
    print("Error: 404 Address Not Found")