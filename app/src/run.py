import os, sys, json, requests
from collections import defaultdict

import hydra
from omegaconf import DictConfig, OmegaConf, open_dict
from gevent.pywsgi import WSGIServer

import utils, caller

# Make this the current work dir
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

from flask import Flask, current_app, request, jsonify
app = Flask(__name__)

@app.route('/answer-rerank',methods=['POST'])
def answer():
	"""
		1 - Call ES
		2 - Convert ES format to QA request body
		3 - return with QA call
	"""
	app.logger.info("New request")
	request_body = request.get_json()
	app.logger.info(json.dumps(request_body,indent=3))
	question, index, publish_time, topk, qa_cut = utils.get_data(request_body)

	app.logger.info("Retrieving contexts from ES")
	contexts = caller.call_ES(question,index,publish_time,topk)

	app.logger.info("Reading...")
	response = caller.call_Rerank(question,contexts,qa_cut)

	app.logger.info("Done!")
	return response


@hydra.main(config_path="../conf", config_name="api")
def main(cfg: DictConfig):
	app.logger.info("CFG:")
	app.logger.info("%s", OmegaConf.to_yaml(cfg))
	
	app.config.from_mapping(cfg.flask)


	app.config["config"] = cfg
	if cfg.flask.ENV == 'production':
		http_server = WSGIServer((cfg.server.host, cfg.server.port), app) 	
		http_server.serve_forever()   
	# debug mode
	else:
		app.run(host=cfg.server.host, port=cfg.server.port)
	 


if __name__ == "__main__":
	main()
