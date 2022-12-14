"""Stream type classes for tap-linear."""
from tap_linear.client import LinearStream
from tap_linear.queries.comments import commentsQuery
from tap_linear.queries.issues import issuesQuery
from tap_linear.queries.projects import projectsQuery
from tap_linear.queries.teams import teamsQuery
from tap_linear.queries.users import usersQuery
from tap_linear.schemas.comments import commentsSchema
from tap_linear.schemas.issues import issuesSchema
from tap_linear.schemas.projects import projectsSchema
from tap_linear.schemas.teams import teamsSchema
from tap_linear.schemas.users import usersSchema


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


class CommentsStream(LinearStream):

    name = "comments"
    schema = commentsSchema
    primary_keys = ["id"]
    replication_key = "updatedAt"
    query = commentsQuery
