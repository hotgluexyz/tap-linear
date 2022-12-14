from singer_sdk import typing as th

teamsSchema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("color", th.StringType),
    th.Property("createdAt", th.DateTimeType),
    th.Property("archiveAt", th.DateTimeType),
    th.Property("updatedAt", th.DateTimeType),
    th.Property("cycleCalenderUrl", th.StringType),
    th.Property("cycleDuration", th.IntegerType),
    th.Property("cycleIssueAutoAssignCompleted", th.BooleanType),
    th.Property("cycleIssueAutoAssignStarted", th.BooleanType),
    th.Property("cycleCooldownTime", th.IntegerType),
    th.Property("autoClosePeriod", th.IntegerType),
    th.Property("autoCloseStateId", th.StringType),
).to_dict()
