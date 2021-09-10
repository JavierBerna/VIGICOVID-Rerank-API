def get_data(request_body):
    """
		Extracts main data structures from the request json
	"""
    return  request_body["question"],request_body["context_type"], request_body["publish_time"], request_body["num_contexts"], request_body["num_answers_per_context"]
