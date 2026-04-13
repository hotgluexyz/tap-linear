"""Linear OAuth authenticator."""

from hotglue_singer_sdk.authenticators import OAuthAuthenticator


class LinearOAuthAuthenticator(OAuthAuthenticator):
    """OAuth authenticator for Linear using refresh_token grant."""

    @property
    def oauth_request_payload(self) -> dict:
        return {
            "client_id": self._tap.config.get("client_id"),
            "client_secret": self._tap.config.get("client_secret"),
            "refresh_token": self._tap.config.get("refresh_token"),
            "grant_type": "refresh_token",
        }
