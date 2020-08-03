from flask import Flask, jsonify
from DeployableModel import getPredictions
app = Flask(__name__)
@app.route('/')
def home():
	return """
	<a href="https://heroku-app-us-admissions.herokuapp.com/">Home</a>
	<h1>Hello<h1>
	<h1> Please use the following format to get the data<h1>
	<h1> https://heroku-app-us-admissions.herokuapp.com/api/&lt;GRE&gt;/&lt;GPA&gt;/&lt;RANK&gt; <h1>
	<h1> In place of &lt;GRE&gt; enter something like 500 and so on in each of the 3 values within range<h1>
	<h1> Allowed Range<h1>
	<h1> 0<=GRE<=800 <h1>
	<h1> 0<=GPA<=4 <h1>
	<h1> 1<=RANK<=4 <h1>
	<h1> Eg. type <a href="https://heroku-app-us-admissions.herokuapp.com/api/500/3/2">"https://heroku-app-us-admissions.herokuapp.com/api/500/3/2"</a> in url box or click to see this example.<h1>
	<h1> If return value 0 then not admitted else if 1 then admitted<h1>
	
	"""
@app.route('/api/<int:gre>/<gpa>/<int:rank>',methods=['GET'])
def test(gre,gpa,rank):
	print(gre,gpa,rank)
	return jsonify(getPredictions(gre=gre,gpa=gpa,rank=rank))

# driver function
if __name__ == '__main__':
	app.run(debug=False)