import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
load_dotenv()

WATSON_NLU_API_URL = os.environ["NATURAL_LANGUAGE_UNDERSTANDING_URL"]
WATSON_NLU_API_KEY = os.environ["NATURAL_LANGUAGE_UNDERSTANDING_APIKEY"]

def get_request(url, api_key=None,**kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=kwargs, 
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey',api_key))
        else:
            response = requests.get(url, params=kwargs, 
              headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url+"/dealership")
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url+"/dealership",ID=str(dealerId))
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        print("Dealer list: {}\n".format(dealers))
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            return dealer_obj
    return None


def get_dealer_reviews_from_cf(url,dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url+"/review",DEALER=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["docs"]
        # For each dealer object
        for review_doc in reviews:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                dealership = review_doc["dealership"],
                name=review_doc["name"],
                purchase = review_doc["purchase"],
                review = review_doc["review"],
                purchase_date = review_doc["purchase_date"],
                car_make = review_doc["car_make"],
                car_model = review_doc["car_model"],
                car_year = review_doc["car_year"],
                sentiment = analyze_review_sentiments(review_doc["review"]),
                id = review_doc["id"])
            results.append(review_obj)

    return results

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    result = get_request(WATSON_NLU_API_URL+"/v1/analyze", 
        version="2021-08-01",
        api_key=WATSON_NLU_API_KEY,
        text=dealerreview,
        features={
			"sentiment": True,
		},
        return_analyzed_text=True)
    print(result)
    print("My label: {}\n".format(result["sentiment"]["document"]["label"]))
    return result["sentiment"]["document"]["label"]

