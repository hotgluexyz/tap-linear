commentsQuery = """
        query Comments($next: String, $replicationKeyValue: DateTimeOrDuration) {
						comments(
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
                                url
                                bodyData
                                createdAt
                                updatedAt
                                body
                                reactionData
                                editedAt
							}
						}
					}
        """
