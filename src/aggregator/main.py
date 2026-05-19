import json
import requests

def aggregate_git_data(data):
    print(data)

def main():

    # Load the sources from the JSON file
    sources = {}
    with open("sources.json", "r") as f:
        sources = json.load(f)

    for source in sources.get("git", []):
        aggregate_git_data(source)


if __name__ == "__main__":
    main()