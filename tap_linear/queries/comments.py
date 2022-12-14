commentsQuery = """
        query Comments($next: String, $replicationKeyValue: DateTime) {
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
