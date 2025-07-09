"""GraphQL client handling, including LinearStream base class."""

from datetime import timedelta
from typing import Any, Iterable, Optional

import requests
import time
import datetime
from singer_sdk.authenticators import APIKeyAuthenticator, BearerTokenAuthenticator
from singer_sdk.streams import GraphQLStream
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError


class LinearStream(GraphQLStream):
    """Linear stream class."""
    extra_retry_statuses = [429, 104, 101]

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        token = self.config.get("access_token") or self.config.get("auth_token")
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

    def get_response_status_code(self, response: requests.Response) -> int:
        """Try to get the status_code from the body if it's an error response.
            For example, if the response is a 429 error, the response.status_code will be 400.
        """
        status_code = response.status_code
        try:
            if status_code >= 400:
                for error in response.json().get("errors", []):
                    code = error.get("extensions", {}).get("statusCode")
                    if code:
                        status_code = code
                        break
        except Exception as e:
            self.logger.error(f"Error parsing response status code: {response.text} {e}")

        return status_code

    def handle_rate_limit_error(self, response: requests.Response) -> None:
        """Handle rate limit error."""
        self.logger.error(f"Rate limit exceeded: {response.text}")
        retry_after_timestamp = response.headers.get("x-ratelimit-requests-reset")
        if retry_after_timestamp:
            retry_after = int(retry_after_timestamp) / 1000
            now = datetime.datetime.now(datetime.timezone.utc)
            dt = datetime.datetime.fromtimestamp(retry_after, tz=datetime.timezone.utc)
            retry_after = (dt - now).total_seconds()
            self.logger.info(f"Rate limit exceeded. Retrying in {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            self.logger.error(f"Rate limit exceeded. No retry after timestamp found.")

    def validate_response(self, response: requests.Response) -> None:
        status_code = self.get_response_status_code(response)
        if (
            status_code in self.extra_retry_statuses
            or 500 <= status_code < 600
        ):
            if status_code == 429:
                self.handle_rate_limit_error(response)
            msg = self.response_error_message(response)
            raise RetriableAPIError(msg, response)
        elif 400 <= status_code < 500:
            msg = self.response_error_message(response)
            raise FatalAPIError(msg)

    def response_error_message(self, response: requests.Response) -> str:
        status_code = self.get_response_status_code(response)
        if 400 <= response.status_code < 500:
            error_type = "Client"
        else:
            error_type = "Server"

        return (
            f"{response.status_code} {error_type} Error: "
            f"{response.text} for path: {self.path}"
        )