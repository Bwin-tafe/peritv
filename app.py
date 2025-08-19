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
    
@app.route("/newSchedule", methods = ['POST'])
def createNewSchedule():
    print(request.form.get('category'))
    if request.method == 'POST':
        if request.form.get('category') != "all":
            channel1.scheduleMaker(filterByCategory= request.form.getlist('category'), intermission= int(request.form.get("intermission")),bufferSize= int(request.form.get("buffer")),totalDays=int(request.form.get('days')))
        elif request.form.getlist("author") != ["all"]:
            channel1.scheduleMaker(filterByAuthor= request.form.getlist("author"), intermission= int(request.form.get("intermission")),bufferSize= int(request.form.get("buffer")),totalDays=int(request.form.get('days')))           
        elif request.form.getlist("tag") != []:
            channel1.scheduleMaker(filterByTag= request.form.getlist("tag"), intermission= int(request.form.get("intermission")),bufferSize= int(request.form.get("buffer")),totalDays=int(request.form.get('days')))
        elif request.form.get('category') == "all":
            channel1.scheduleMaker(intermission= int(request.form.get("intermission")),bufferSize= int(request.form.get("buffer")),totalDays=int(request.form.get('days')))
    return redirect("/")

@app.route("/schedule", methods = ['POST'])
def getSchedule():
    toSend= channel1.sendSchedule()
    return toSend

@app.route("/settings")
def settings():
    return render_template('settings.html', tags = channel1.tagList, authors = channel1.authorList)

@app.route("/yownload",methods = ['POST','GET'])
def yownloader():
    if request.method == 'POST':
        id = request.form.get('url')
        category = request.form.get('category')
        idType = request.form.get('mode')
        if idType == 'playlist':
            if request.form.get('series') == 'series':
                channel1.addPlaylistToLibrary(id,category,True)
            else:
                channel1.addPlaylistToLibrary(id,category,False)
        elif idType == 'single':
            channel1.addSingleToLibrary(id,category)
    return render_template('yownload.html')
