from flask import Flask, jsonify
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta

app = Flask(__name__)

# Replace the following connection string, container name, blob name, and account key with your own values
connection_string = "DefaultEndpointsProtocol=https;AccountName=stgnie;AccountKey=3ZzxTtOsD00gpQ/gZdgvFezU2L4f+7xZhgFXELgsVM3ZOKLlRMrtNoBs42w3d+OvjsjTHwLIdUob+AStU3x9cg=="
container_name = "ctcnie"
blob_name = "dir1/dir2/sample.png"
account_name = "stgnie"
account_key = "3ZzxTtOsD00gpQ/gZdgvFezU2L4f+7xZhgFXELgsVM3ZOKLlRMrtNoBs42w3d+OvjsjTHwLIdUob+AStU3x9cg=="

@app.route('/')
def index():
    return "To get a SAS token, use the following URL format: /get_sas/<int:days>"

@app.route('/get_sas/<int:days>')
def sas_url(days):
    # Create a BlobServiceClient instance
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Set the expiration timestamp based on the number of days specified in the URL
    expiry_timestamp = datetime.utcnow() + timedelta(days=days)

    # Define the permissions you want to grant (e.g., read-only)
    permissions = BlobSasPermissions(read=True)

    # Generate the SAS token for the blob with the specified permissions and expiration time
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=permissions,
        expiry=expiry_timestamp,
    )

    # Construct the SAS URL with timestamp
    sas_url_with_timestamp = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

    # Create a dictionary with the SAS URL
    response_data = {
        "sas_url": sas_url_with_timestamp
    }

    # Return the response as JSON
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
