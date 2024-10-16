issuesQuery = """
        query Issues($next: String, $replicationKeyValue: DateTimeOrDuration) {
						issues(
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
								title
								description
								url
								updatedAt
								number
								priority
								estimate
								createdAt
								boardOrder
								branchName
								startedAt
								completedAt
								startedTriageAt
								triagedAt
								canceledAt
								autoClosedAt
								autoArchivedAt
								dueDate
								slaStartedAt
								slaBreachesAt
								trashed
								snoozedUntilAt
								labelIds
								state {
									id
									createdAt
									updatedAt
									archivedAt
									name
									description
									position
									type
								}
								cycle {
									id
									number
									name
								}
								project {
									id
									name
									slugId
								}
								creator {
									id
									name
									email
								}
								assignee {
									id
									name
									email
								}
								project {
									id
									name
								}
								team {
									id
									name
								}
							}
						}
					}
        """
