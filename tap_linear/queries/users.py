usersQuery = """
        query Users($next: String, $replicationKeyValue: DateTimeOrDuration) {
						users(
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
								active
								admin
                                archivedAt
                                avatarUrl
                                calendarHash
								createdAt
                                createdIssueCount
								description
                                disableReason
								displayName
                                inviteHash
                                isMe
								email
								guest
								lastSeen
								organization {
									id
									name
								}
								statusLabel
								timezone
								updatedAt
								url
                                statusEmoji
                                statusUntilAt
							}
						}
					}
        """
