from flask import Flask
from flask_restful import Resource, Api, reqparse
from searcher import searchQuery, searchKeyword, trimSearchQuery
from ontology import findChild
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

search_args = reqparse.RequestParser()
search_args.add_argument("data", type=str, required=True)

#API To get list of sub-domain knowledge
class GetOntology(Resource):
    def get(self, query):
        allPossibeKeyword = trimSearchQuery(query.lower()) #Get All sub-domain knowledge keyword
        returnItem = {}
        for keyword in allPossibeKeyword: #build return json
            returnItem[str(keyword)] = findChild(keyword)

        return returnItem

#API to get search result for keyword and selected sub-domain knowledge
class Search(Resource):
    def post(self):
        args=search_args.parse_args() #get search json object
        searchObj = json.loads(args["data"].replace("True", "true").replace("False", "false").replace("\'", "\"")) #destruct search json object
        resultObj = searchQuery(searchObj) #get search result
        #print(resultObj)
        return resultObj

api.add_resource(GetOntology, '/api/getOntology/<string:query>')
api.add_resource(Search, '/api/search/')

if __name__ == '__main__':
    app.run(debug=True)