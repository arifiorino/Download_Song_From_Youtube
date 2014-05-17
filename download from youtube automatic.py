from urllib import request
import os, glob, subprocess, sys, glob, shutil

def returnlink(songname):
    html=request.urlopen("http://www.youtube.com/results?search_query="+request.quote(songname)+"&sm=3")
    html = str(html.read())
    link="__url__"
    while link=="__url__" or link[:6]=="/user/":
        html=html[html.find(r"yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"):]
        html=html[html.find("href=\"")+len("href=\""):]
        link=html[:html.find("\"")]
        name=html[html.find(">")+1:html.find("</a>")]
    return [link, name]
def amountof(string, findd):
	x=0
	string=string[string.find(findd)+1:]
	y=string.find(findd)
	while y!=-1:
		x+=1
		string=string[string.find(findd)+1:]
		y=string.find(findd)
	if x==0:
		return 0
	else:
		return x+1
i=input("song: ")
links=[]
while i!="":
    links.append(returnlink(i))
    i=input("song: ")
for k in links:
    subprocess.call("youtube-dl.exe www.youtube.com"+k[0]+" -l")#+" -o '"+k[1]+"'")

for k in glob.glob(os.path.dirname(sys.argv[0])+"/*.mp4"):
    subprocess.call("ffmpeg -i \""+ k +"\" -vcodec mpeg1video -af volume=2 -acodec libmp3lame -intra \""+ k.rsplit( ".", 1 )[ 0 ]+".mp3\"")

for k in glob.glob(os.path.dirname(sys.argv[0])+"/*.mp3"):
    if amountof(k, "-")>=2:
        taggs=[]
        filenameb=os.path.basename(k)
        author=filenameb[:filenameb.find("-")]
        title=filenameb[filenameb.find("-")+1:]
        print(title)
        title=title[:title.find("-")]
        s='id3 -t "'+title.lstrip().rstrip()+'" -a "'+author.lstrip().rstrip()+'"  "'+k+'"'
        subprocess.call(s)
        print(filenameb.find("-"), s)
for i in glob.glob(os.path.dirname(sys.argv[0])+"/*.mp4"):
    os.remove(i)

if not os.path.exists(os.path.dirname(sys.argv[0])+"/Finished"):
    os.makedirs(os.path.dirname(sys.argv[0])+"/Finished")

for i in glob.glob(os.path.dirname(sys.argv[0])+"/*.mp3"):
    shutil.move(i, i[:i.rfind('\\')]+"\\Finished"+i[i.rfind('\\'):])

