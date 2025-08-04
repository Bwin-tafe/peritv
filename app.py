from flask import Flask, request,redirect,url_for,render_template
from channel import channel
from vid import vid,scheduledVid
from pyyoutube import Client

app = Flask(__name__)
client = Client(api_key="AIzaSyDmM_aj7-NDhG1L_hWVD9ZUgr_Stn5mdls")
channel1 = channel(client,"The Big Boy")

@app.route("/")
def hello_world():
    return render_template('channel.html')

@app.route("/currentVid", methods = ['POST'])
def getCurrentVideo():
    if request.method == 'POST':
        print("Current Video Requested")
        sendBack =channel1.currentVideo()
        return sendBack
    
@app.route("/error", methods = ['POST'])
def onError():
    if request.method == 'POST':
        print("Playback Error")
        sendBack =channel1.currentVideo()
        url = {'url': "https://www.youtube.com/watch?v=" + sendBack['video']['id'] + F"&t={sendBack['startTime']}"}
        print(url)
        return url
    
@app.route("/newSchedule")
def createNewSchedule():
    channel1.scheduleMaker(intermission= 10)
    return redirect("/")

@app.route("/schedule", methods = ['POST'])
def getSchedule():
    toSend= channel1.sendSchedule()
    return toSend

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/yownload",methods = ['POST','GET'])
def yownloader():
    if request.method == 'POST':
        id = request.form.get('url')
        category = request.form.get('category')
        idType = request.form.get('mode')
        if idType == 'playlist':
            channel1.addPlaylistToLibrary(id,category)
        elif idType == 'single':
            channel1.addSingleToLibrary(id,category)
    return render_template('yownload.html')
