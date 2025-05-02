"""GraphQL client handling, including LinearStream base class."""

from datetime import timedelta
from typing import Any, Iterable, Optional

import requests
from singer_sdk.authenticators import APIKeyAuthenticator, BearerTokenAuthenticator
from singer_sdk.streams import GraphQLStream
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from dotenv import load_dotenv
import os

load_dotenv()

class LinearStream(GraphQLStream):
    """Linear stream class."""
    extra_retry_statuses = [429, 104, 101]

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        token = self.config.get("access_token") or self.config.get("auth_token") or os.getenv(
            "LINEAR_ACCESS_TOKEN"
        )
        if not token:
            raise FatalAPIError("Access token or auth token required")
        if self.config.get("access_token"):
            return BearerTokenAuthenticator.create_for_stream(self, token=token)
        # Fallback to API key
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value=token,
            location="header",
        )

    @property
    def url_base(self) -> str:
        return self.config.get("api_url")

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.models.Response, previous_token: Optional[Any]
    ) -> Any:
        """Return the next page token."""
        resp_json = response.json()
        if resp_json["data"][self.name]["pageInfo"]["hasNextPage"]:
            return resp_json["data"][self.name]["pageInfo"]["endCursor"]
        else:
            return None

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Return the request payload."""
        variables = {"next": next_page_token}
        starting_timestamp_replication_key_value = self.get_starting_timestamp(context)
        if starting_timestamp_replication_key_value:
            value = (starting_timestamp_replication_key_value + timedelta(seconds=1)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            variables["replicationKeyValue"] = value
            self.logger.info(f"Previous state timestamp: {value}")
        else:
            self.logger.info(f"Previous state timestamp not provided. Stream: {self.name}")
        if context:
            variables.update(context)
        body = {
            "query": self.query,
            "variables": variables,
        }
        return body

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        for row in resp_json["data"][self.name]["nodes"]:
            yield row
    
    def validate_response(self, response: requests.Response) -> None:

        if (
            response.status_code in self.extra_retry_statuses
            or 500 <= response.status_code < 600
        ):
            msg = self.response_error_message(response)
            raise RetriableAPIError(msg, response)
        elif 400 <= response.status_code < 500:
            msg = self.response_error_message(response)
            raise FatalAPIError(msg)

    def response_error_message(self, response: requests.Response) -> str:

        if 400 <= response.status_code < 500:
            error_type = "Client"
        else:
            error_type = "Server"

        return (
            f"{response.status_code} {error_type} Error: "
            f"{response.text} for path: {self.path}"
        )
