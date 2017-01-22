from flask import Flask, render_template, redirect, request, session
import random

# Declare all global values
activity = []
# conter = 0

# Function to return activity string from the dictionary bldgLegend to be placed into the list activity
def getResponse(click, num):

	bldgLegend = {"farm": "Earned " + str(num) + " golds from the farm", "cave": "Earned " + str(num) + " golds from the cave", "house": "Earned " + str(num) + " golds from the house", "casino+": "Entered a casino and won " + str(num) + " golds...Yay!", "casino-" : "Entered a casino and lost " + str(num) + " golds...Ouch!"}

	bldgResponse = bldgLegend[click]

	return bldgResponse

# Function to generate a random number for the game when envoked
def randomGold(click):
	randFarm = random.randrange(9, 21)
	randCave = random.randrange(4, 11)
	randHouse = random.randrange(1, 6)
	randCasino = random.randrange(-51, 51)

	if click == "farm":
		return randFarm
	elif click == "cave":
		return randCave
	elif click == "house":
		return randHouse
	elif click == "casino":
		return randCasino

# Function to determine whether a positive or negative result for casino activity should be generated
def checkCasino(random):
	if random < 0:
		click = "casino-"
		response = getResponse(click, random)
	elif random >= 0:
		click = "casino+"
		response = getResponse(click, random)
	print click, random
	return response

# Function to get the activity string
def getActivity(click, random):
	if click =="casino":
		act = checkCasino(random)
	elif click == "farm":
		act = getResponse(click, random)
	elif click == "cave":
		act = getResponse(click, random)
	elif click == "house":
		act = getResponse(click, random)
	return act

app = Flask(__name__)
app.secret_key = "ThisIsSecret"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/process_money", methods=["POST"])
def process():
	session["activity"] = 0
	click = request.form["building"]
	yourGold = session["yourGold"]
	counter = 0
	if click == "farm":
		random = randomGold(click)
		yourGold += random
		act = getActivity(click, random)
		activity.append(act)
	elif click == "cave":
		random = randomGold(click)
		yourGold += random
		act = getActivity(click, random)
		activity.append(act)
	elif click == "house":
		random = randomGold(click)
		yourGold += random
		act = getActivity(click, random)
		activity.append(act)
	elif click == "casino":
		random = randomGold(click)
		yourGold += random
		act = getActivity(click, random)
		activity.append(act)

	session["yourGold"] = yourGold
	session["activity"] = activity
	session["counter"] = counter
	counter += 1

	return render_template("process_money.html")

@app.route("/reset")
def reset():
	session["yourGold"] = 0
	session["counter"] = 0
	session.pop("activity")

	return redirect("/")

app.run(debug = True)
