import os
import requests
from google.auth import compute_engine
import google.auth.transport.requests

class NotebookLMClient:
    """A client to interact with the NotebookLM Enterprise API."""
    
    def __init__(self, project_id, location="us-central1"):
        self.project_id = project_id
        self.location = location
        self.base_url = f"https://discoveryengine.googleapis.com/v1/projects/{project_id}/locations/{location}/collections/default_collection/dataStores/default_data_store/notebooks"
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        """Fetches the Google Cloud access token."""
        try:
            credentials, project = google.auth.default(
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            auth_req = google.auth.transport.requests.Request()
            credentials.refresh(auth_req)
            return credentials.token
        except Exception as e:
            print(f"Error fetching access token: {e}")
            return None

    def create_notebook(self, title):
        """Creates a new notebook."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {"displayName": title}
        response = requests.post(self.base_url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"Notebook created: {response.json().get('name')}")
            return response.json().get('name')
        else:
            print(f"Failed to create notebook: {response.text}")
            return None

    def upload_source(self, notebook_name, file_path):
        """Uploads a PDF source to a specific notebook."""
        upload_url = f"https://discoveryengine.googleapis.com/v1/{notebook_name}/sources:uploadFile"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        files = {
            'file': open(file_path, 'rb')
        }
        response = requests.post(upload_url, headers=headers, files=files)
        if response.status_code == 200:
            print(f"Source uploaded successfully: {file_path}")
            return response.json()
        else:
            print(f"Failed to upload source: {response.text}")
            return None

if __name__ == "__main__":
    # Prototype: Assume project_id is set in environment
    project_id = os.getenv('GCP_PROJECT_ID', 'your-project-id')
    client = NotebookLMClient(project_id)
    
    # Example usage:
    # notebook_name = client.create_notebook("Course: Digital Marketing")
    # if notebook_name:
    #     client.upload_source(notebook_name, "data/transcripts/example_transcript.pdf")
