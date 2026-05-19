import json
import requests
from datetime import datetime
import csv
import os

def save_payload(payload):

    # Validate the payload
    if "ip" not in payload: return
    if "results" not in payload: return
    if "flags" not in payload: return

    # Validate the IP address and skip if it's a multicast or reserved address
    ip = payload["ip"]
    firstOctet = int(ip.split(".")[0])
    if firstOctet >= 224 and firstOctet <= 239: return # Skip multicast addresses
    if firstOctet >= 240 and firstOctet <= 255: return # Skip reserved addresses

    # Make sure /data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Make sure /data/{firstOctet}.jsonl exists
    if not os.path.exists(f"data/{firstOctet}.jsonl"):
        with open(f"data/{firstOctet}.jsonl", "w") as f:
            pass

    # Check if the IP already exists in the file, if it does, update the existing entry instead of adding a new one
    exists = False
    
    # Open /data/{firstOctet}.jsonl and check if the IP already exists
    jsonList = []
    with open(f"data/{firstOctet}.jsonl", 'r') as json_file:
        jsonList = list(json_file)

    for record in jsonList:
        
        # Skip empty lines
        if record.strip() == "": continue

        jsonLine = json.loads(record)
        if jsonLine["ip"] == ip:
            exists = True

            # If the IP already exists, update the existing entry
            jsonLine["flags"] = list(set(jsonLine["flags"] + payload["flags"]))
            jsonLine["results"] = list(jsonLine["results"] + payload["results"])

            # Write the updated entry back to the file at the same line
            with open(f"data/{firstOctet}.jsonl", 'w') as json_file:
                for line in jsonList:
                    if line == record:
                        json_file.write(json.dumps(jsonLine) + "\n")
                    else:
                        json_file.write(line)
            break

    # If the IP doesn't already exist, add it to the file
    if not exists:
        with open(f"data/{firstOctet}.jsonl", "a") as f:
            f.write(json.dumps(payload) + "\n")

def aggregate_git_data(data):

    filePath = f"{data["file_format"]}".replace("YYYY", str(datetime.now().year)).replace("MM", str(datetime.now().month).rjust(2, "0")).replace("DD", str(datetime.now().day).rjust(2, "0"))
    print(data["url_raw"] + filePath)

    r = requests.get(data["url_raw"] + filePath)
    body = r.text

    if data["type"] == "csv":
        reader = csv.reader(body.splitlines())
        for row in reader:
            
            ip = row[0];flag = row[1];port = row[2];score = row[3];country = row[4];time = row[5];
            if ip == "IP": continue

            save_payload({
                "ip": ip,
                "results": [
                    {
                        "source": data["name"],
                        "datetime": datetime.now().isoformat(),
                        "flags": [
                            flag
                        ]
                    }
                ],
                "flags": [
                    flag
                ]
            })

def main():

    # Load the sources from the JSON file
    sources = {}
    with open("sources.json", "r") as f:
        sources = json.load(f)

    for source in sources.get("git", []):
        aggregate_git_data(source)

if __name__ == "__main__":
    main()