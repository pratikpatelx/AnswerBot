# Imports the Google Cloud client library
from google.cloud import storage
from google.cloud import bigquery


def explicit():
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('C:/Users/prati/Desktop/COMP SCIENCE/COMP 4060 - Data Driven Software Engineering/Project/COMP 4060-1571c831e97f.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

if __name__ == "__main__":
    explicit()