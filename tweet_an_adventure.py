
from src import main

adventure_path = "data/adventure1.yaml"
credential_path = "credentials.yaml"

if __name__ == "__main__":
    api = main.parse_credentials(credential_path)
    result = main.create_adventure(adventure_path, api)
    print("adventure complete, check your twitter feed")
