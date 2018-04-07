import requests

def BingImage(search_term):
    subscription_key = "5ecd1122df704d5080f7a4639f1aad98"

    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "license": "public", "imageType": "photo"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # print(search_results["value"][:1])
    import os

    content_urls = [img["contentUrl"] for img in search_results["value"][:4]]

    for content in content_urls:
        print(content)
        command = "wget " + content + " --directory-prefix=img/"
        os.system(command)

query = input("Please enter the given search query:")
BingImage(query)