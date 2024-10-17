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
								createdAt
								updatedAt
								archivedAt
								body
								resolvedAt
								editedAt
								bodyData
								quotedText
								summaryText
								reactionData
								url
								issue {
									id
									title
								}
								user {
									avatarUrl
									avatarBackgroundColor
									displayName
									email
									id
									name
									url
								}
							}
						}
					}
        """
