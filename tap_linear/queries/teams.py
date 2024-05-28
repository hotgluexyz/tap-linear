teamsQuery = """
    query Teams($next: String, $replicationKeyValue: DateTimeOrDuration) {
						teams(
							first: 100
							after: $next
							filter: { updatedAt: {gt: $replicationKeyValue } }
						) {
							pageInfo {
								hasNextPage
								endCursor
							}
							nodes {
                                id
                                name
                                color
                                createdAt
                                archivedAt
                                updatedAt
                                cycleCalenderUrl
                                cycleDuration
                                cycleIssueAutoAssignCompleted
                                cycleIssueAutoAssignStarted
                                cycleCooldownTime
                                autoClosePeriod
                                autoCloseStateId                         
                            }
						}
					}


"""
