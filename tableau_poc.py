import tableauserverclient as TSC
from dotenv import load_dotenv
import os

e = load_dotenv(".tableau_env")

TABLEAU_USERNAME = os.environ.get("TABLEAU_USERNAME")
TABLEAU_PASSWORD = os.environ.get("TABLEAU_PASSWORD")
TABLEAU_SITENAME = os.environ.get("TABLEAU_SITENAME")
TABLEAU_SERVER_URL = os.environ.get("TABLEAU_SERVER_URL")
# for auth via token
TABLEAU_TOKEN_NAME = os.environ.get("TABLEAU_TOKEN_NAME")
TABLEAU_TOKEN_VALUE = os.environ.get("TABLEAU_TOKEN_VALUE")


class TableauServer:
    def __init__(
        self,
        tableau_token_name,
        tableau_token_value,
        tableau_sitename,
        tableau_server_url,
    ):
        self.tableau_token_name = tableau_token_name
        self.tableau_token_value = tableau_token_value
        self.tableau_sitename = tableau_sitename
        self.tableau_server_url = tableau_server_url
        self._server = self._connect()

    def _connect(self):
        tableau_auth = TSC.PersonalAccessTokenAuth(
            self.tableau_token_name, self.tableau_token_value, self.tableau_sitename
        )
        server = TSC.Server(
            f"https://{self.tableau_server_url}", use_server_version=True
        )
        server.auth.sign_in(tableau_auth)
        return server

    def get_workbooks(self):
        result = self._server.workbooks.get()
        workbooks = [
            (
                i.content_url,
                i.created_at,
                i.id,
                i.name,
                i.owner_id,
                i.project_id,
                i.project_name,
                i.size,
                i.show_tabs,
                i.hidden_views,
                i.tags,
                i.updated_at,
                i.webpage_url,
            )
            for i in result[0]
        ]
        return workbooks
