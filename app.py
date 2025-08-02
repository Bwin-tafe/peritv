from flask import Flask, request,redirect,url_for,render_template
from channel import channel
from vid import vid,scheduledVid
from pyyoutube import Client

app = Flask(__name__)
client = Client(api_key="AIzaSyDmM_aj7-NDhG1L_hWVD9ZUgr_Stn5mdls")
channel1 = channel(client,"The Big Boy")

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/currentVid", methods = ['POST'])
def getCurrentVideo():
    if request.method == 'POST':
        print("someone saw this!")
        sendBack =channel1.currentVideo()
        print(sendBack)
        print(channel1.schedule)
        return sendBack
    
@app.route("/newSchedule")
def createNewSchedule():
    channel1.scheduleMaker()
    return redirect("/")