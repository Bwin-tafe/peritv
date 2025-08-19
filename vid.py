from pyyoutube import Client
from datetime import datetime, timedelta
import re


class vid:
    def __init__(self, id : str, client : Client, category, author : str = "none", title : str = "none", description : str = "none", duration : float = 0, thumbnailUrl : str = "none", tags: list = [], series : str = "none", episode : int = 0):
        self.id = id
        if author == "none" and title == "none" and description == "none" and duration == 0 and thumbnailUrl == "none" and tags == []:
            ytData = client.videos.list(video_id=id)
            self.author = ytData.items[0].snippet.channelTitle
            self.title = ytData.items[0].snippet.title
            self.description = ytData.items[0].snippet.description
            durationList = re.findall(r'\d+',ytData.items[0].contentDetails.duration)
            if len(durationList) == 1:
                self.duration = timedelta(seconds=int(durationList[0])).total_seconds()
            elif len(durationList) == 2:
                self.duration = timedelta(minutes=int(durationList[0]),seconds=int(durationList[1])).total_seconds()
            elif len(durationList) == 3:
                self.duration = timedelta(hours=int(durationList[0]),minutes=int(durationList[1]),seconds=int(durationList[2])).total_seconds()
            if ytData.items[0].snippet.thumbnails.maxres != None:
                self.thumbnail = ytData.items[0].snippet.thumbnails.maxres.url
            else:
                self.thumbnail = None
            # self.tags = ytData.items[0].snippet.tags
            # if self.tags == None:
            self.tags = []
        else:
            self.author = author
            self.title = title
            self.description = description
            self.duration = duration
            self.thumbnail = thumbnailUrl
            self.tags = tags
        self.series = series
        self.episode = episode
        self.category = category
    
    def __str__(self):
        return f"Video Id: {self.id}\nAuthor: {self.author}\nTitle: {self.title}\nDescription: {self.description}\nDuration: {str(self.duration)}\nThumbnail: {self.thumbnail}\nTags: {self.tags}\nSeries: {self.series}\nEpisode: {self.episode}\n"
    
class scheduledVid:
    def __init__(self,startTime,video : vid, intermission = 0):
        self.startTime : datetime = startTime
        self.video= video
        self.endTime : datetime = self.startTime + timedelta(seconds=self.video.duration)
        self.intermission : int = intermission
    
    def __str__(self):
        return f"{self.video.title} to start at {self.startTime}"