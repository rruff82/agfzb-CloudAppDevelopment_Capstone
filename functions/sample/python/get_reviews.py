#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result
import requests


def format_result(r):
    return {
        "id": r["doc"]["id"],
        "car_make":  r["doc"]["car_make"],
        "car_model":  r["doc"]["car_model"],
        "car_year":  r["doc"]["car_year"],
        "dealership":  r["doc"]["dealership"],
        "name":  r["doc"]["name"],
        "purchase":  r["doc"]["purchase"],
        "purchase_date":  r["doc"]["purchase_date"],
        "review":  r["doc"]["review"]
    }

def main(dict):
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            None,
            api_key=dict["IAM_API_KEY"],
            url=dict["COUCH_URL"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    review_db = client["reviews"]
    result_collection = Result(review_db.all_docs, include_docs=True)
    search_results = list(filter(lambda x: x["doc"]["dealership"]==dict["DEALERSHIP"],result_collection))
    
    return {"reviews": list(map(format_result,search_results))}
