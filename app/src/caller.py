import requests
import json

def call_ES(question,index,publish_time,topk):

	url = f"http://vespa.lsi.uned.es:9000/elastic-search/{index}/_search"

	body = {
		"query":
		{
			"bool":
			{
				"must":
				{
					"multi_match":
					{
					"query":question,
					"fields":["body","abstract"]
					}
				},
				"filter":{
					"range":{
						"publish_time":{
							"gte":f"now-{publish_time}"
						}
					}
				}
			}
		}
	}

	headers = {
    	'Content-Type': 'application/json',
	}

	params = (
		('size', topk),
	)
	
	# response = requests.post(url,data=body, headers={ "Content-Type": "application/json" })
	response = requests.post(url, headers=headers, params=params, data=json.dumps(body))

	contexts = [
		{
			"id":hit["_source"]["cord_uid"],
			"text":hit["_source"]["body"],
			"score":hit["_score"]
		} 
		for hit in response.json()["hits"]["hits"]
	]

	return contexts

def call_Rerank(question,contexts,qa_cut):
	url = f"http://vespa.lsi.uned.es:9000/vigicovid-rerank-module/rerank"

	body = [{
		"question":question,
		"contexts":contexts
	}]

	headers = {
    	'Content-Type': 'application/json',
	}
	
	response = requests.post(url, headers=headers, data=json.dumps(body))

	return response.json()

# question = "What type of complications related to COVID-19 are associated with hypertension?"
# contexts = call_ES(question,"paragraphs","6M/M",2)
# print(json.dumps(call_QA(question,contexts,2),indent=3))