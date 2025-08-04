from pyyoutube import Client
from vid import vid,scheduledVid
import re,json, random
from datetime import datetime,timedelta


class channel:
    def __init__(self, client,name):
        self.client : Client = client
        self.name = name
        self.library : list[vid] = []
        self.seriesList : list = []
        self.loadLibrary()
        self.schedule : list[scheduledVid] = []
        self.loadSchedule()
      

    def addSingleToLibrary(self, id, category):
        newVid = vid(id,self.client,category)
        self.library.append(newVid)
        self.saveLibrary()
        self.getUniqueSeries()
    
    def addPlaylistToLibrary(self, id, category):
        playlist = self.client.playlistItems.list('contentDetails,snippet',playlist_id=id, max_results=50)
        playlistData = self.client.playlists.list('id,snippet',playlist_id=id,max_results=50)
        series = playlistData.items[0].snippet.title
        for video in playlist.items:   
            vidId = video.contentDetails.videoId
            episode = int(video.snippet.position) + 1
            newvid = vid(vidId,self.client,category,series=series,episode=episode)
            self.library.append(newvid)
        self.getUniqueSeries()
        self.saveLibrary()

    
    def saveLibrary(self):
        toDump = {
            'library':[],
            'seriesList' : self.seriesList
            }
        for x in self.library:
            toDump['library'].append(x.__dict__)
        with open('settings/library.json','w+') as fout:
            json.dump(toDump,fout)
    
    def loadLibrary(self):
        self.library = []
        with open('settings/library.json','r') as fout:
            list = json.load(fout)
            if list['library'] != []:
                for x in list['library']:
                    vidToLoad = vid(
                        x['id'],
                        self.client,
                        x['category'],
                        author= x['author'],
                        title= x['title'],
                        description= x['description'],
                        duration= float(x['duration']),
                        thumbnailUrl= x['thumbnail'],
                        tags= x['tags'],
                        series= x['series'],
                        episode= x['episode']
                    )
                    self.library.append(vidToLoad)
                self.seriesList = list['seriesList']
    
    def getUniqueSeries(self):
        self.seriesList =[]
        for x in self.library:
            if x.series not in self.seriesList:
                self.seriesList.append(x.series)


    def createScheduleBySeries(self):
        videoSortedBySeries = []
        for series in self.seriesList:
            videoToBeadded = []
            if series != "none":
                for video in self.library:
                    if video.series == series:
                        videoToBeadded.append(video)
                videoToBeadded.sort(key=lambda x: x.episode)
                videoSortedBySeries.append(videoToBeadded)
        for video in self.library:
            if video.series == "none":
                videoSortedBySeries.append([video])
        random.shuffle(videoSortedBySeries)
        return videoSortedBySeries
        # for block in videoSortedBySeries:
        #     for video in block:
        #         scheduledVidToAdd = scheduledVid(
        #             startTime,
        #             video,
        #             intermission= intermission
        #         )
        #         self.schedule.append(scheduledVidToAdd)
        #         startTime = scheduledVidToAdd.endTime + timedelta(seconds=scheduledVidToAdd.intermission)
    
    def scheduleForPeriod(self, sortedVideos : list[list[vid]], selectionBuffer : int = 1, totalDays : int = 7):
        maxNumber = len(sortedVideos)
        buffer = []
        total = timedelta(days=totalDays).total_seconds()
        completedSchedule : list[vid] = []
        if selectionBuffer >= maxNumber:
            selectionBuffer = maxNumber -1
        
        while total > 0:
            pick = random.randint(0,maxNumber - 1)
            if pick not in buffer:
                for video in sortedVideos[pick]:
                    completedSchedule.append(video)
                    total -= video.duration
                buffer.append(pick)
                if len(buffer) > selectionBuffer:
                    buffer.pop(0)

        return completedSchedule




    def addToSchedule(self,fullListOfVideos : list[scheduledVid], startTime : datetime = datetime.now(),  intermission : float = 0):
            for video in fullListOfVideos:
                scheduledVidToAdd = scheduledVid(
                    startTime,
                    video,
                    intermission= intermission
                )
                self.schedule.append(scheduledVidToAdd)
                startTime = scheduledVidToAdd.endTime + timedelta(seconds=scheduledVidToAdd.intermission)   
            self.saveSchedule() 

    
    def saveSchedule(self):
        toDump =[]
        for x in self.schedule:
            toAdd = {
                'startTime' : x.startTime.strftime('%d/%m/%Y - %H:%M:%S:%f'),
                'video' : x.video.id,
                'intermission' : x.intermission
            }
            toDump.append(toAdd)
        with open(f'settings/{self.name}_schedule.json','w+') as fout:
            json.dump(toDump,fout)    

    def loadSchedule(self):
        self.schedule = []
        with open(f'settings/{self.name}_schedule.json','r') as fout:
            list = json.load(fout)
            for x in list:
                for video in self.library:
                    if video.id == x['video']:
                        vidToLoad = video
                scheduleToLoad = scheduledVid(
                    datetime.strptime(x['startTime'],'%d/%m/%Y - %H:%M:%S:%f'),
                    vidToLoad,
                    intermission= x['intermission']
                )
                self.schedule.append(scheduleToLoad)
    
    def currentVideo(self):
        currentTime = datetime.now()
        for scheduledVid in self.schedule:
            if scheduledVid.startTime < currentTime and scheduledVid.endTime > currentTime:
                timeIn = currentTime - scheduledVid.startTime
                return {'startTime' : int(timeIn.total_seconds()), 'video' : scheduledVid.video.__dict__, 'active' : True}
            elif scheduledVid.startTime > currentTime and previousEndTime < currentTime:
                print("HIT PREVIOUS")
                timeIn = scheduledVid.startTime - currentTime
                return {'startTime' : int(timeIn.total_seconds()*1000), 'video' : scheduledVid.video.__dict__, 'active' : False}
            previousEndTime = scheduledVid.endTime
            
    def scheduleMaker(self,intermission = 10):
        self.schedule =[]
        currentTime = datetime.now()
        seriesBlocks = self.createScheduleBySeries()
        completedList = self.scheduleForPeriod(seriesBlocks)
        self.addToSchedule(completedList,currentTime,intermission= intermission)
    
    def sendSchedule(self):
        schedule = self.schedule
        currentTime = datetime.now()
        toSend = []
        for scheduledVid in schedule:
            if currentTime > scheduledVid.startTime and currentTime < scheduledVid.endTime:
                toSend.append({'active': True, 'video' : scheduledVid.video.__dict__, 'startTime' : datetime.strftime(scheduledVid.startTime,"%a, %w/%-d - %-I:%M:%S %p"), 'endTime' : scheduledVid.endTime})
            else:
                toSend.append({'active': False, 'video' : scheduledVid.video.__dict__, 'startTime' :  datetime.strftime(scheduledVid.startTime,"%a, %w/%-d - %-I:%M:%S %p"), 'endTime' : scheduledVid.endTime})
        return toSend
                
                    

