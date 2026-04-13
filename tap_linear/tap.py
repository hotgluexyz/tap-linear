"""Linear tap class."""

from typing import List

from hotglue_singer_sdk import Stream, Tap
from hotglue_singer_sdk import typing as th

from tap_linear.auth import LinearOAuthAuthenticator
from tap_linear.streams import (
    CommentsStream,
    IssuesStream,
    ProjectsStream,
    TeamsStream,
    UsersStream,
    LabelsStream,
)

STREAM_TYPES = [
    IssuesStream,
    ProjectsStream,
    UsersStream,
    TeamsStream,
    CommentsStream,
    LabelsStream,
]


class TapLinear(Tap):
    """Linear tap class."""

    name = "tap-linear"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "access_token",
            th.StringType,
            description="OAuth access token",
        ),
        th.Property(
            "refresh_token",
            th.StringType,
            description="OAuth refresh token",
        ),
        th.Property(
            "client_id",
            th.StringType,
            description="OAuth client ID",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            description="OAuth client secret",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.linear.app/graphql",
            description="The URL for the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
            default="2010-01-01T00:00:00.000Z",
        ),
    ).to_dict()

    @classmethod
    def access_token_support(cls, connector=None):
        return (LinearOAuthAuthenticator, "https://api.linear.app/oauth/token")

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapLinear.cli()
