from flask import Flask, jsonify
from DeployableModel import getPredictions
app = Flask(__name__)
@app.route('/')
def home():
	return """
	<a href="https://heroku-app-us-admissions.herokuapp.com/">Home</a>
	<h1>Hello<h1>
	<h4> Please use the following format to get the data<h4>
	<h6> https://heroku-app-us-admissions.herokuapp.com/api/<GRE>/<GPA>/<RANK><h6>
	<h6> In place of <GRE> enter something like 500 and so on in each of the 3 values within range<h6>
	<h6> 0<=GRE<=800 <h6>
	<h6> 0<=GPA<=4 <h6>
	<h6> 1<=RANK<=4 <h6>
	<h6> Eg. type "https://heroku-app-us-admissions.herokuapp.com/api/500/3/2" this in url <h6>
	<h6> If return value 0 then not admitted else if 1 then admitted<h6>
	
	"""
@app.route('/api/<int:gre>/<gpa>/<int:rank>',methods=['GET'])
def test(gre,gpa,rank):
	print(gre,gpa,rank)
	return jsonify(getPredictions(gre=gre,gpa=gpa,rank=rank))

# driver function
if __name__ == '__main__':
	app.run(debug=False)