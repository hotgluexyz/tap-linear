"""Stream type classes for tap-linear."""
from typing import Any, Iterable, Optional
import requests
from tap_linear.client import LinearStream
from tap_linear.queries.comments import commentsQuery
from tap_linear.queries.issues import issuesQuery
from tap_linear.queries.projects import projectsQuery
from tap_linear.queries.teams import teamsQuery
from tap_linear.queries.users import usersQuery
from tap_linear.queries.labels import labelsQuery
from tap_linear.schemas.comments import commentsSchema
from tap_linear.schemas.issues import issuesSchema
from tap_linear.schemas.projects import projectsSchema
from tap_linear.schemas.teams import teamsSchema
from tap_linear.schemas.users import usersSchema
from tap_linear.schemas.labels import labelsSchema


class IssuesStream(LinearStream):

    name = "issues"
    schema = issuesSchema
    primary_keys = ["id"]
    replication_key = "updatedAt"
    query = issuesQuery


class ProjectsStream(LinearStream):

    name = "projects"
    schema = projectsSchema
    primary_keys = ["id"]
    replication_key = "updatedAt"
    query = projectsQuery


class UsersStream(LinearStream):

    name = "users"
    schema = usersSchema
    primary_keys = ["id"]
    replication_key = "updatedAt"
    query = usersQuery


class TeamsStream(LinearStream):

    name = "teams"
    schema = teamsSchema
    primary_keys = ["id"]
    replication_key = "updatedAt"
    query = teamsQuery

    def get_child_context(self, record: dict, context) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "teamId": record["id"]
        }


class CommentsStream(LinearStream):

    name = "comments"
    schema = commentsSchema
    primary_keys = ["id"]
    replication_key = "updatedAt"
    query = commentsQuery

class LabelsStream(LinearStream):

    name = "labels"
    schema = labelsSchema
    primary_keys = ["id"]
    replication_key = "updatedAt"
    query = labelsQuery
    parent_stream_type = TeamsStream
    ignore_parent_replication_key = True

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        labels = resp_json["data"]["team"]["labels"]["nodes"]
        for row in labels:
            yield row

    def get_next_page_token(
        self, response: requests.models.Response, previous_token: Optional[Any]
    ) -> Any:
        """Return the next page token."""
        resp_json = response.json()
        page_info = resp_json["data"]["team"]["labels"]["pageInfo"]
        if page_info["hasNextPage"]:
            return page_info["endCursor"]
        else:
            return None