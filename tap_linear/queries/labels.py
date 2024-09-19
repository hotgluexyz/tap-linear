labelsQuery = """
query Labels($teamId: String!, $next: String, $replicationKeyValue: DateTimeOrDuration) {
  team(id: $teamId) {
    labels(
      first: 100
      after: $next
      filter: { updatedAt: { gt: $replicationKeyValue } }
    ) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        id
        name
        description
        color
        createdAt
        updatedAt
        archivedAt
      }
    }
  }
}
"""