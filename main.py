import json
import requests
import time

# this api is using virustotal apiv3
# author : @taylanisleyici



def main():
    # IMPORTANT : CHANGE FOLLOWING TWO LINES BEFORE USING
    userId = "VMRay"
    max_iterations = 2 # this is temporary, each iteration takes 16 seconds due to limitations of virustotal api, you can iterate 500 times per day.
    keywords = ["agenttesla", "tesla", "cobalt", "cobaltstrike"]
    #####################################################

    # api endpoint for virustotal users
    url = "https://www.virustotal.com/api/v3/users/" + userId +  "/comments?limit=40" # 2147483647 is max limit of int32 so it is for comments.

    # read api key from file
    with open("SECRET", "r") as file:
        api_key = file.read()
    
    # set api key as header
    headers = {"x-apikey": api_key, "accept": "application/json"}
    
    # avoiding reference errors
    json_response = None
    
    # clear outputs.json
    with open("outputs.json", "w") as file:
        file.write("")

    # filtering data
    for i in range(max_iterations):
        if i!=0:
            time.sleep(16)
            url = json_response["links"]["next"]
        response = requests.get(url, headers= headers)
        if response.status_code != 200:
            print("Error occured during http request")
            exit(1)
        
        json_response = response.json()
        json_data = json_response["data"]
        comments_filtered = []
        for comment in json_data:
            text = comment["attributes"]["text"].lower()
            if any(keyword.lower() in text for keyword in keywords):
                comments_filtered.append(comment)

        with open("outputs.json", "a") as file:
            json.dump(comments_filtered, file, indent=4)

        

if __name__ == "__main__":
    main()