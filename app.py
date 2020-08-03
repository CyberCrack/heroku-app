from flask import Flask, jsonify
from DeployableModel import getPredictions
app = Flask(__name__)
@app.route('/')
def home():
	return "<H1>Hello</H1>"
@app.route('/api/<int:gre>/<gpa>/<int:rank>',methods=['GET'])
def test(gre,gpa,rank):
	print(gre,gpa,rank)
	return jsonify(getPredictions(gre=gre,gpa=gpa,rank=rank))

# driver function
if __name__ == '__main__':
	app.run(debug=False)