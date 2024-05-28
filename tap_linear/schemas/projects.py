from singer_sdk import typing as th

projectsSchema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property(
        "projectMilestones",
        th.ObjectType(
            th.Property(
                "nodes",
                th.ArrayType(
                    th.ObjectType(
                        th.Property("id", th.StringType),
                        th.Property("name", th.StringType),
                    )
                ),
            )
        ),
    ),
    th.Property("url", th.StringType),
    th.Property("progress", th.NumberType),
    th.Property("startedAt", th.DateTimeType),
    th.Property("startDate", th.DateTimeType),
    th.Property("createdAt", th.DateTimeType),
    th.Property("updatedAt", th.DateTimeType),
    th.Property("completedAt", th.DateTimeType),
    th.Property("canceledAt", th.DateTimeType),
    th.Property("color", th.StringType),
    th.Property("state", th.StringType),
    th.Property(
        "creator",
        th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("email", th.StringType),
        ),
    ),
    th.Property(
        "lead",
        th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("email", th.StringType),
        ),
    ),
).to_dict()
