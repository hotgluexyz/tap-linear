from singer_sdk import typing as th

commentsSchema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("url", th.StringType),
    th.Property("bodyData", th.StringType),
    th.Property("createdAt", th.DateTimeType),
    th.Property("updatedAt", th.DateTimeType),
    th.Property("resolvedAt", th.DateTimeType),
    th.Property("body", th.StringType),
    th.Property("bodyData", th.StringType),
    th.Property("quotedText", th.StringType),
    th.Property("summaryText", th.StringType),
    th.Property(
        "reactionData",
        th.ArrayType(
            th.ObjectType(
                th.Property("emoji", th.StringType),
                th.Property(
                    "reactions",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType),
                            th.Property("reactedAt", th.DateTimeType),
                            th.Property("userId", th.StringType),
                        )
                    ),
                ),
            )
        ),
    ),
    th.Property(
        "issue",
        th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("title", th.StringType),
        ),
    ),
    th.Property("editedAt", th.DateTimeType),
    th.Property("children", th.CustomType({"type": ["object", "string"]})),
).to_dict()
