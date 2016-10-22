from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def search():
	index = open_dir('guardian_index')
	searcher = index.searcher()
	query_str = request.args.get('query', 'accident')
	query = QueryParser('description', index.schema).parse(query_str.decode('utf-8'))
	results = searcher.search(query, limit = 1000)
	search_results = list()
	for result in results:
		myimgpath = 'guardian_images/%s/%s.jpg' % (result['key'][:4], result['key'][4:])
		search_results.append({'imgpath': myimgpath, \
							   'key': result['key'], \
							   'description': result['description']})
	return render_template('index.html', totalResults = len(results), results = search_results)

