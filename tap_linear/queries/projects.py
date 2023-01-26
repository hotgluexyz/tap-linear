projectsQuery = """
        query Projects($next: String, $replicationKeyValue: DateTime) {
						projects(
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
								milestone {
                                    id
                                    name
                                }
								url
								progress
								startedAt
								startDate
								createdAt
								updatedAt
								completedAt
								canceledAt
								color
								state
								creator {
									id
									name
									email
								}
								lead {
									id
									name
									email
								}
							}
						}
					}
        """
