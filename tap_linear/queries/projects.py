projectsQuery = """
        query Projects($next: String, $replicationKeyValue: DateTimeOrDuration) {
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
                                projectMilestones{
                                    nodes{
                                        name
                                        id
                                    }
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
