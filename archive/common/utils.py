
def limit_api_results(query, limit=None):
    if limit is None:
        return query

    return query.limit(limit)
