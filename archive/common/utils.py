
def limit_query(query, limit=None):
    if limit is None:
        return query

    return query.limit(limit)
