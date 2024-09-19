from singer_sdk import typing as th

labelsSchema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("description", th.StringType),
    th.Property("color", th.StringType),
    th.Property("createdAt", th.DateTimeType),
    th.Property("updatedAt", th.DateTimeType),
    th.Property("archivedAt", th.DateTimeType),
).to_dict()