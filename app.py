from flask import Flask, jsonify, request, redirect, url_for, render_template

import Database
from DeployableModel import getPredictions

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == "POST":
		recv_gre = request.form['gre']
		recv_gpa = request.form['gpa']
		recv_rank = request.form['rank']
		try:
			return redirect(url_for('test', gre=recv_gre, gpa=recv_gpa, rank=recv_rank))
		except Exception:
			return jsonify("ERROR")
	return render_template("home.html")


@app.route('/api/<int:gre>/<gpa>/<int:rank>', methods=['GET'])
def test(gre, gpa, rank):
	if not gpa.isnumeric():
		return jsonify("ERROR")
	if not 0 <= gre <= 800:
		return jsonify("ERROR")
	gpa = float(gpa)
	if not 0 <= gpa <= 4:
		return jsonify("ERROR")
	if not 1 <= rank <= 4:
		return jsonify("ERROR")
	result = getPredictions(gre=gre, gpa=gpa, rank=rank)
	Database.insertData(gre=gre, gpa=gpa, student_rank=rank, admit=result)
	return jsonify(result)


@app.route('/api', methods=['POST'])
def postAPI():
	recv_data = request.get_json()
	try:
		gre = int(recv_data['gre'])
		gpa = float(recv_data['gpa'])
		rank = int(recv_data['rank'])
	except Exception:
		return jsonify("ERROR")
	if not 0 <= gre <= 800:
		return jsonify("ERROR")
	if not 0 <= gpa <= 4:
		return jsonify("ERROR")
	if not 1 <= rank <= 4:
		return jsonify("ERROR")
	result = getPredictions(gre=gre, gpa=gpa, rank=rank)
	Database.insertData(gre=gre, gpa=gpa, student_rank=rank, admit=result)
	studentID = Database.getRecentID()
	return jsonify(StudentID=studentID, Prediction=result)


@app.route('/api', methods=['PUT'])
def putAPI():
	hasKeys = {'gre': True, 'gpa': True, 'rank': True}
	recv_data: dict = request.get_json()
	updateCount = 0
	try:
		id = int(recv_data['id'])
	except Exception as e:
		return jsonify("ERROR")

	try:
		gre = int(recv_data['gre'])
	except KeyError:
		hasKeys['gre'] = False
	except ValueError:
		return jsonify("ERROR")
	except Exception as e:
		return jsonify("ERROR")

	try:
		gpa = float(recv_data['gpa'])
	except KeyError:
		hasKeys['gpa'] = False
	except ValueError:
		return jsonify("ERROR")
	except Exception as e:
		return jsonify("ERROR")

	try:
		rank = int(recv_data['rank'])
	except KeyError:
		hasKeys['rank'] = False
	except ValueError:
		return jsonify("ERROR")
	except Exception as e:
		return jsonify("ERROR")

	if hasKeys['gre']:
		if not 0 <= gre <= 800:
			return jsonify("ERROR")

	if hasKeys['gpa']:
		if not 0 <= gpa <= 4:
			return jsonify("ERROR")

	if hasKeys['rank']:
		if not 1 <= rank <= 4:
			return jsonify("ERROR")

	for key in list(recv_data.keys()):
		if key == 'gre':
			try:
				updateCount += Database.updategre(gre=gre, id=id)
			except Exception:
				return jsonify("ERROR")
		if key == 'gpa':
			try:
				updateCount += Database.updateGPA(gpa=gpa, id=id)
			except Exception:
				return jsonify("ERROR")
		if key == 'rank':
			try:
				updateCount += Database.updaterank(rank=rank, id=id)
			except Exception:
				return jsonify("ERROR")
	if True not in hasKeys.values():
		return jsonify("ERROR")
	studentID = id
	if list(hasKeys.values()).count(True) == updateCount:
		return jsonify(StudentID=studentID, Sucessfull=True)
	else:
		return jsonify("ERROR")


@app.route('/api', methods=['DELETE'])
def deleteAPI():
	recv_data: dict = request.get_json()
	try:
		id = int(recv_data['id'])
	except Exception:
		return jsonify("ERROR")

	studentID = id
	updateCount = Database.deleteData(id=studentID)
	if updateCount != 0:
		return jsonify(StudentID=studentID, Sucessfull=True)
	else:
		return jsonify("ERROR")


# driver function
if __name__ == '__main__':
	app.run(debug=True)
