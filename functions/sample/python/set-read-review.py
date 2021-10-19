#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

QUERY_FIELDS = ["id", "car_make", "car_model", "car_year", 
                "dealership", "name", "purchase", "purchase_date", 
                "review"]
    
def query_by_id(id):
    return {"selector": {"id": {"$eq": int(id)}}, 
        "fields": QUERY_FIELDS}  
 

def query_by_dealership(dealer_id):
    return { 
        "selector": {"dealership": {"$eq": int(dealer_id)}}, 
        "fields": QUERY_FIELDS}

def query_all():
    return { 
        "selector": {"id": {"$gte": 0}}, 
        "fields": QUERY_FIELDS}    

   
def main(params):
    if ("DEALER" in params):
        return {"query": query_by_dealership(params["DEALER"]), "include_docs":True};
    elif ("ID" in params):
        return {"query": query_by_id(params["ID"]), "include_docs":True};
    else:
        return {"query": query_all(), "include_docs":True};
