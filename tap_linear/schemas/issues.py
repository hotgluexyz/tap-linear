from singer_sdk import typing as th

issuesSchema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("title", th.StringType),
    th.Property("url", th.StringType),
    th.Property("updatedAt", th.DateTimeType),
    th.Property(
        "creator",
        th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("email", th.StringType),
        ),
    ),
    th.Property(
        "assignee",
        th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("email", th.StringType),
        ),
    ),
    th.Property(
        "project",
        th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
        ),
    ),
    th.Property(
        "team",
        th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
        ),
    ),
    th.Property("number", th.IntegerType),
    th.Property("priority", th.IntegerType),
    th.Property("estimate", th.NumberType),
    th.Property("createdAt", th.DateTimeType),
    th.Property("boardOrder", th.IntegerType),
    th.Property("startedAt", th.DateTimeType),
    th.Property("completedAt", th.DateTimeType),
    th.Property("startedTriageAt", th.DateTimeType),
    th.Property("triagedAt", th.DateTimeType),
    th.Property("canceledAt", th.DateTimeType),
    th.Property("autoClosedAt", th.DateTimeType),
    th.Property("autoArchivedAt", th.DateTimeType),
    th.Property("dueDate", th.DateTimeType),
    th.Property("slaStartedAt", th.DateTimeType),
    th.Property("slaBreachesAt", th.DateTimeType),
    th.Property("trashed", th.BooleanType),
    th.Property("snoozedUntilAt", th.DateTimeType),
    th.Property("labelIds", th.CustomType({"type": ["array", "string"]})),
    th.Property("state", th.CustomType({"type": ["object", "string"]})),
    th.Property("cycle", th.CustomType({"type": ["object", "string"]})),
    th.Property("project", th.CustomType({"type": ["object", "string"]})),
).to_dict()
