import json
import requests
import time

# this api is using virustotal apiv3
# author : @taylanisleyici



def main():
    # IMPORTANT : CHANGE FOLLOWING LINES BEFORE USING
    userId = "VMRay"
    maxIterations = 2 # this is temporary, each iteration takes 16 seconds due to limitations of virustotal api, you can iterate 500 times per day.
    keywords = ["agenttesla", "tesla", "cobalt", "cobaltstrike"]
    restoreSession = False # if you want to continue from where you left, set this to True
    saveSession = False # if you want to save the session, set this to True and it will save the next url to next.txt
    #####################################################

    # api endpoint for virustotal users
    url = "https://www.virustotal.com/api/v3/users/" + userId +  "/comments?limit=40" # 2147483647 is max limit of int32 so it is for comments.

    if restoreSession:
        with open("next.txt", "r") as file:
            newUrl = file.read()
        if newUrl:
            url = newUrl
        else:
            print("next.txt is empty, starting a new filtering session")
            restoreSession = False

    # read api key from file
    with open("SECRET", "r") as file:
        apiKey = file.read()
    
    # set api key as header
    headers = {"x-apikey": apiKey, "accept": "application/json"}
    
    # avoiding reference errors
    jsonResponse = None
    
    # clear outputs.json
    if not restoreSession:
        with open("outputs.json", "w") as file:
            file.write("")

    # filtering data
    for i in range(maxIterations):
        if i!=0:
            time.sleep(16)
            url = jsonResponse["links"]["next"]
        response = requests.get(url, headers= headers)
        if response.status_code != 200:
            print("Error occured during http request")
            exit(1)
        
        jsonResponse = response.json()
        jsonData = jsonResponse["data"]
        commentsFiltered = []
        for comment in jsonData:
            text = comment["attributes"]["text"].lower()
            if any(keyword.lower() in text for keyword in keywords):
                commentsFiltered.append(comment)

        if commentsFiltered:
            with open("outputs.json", "a") as file:
                json.dump(commentsFiltered, file, indent=4)

        if saveSession:
            with open("next.txt", "w") as file:
                file.write(jsonResponse["links"]["next"])
        

if __name__ == "__main__":
    main()