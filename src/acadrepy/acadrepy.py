import requests
from requests_ntlm import HttpNtlmAuth


class AcadreClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_cookie = None
        self.username = username
        self.password = password

        requests.packages.urllib3.disable_warnings()

    def get_authentication_url(self):
        """
        Get the initial authentication URL from the Acadre API.
        """
        url = f"{self.base_url}/Frontend/AuthService/GetLoginUrl"
        response = self.session.get(url, verify=False)  # Disable SSL verification
        if response.status_code == 200:
            return response.text.strip()
        else:
            raise Exception(
                f"Failed to get authentication URL. Status Code: {response.status_code}"
            )

    def authenticate(self):
        """
        Authenticate using the authentication URL obtained from get_authentication_url.
        """
        auth_url = self.get_authentication_url()
        response = self.session.get(
            auth_url, auth=HttpNtlmAuth(self.username, self.password), verify=False
        )  # Use NTLM authentication
        if response.status_code == 200:
            # Extracting the authentication cookie from the response
            self.auth_cookie = response.cookies.get(".acadre_st")
            if not self.auth_cookie:
                raise Exception("Failed to retrieve authentication token.")
            self.session.cookies.set(".acadre_st", self.auth_cookie)
        else:
            raise Exception(
                f"Authentication failed. Status Code: {response.status_code}"
            )

    def get_documents_by_searchterm_paged(self, search_term, page_index, page_size):
        """
        Get documents information based on a search term with pagination.
        """
        url = f"{self.base_url}/Frontend/api/v11/mainDocument?SearchTerm={search_term}&page-index={page_index}&page-size={page_size}"
        headers = {"Accept": "application/json"}
        response = self.session.get(
            url, headers=headers, verify=False
        )  # Disable SSL verification
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to get documents by search term. Status Code: {response.status_code}"
            )

    def download_document_by_id(self, document_id, out_file):
        """
        Download a document by its ID and save it to the specified file.
        """
        url = f"{self.base_url}/Frontend/api/v11/mainDocument/{document_id}/Download"
        headers = {"Accept": "application/json"}
        response = self.session.get(
            url, headers=headers, verify=False, stream=True
        )  # Disable SSL verification
        if response.status_code == 200:
            with open(out_file, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            raise Exception(
                f"Failed to download document. Status Code: {response.status_code}"
            )
