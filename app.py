from flask import Flask, request,redirect,url_for,render_template, jsonify
from channel import channel
from vid import vid,scheduledVid
from pyyoutube import Client

app = Flask(__name__)
client = Client(api_key="AIzaSyDmM_aj7-NDhG1L_hWVD9ZUgr_Stn5mdls")
channel1 = channel(client,"The Big Boy")


if __name__ == "__main__":
    app.run(debug=True)

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
        if sendBack['active'] == True:
            url = {'url': "https://www.youtube.com/watch?v=" + sendBack['video']['id'] + F"&t={sendBack['startTime']}"}
        elif sendBack['active'] == False:
            url = {'url': "https://www.youtube.com/watch?v=" + sendBack['video']['id']}

        print(url)
        return url
    
@app.route("/newSchedule", methods = ['POST'])
def createNewSchedule():
    print(request.form.get('category'))
    print(request.form.getlist("tag"))
    print(request.form.getlist("author"))
    if request.method == 'POST':
        # if request.form.get('category') != "all":
            channel1.scheduleMaker(filterByCategory= request.form.getlist('category'),filterByAuthor= request.form.getlist("author"), filterByTag= request.form.getlist("tag"), intermission= int(request.form.get("intermission")),bufferSize= int(request.form.get("buffer")),totalDays=int(request.form.get('days')))
        # elif request.form.getlist("author") != ["all"]:
        #     channel1.scheduleMaker(filterByAuthor= request.form.getlist("author"), intermission= int(request.form.get("intermission")),bufferSize= int(request.form.get("buffer")),totalDays=int(request.form.get('days')))           
        # elif request.form.getlist("tag") != []:
        #     channel1.scheduleMaker(filterByTag= request.form.getlist("tag"), intermission= int(request.form.get("intermission")),bufferSize= int(request.form.get("buffer")),totalDays=int(request.form.get('days')))
        # elif request.form.get('category') == "all":
        #     channel1.scheduleMaker(intermission= int(request.form.get("intermission")),bufferSize= int(request.form.get("buffer")),totalDays=int(request.form.get('days')))
    return redirect("/")

@app.route("/schedule", methods = ['POST'])
def getSchedule():
    toSend= jsonify(channel1.sendSchedule())
    print(toSend)
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
        seriesToAdd= request.form.get('series')
        tagsToAdd= request.form.getlist('tag')
        episodeToAdd = request.form.get('episode')
        if idType == 'playlist':
            if request.form.get('series') == 'series':
                channel1.addPlaylistToLibrary(id,category,True)
            else:
                channel1.addPlaylistToLibrary(id,category,False)
        elif idType == 'single':
            if seriesToAdd != "none":
                channel1.addSingleToLibrary(id,category,series=seriesToAdd,tags=tagsToAdd,episode=episodeToAdd)
            else:
                channel1.addSingleToLibrary(id,category,tags=tagsToAdd)
    return render_template('yownload.html',series= channel1.seriesList, tags= channel1.tagList)

@app.route("/library", methods= ['POST','GET'])
def videdit():
    return render_template('videdit.html', videos = channel1.library, series = channel1.seriesList)

@app.route("/deletevid", methods= ['POST'])
def deleteVid():
    channel1.deleteVid(request.form.get('id'))
    return redirect("/library")

@app.route("/updateVid", methods=['POST'])
def updateVid():
    id = request.form.get("id")
    title = request.form.get("title")
    author = request.form.get("author")
    series = request.form.get("series")
    episode = request.form.get("episode")
    category = request.form.get("category")
    if request.form.get("tags")[0] == "[" and request.form.get("tags")[-1] == "]":
        tags = request.form.get("tags")[1:-1].replace("'","").replace('"',"").split(",")
    else:
        tags = "invalid"
    channel1.editVid(id,title,author,series,episode,category,tags)
    return redirect("/library")
