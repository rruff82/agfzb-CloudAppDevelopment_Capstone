/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const QUERY_FIELDS = [
    "id", "address", "city", "full_name", "lat", "long", "short_name", "st", "zip"
]

function query_by_state(st) {
    return {
        "selector": {
            "st": {
                "$eq": st
            }
        },
        "fields": QUERY_FIELDS,

    }
}

function query_by_id(id) {
    return {
        "selector": {
            "id": {
                "$eq": parseInt(id)
            }
        },
        "fields": QUERY_FIELDS,
    }
}

function query_all() {
    return {
        "selector": {
            "id": {
                "$gte": 0
            }
        },
        "fields": QUERY_FIELDS,
    }
}

function main(params) {

    if ("STATE" in params)
        return { "query": query_by_state(params.STATE), "include_docs": true };
    if ("ID" in params)
        return { "query": query_by_id(params.ID), "include_docs": true };
    return { "query": query_all(), "include_docs": true };
}
