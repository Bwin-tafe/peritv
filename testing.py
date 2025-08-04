from pyyoutube import Client, Api
from vid import vid
from channel import channel

client = Client(api_key="AIzaSyDmM_aj7-NDhG1L_hWVD9ZUgr_Stn5mdls")
playlist_id='PLENRDRBm-Rgy8-lzxbCqqpSJo_-iVlkOu'

channel1 = channel(client,"The Big Boy")
# channel1.addSingleToLibrary("Ke-6WW-xGic")
channel1.addPlaylistToLibrary(playlist_id,"stream")

# channel1.getUniqueSeries()
# channel1.saveLibrary()

# channel1.loadLibrary()
# channel1.getUniqueSeries()
# for x in channel1.library:
#     print(x)

print(channel1.__dict__['library'][0].__dict__)
print(channel1.seriesList)

# test = channel1.createScheduleBySeries()

# again = channel1.scheduleForPeriod(test,selectionBuffer=1)

# channel1.addToSchedule(again)
channel1.saveLibrary()

# channel1.loadSchedule()
# for x in channel1.schedule:
#     print(x)




# channel1.saveSchedule()

# bingus = vid('PCmnYlsfi28',client, duration=12)
# bongus = client.playlistItems.list('contentDetails,snippet',playlist_id='PLENRDRBm-RgzWvIHFyslEveetmdxvrF2k')

# print(bingus.duration)
# print(bongus.items[0].contentDetails.videoId)

# # test = client.videos.list(video_id='PCmnYlsfi28')
# # print(test.items[0].snippet.channelTitle)
# # print(test.items[0].snippet.title)
# # print(test.items[0].snippet.description)
# # duration = test.items[0].contentDetails.duration
# # splitDur = re.findall(r'\d+',duration)
# # print(splitDur)
# # print(test.items[0].snippet.thumbnails.maxres.url)
# # print(test.items[0].snippet.tags)