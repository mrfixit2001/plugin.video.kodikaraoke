# MRFIXIT:
# The original source code was pretty messy and had a lot of issues. I reworked and reorganized a lot.
# There is still a bunch of unused code in here, but I left it in case anyone wants to reference it. But I'm pretty sure it won't work anyway.
# The original kodi karaoke used a .COM to authenticate paid services. But that .COM has since been allowed to expire.

# Import required libraries
import urllib,urllib3,re,sys,xbmcplugin,xbmcgui,xbmcaddon,xbmc,xbmcvfs,os,requests,string


# Define all our methods and functions

# NOT USED
#import datetime
#def SYSEXIT():
#    sys.exit()
#    xbmc.executebuiltin("Container.Update(path,replace)")
#    xbmc.executebuiltin("ActivateWindow(Videos)")
#def STRIP(name):
#  return re.sub(r'\[.*?\]|\(.*?\)|\W -', ' ', name).strip()
#def parse_date(dateString):
#    import time
#    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
#def getday():
#    today = datetime.datetime.today()
#    return today.strftime("%A")
#def getYday():
#    from datetime import timedelta
#    today = datetime.datetime.today()-timedelta(hours=24)
#    return today.strftime("%A")


# NOT USED - Only called in sunfly methods
def GRABBER(type,mode,item):
    db = database.connect( db_dir );cur = db.cursor()
    if type == 1:#EXACT MATCH ALL
        item = '%'+item+'%'
        cached = cur.fetchall()
        try: cur.execute('SELECT * FROM tracklist WHERE %s = "%s"' %(mode,item))
        except:pass
    elif type == 2: #EXACT MATCH ONE
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s = "%s"' %(mode,item))
        except:pass
        cached = cur.fetchone()
    elif type == 3:#NEAREST MATCH ONE
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchone()
    elif type == 4:# NEAREST MATCH ALL
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchall()
    elif type == 5:# NEAREST MATCH ALL BY FIRST LETTER
        item = item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchall()
    db.close()
    if cached:
        return cached


# NOT USED
def KaraokeSource(url):
    tagNAME='Kodi Karoke Folder'; tagURL=url;
    path=os.path.join(xbmcvfs.translatePath('special://home'),'userdata','sources.xml')
    if not os.path.exists(path): f=open(path,mode='w'); f.write('<sources><files><source><name>'+tagNAME+'</name><path pathversion="1">'+tagURL+'</path></source></files></sources>'); f.close();
    f=open(path,mode='r'); str=f.read(); f.close()
    if not tagURL in str:
        if '</files>' in str: str=str.replace('</files>','<source><name>'+tagNAME+'</name><path pathversion="1">'+tagURL+'</path></source></files>'); f=open(path,mode='w'); f.write(str); f.close()
        else: str=str.replace('</sources>','<files><source><name>'+tagNAME+'</name><path pathversion="1">'+tagURL+'</path></source></files></sources>'); f=open(path, mode='w'); f.write(str); f.close()


# NOT USED
def ProKaraoke(url):
        try:
            addDir('[COLOR '+newfont+']'+'Search[/COLOR]-[COLOR '+newfont+']'+'K[/COLOR]odi Karaoke','url',5003,art+'Main/Search.png','none',1)
            if ADDON.getSetting('sfenable') == 'true':
                KaraokeSource(sfdownloads)
                addDir('[COLOR '+newfont+']'+'D[/COLOR]ownloads','url',31,art+'Main/favorites.png','',1)
            addDir('[COLOR '+newfont+']'+'Search[/COLOR] By Number','url',25,art+'Main/Search.png','none',1)
            addDir('[COLOR '+newfont+']'+'Browse[/COLOR] Artist','http://www.sunflykaraoke.com/',1,art+'Main/Artist.png','none',23)
            addDir('[COLOR '+newfont+']'+'Browse[/COLOR] Tracks','http://www.sunflykaraoke.com/',1,art+'Main/Title.png','none',24)
            addDir('[COLOR '+newfont+']'+'G[/COLOR]enre','http://www.sunflykaraoke.com/',32,art+'Main/Genre.png','none',1)
            addDir('[COLOR '+newfont+']'+'D[/COLOR]ownload Database / Fix Database','url',103,'','none',1)
        except:
            addDir('[COLOR '+newfont+']'+'F[/COLOR]ix Database','url',103,'','none',1)


# MODE 201: not used
#def download_DB():
#    import downloader
#    dp = xbmcgui.DialogProgress()
#    db_dir = xbmcvfs.translatePath(os.path.join(ADDON.getAddonInfo('path'),'Karaoke.db'))
#    dp.create("Kodi Karaoke","",'Building Database Please Wait', ' ')
#    downloader.download(K_db, db_dir,dp)


# NOT USED
#def Update(s):
#    import downloader
#    dp = xbmcgui.DialogProgress()
#    dp.create("Kodi Karaoke","",'Building Database Please Wait', ' ')
#    downloader.download(K_db, db_dir,s,dp)






def OPEN_URL(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
       response = urllib.request.urlopen(req)
    except:
       print("ERROR: Unable to open requested url: " + url)
       return ""

    try:
       link=response.read().decode(response.headers.get_content_charset('utf8'))
    except:
       print("WARNING: Charset not set for: " + url)
       # If charset is not available, fall back to default for all content
       link=result.decode('utf8')

    response.close()
    return link


# MAIN MENU
def MAINMENU(url):
        addDir('[COLOR '+newfont+']'+'Search[/COLOR]-[COLOR '+newfont+']'+'K[/COLOR]odi Karaoke','url',5003,art+'Main/Search.png','none',1)
        addDir('[COLOR '+newfont+']'+'F[/COLOR]avorites','switch=display',2,art+'Main/favorites.png','none',1)
        addDir('[COLOR '+newfont+']'+'Most[/COLOR] Popular','http://www.sunflykaraoke.com/tracks?dir=asc&limit=200&order=popular',7,art+'AtoZ/P.png','none',1)
        addDir('[COLOR '+newfont+']'+'L[/COLOR]atest','http://www.sunflykaraoke.com/tracks?dir=asc&limit=200&order=latestalbums',7,art+'AtoZ/L.png','none',1)
        addDir('[COLOR '+newfont+']'+'Browse[/COLOR] Artist','https://www.azlyrics.com/%s.html',1,art+'Main/Artist.png','none',4)
        addDir('[COLOR '+newfont+']'+'Browse[/COLOR] Tracks','http://www.sunflykaraoke.com/tracks/search/byletter/letter/%s/',1,art+'Main/Title.png','none',7)
        addDir('[COLOR '+newfont+']'+'G[/COLOR]enre','http://www.sunflykaraoke.com/',8,art+'Main/Genre.png','none',1)


# MODE 1 - used by browse artists (num=4) and tracks (num=7)
def AtoZ(url,number,fanart):
    # "browse by" = includes '%s'
    if '%s' in url:
        addDir('0-9',url%('19' if number==4 else '0-9'),number,"%s/KaraokeArt/AtoZ/%s.png"%(ADDON.getAddonInfo("path"),'0-9'),fanart,1)
    for i in string.ascii_uppercase:
        addDir(i,url%i,number,"%s/KaraokeArt/AtoZ/%s.png"%(ADDON.getAddonInfo("path"),i),fanart,1)


# MODE 2 - adds, removes, and lists favorites
def FAVORITES(switch,name,iconimage,url):
    if 'http' in Kfolder:
        url=url.replace(' ','%20')
        iconimage=iconimage.replace(' ','%20')

    IMAGE = os.path.join(ADDON.getAddonInfo('path'), 'icon.png')

    db = database.connect( db_dir );cur = db.cursor()
    if switch == 'add':
        sql = "INSERT OR REPLACE INTO favourites (track_name,iconimage,url) VALUES(?,?,?)"
        cur.execute(sql, (name,iconimage.replace(Kfolder,''),url.replace(Kfolder,'')))
        db.commit(); db.close()
        xbmc.executebuiltin('Notification('+name+',Added to Favorites,2000,'+IMAGE+')')
        xbmc.executebuiltin("Container.Refresh")
    if switch == 'delete':
        cur.execute("DELETE FROM favourites WHERE track_name='%s'"%name)
        db.commit(); db.close()
        xbmc.executebuiltin('Notification('+name.replace('  ',' ')+',Deleted from Favorites,2000,'+IMAGE+')')
        xbmc.executebuiltin("Container.Refresh")
    if switch == 'display':
        cur.execute("SELECT * FROM favourites")
        cached = cur.fetchall()
        if cached:
            for name,artist,track,iconimage,url in cached:
                #if url[-4]=='.':
                #    addLinkSF(name,url,url.replace('.avi','.jpg'))
                #else:
                addLink(name,url,iconimage,'')
        db.close()


# List of previous search's and new search link
def FirstSearchDir():
    addDir('[COLOR '+newfont+']'+'Search[/COLOR]-Free Karaoke','url',3,art+'Main/Search.png','none',1)

    favs = ADDON.getSetting('favs').split(',')
    for title in favs:
        if len(title)>1:
            addDir(title.title(),title.lower(),3,art+'Main/Search.png','none',1)

    setView('DEFAULT')


def PlayListHandler(url):
        TXT='https://www.youtube.com/watch?v=%s' % (url.replace(' ','+').replace("\\u0026","&"))
        html=OPEN_URL(TXT)
        html=html[html.find('"playlist":{"playlist"'):html.find('"currentIndex"')]

        # NOTE: the current element in the loop contains the title for the NEXT element
        link=html.split('watch?v=')
        for i, p in enumerate(link):
            nextLink = link[(i+1) % len(link)]
            p=p.replace('\\"',"")

            # Get the title from this element
            name = ""
            if '{"title":{"accessibility":{"accessibilityData":{"label":"' in p:
                name = p.split('{"title":{"accessibility":{"accessibilityData":{"label":"')[1]
            name = name.split('"')[0]
            name = str(name).replace("&#39;","'").replace("&amp;","and").replace("&#252;","u").replace("&quot;","").replace("[","").replace("]","").replace("-"," ")

            # Everything else from the next element
            if ':"buy or rent"' in nextLink.lower():
                continue

            url=nextLink.split('"')[0]
            if "\\u0026" in url:
               url=url.split("\\u0026")[0]
            if '&amp' in url:
               url = url.split('&amp')[0]
            iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
            if not 'video_id' in name:
                 if not '_title_' in name:
                    if not 'video search' in name.lower():
                        addLink(name,url,iconimage,'')

        setView('VIDEO')


def HtmlToResults(html):
        link=html.split('watch?v=')

        # NOTE: the current element in the loop contains the title for the NEXT element
        for i, p in enumerate(link):
            nextLink = link[(i+1) % len(link)]
            p=p.replace('\\"',"")

            # Get the title from this element
            name = ""
            if ',"title":{"simpleText":"' in p:
                name = p.split(',"title":{"simpleText":"')[1]
            if ',"title":{"runs":[{"text":"' in p:
                name = p.split(',"title":{"runs":[{"text":"')[1]
            name = name.split('"')[0]
            name = str(name).replace("&#39;","'").replace("&amp;","and").replace("&#252;","u").replace("&quot;","").replace("[","").replace("]","").replace("-"," ")

            # Everything else from the next element
            if ':"buy or rent"' in nextLink.lower():
                continue

            url=nextLink.split('"')[0]
            print("URL:" + url)
            iconimage=""
            if "\\u0026list=" in url:
                # Playlist
                iconimage="DefaultFolder.png"
                addDir(name,url,99,'DefaultFolder.png','none',1)
            else:
              if '&amp' in url:
                  url = url.split('&amp')[0]
              if iconimage=="":
                 iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
              if not 'video_id' in name:
                 if not '_title_' in name:
                    if not 'video search' in name.lower():
                        addLink(name,url,iconimage,'')


def SEARCH(search_entered):
        favs = ADDON.getSetting('favs').split(',')
        if 'url' in search_entered:
            keyboard = xbmc.Keyboard('', 'KODI KARAOKE FREE')
            keyboard.doModal()
            if keyboard.isConfirmed() and len(keyboard.getText())>0:
               search_entered = keyboard.getText()
            else: return False

        search_entered = search_entered.replace(',', '').lower()

        if len(search_entered.replace(' ','')) == 0:
            return False

        TXT='https://www.youtube.com/results?search_query=%s+karaoke&hl=en-GB'  % (search_entered.replace(' ','+'))
        html=OPEN_URL(TXT)
        if not search_entered in favs:
            favs.append(search_entered.lower())
            ADDON.setSetting('favs', ','.join(favs))

        HtmlToResults(html)
        return True


# MODE=4 - list of artists by starting character
def ARTIST_INDEX(url, iconimage, name):
        html=OPEN_URL(url.lower())
        try:
            link=html.split('<div class="container main-page">')[1]
            link=link.split('<nav class="navbar navbar-default navbar-bottom">')[0]
        except:
            link=html
        match = re.compile('<a href="(.+?)">(.+?)</a>').findall(link)
        for url2, mname in match:
            url2 = 'https://www.azlyrics.com/'+url2
            mname = str(mname).replace("lyrics","").replace("\\"," ").replace("+"," ").replace("-"," ").strip()

            if mname.replace(" ","")=="":
                continue

            if not bool(re.match('^[a-zA-Z0-9]+$', mname[0])):
                continue

            if name != "0-9":
                if mname[0].lower() == name.lower():
                    addDir(mname,url2,5,iconimage,art+'Main/Fanart_A.jpg',1)
            else:
                 if not mname[0].isalpha():
                    addDir(mname,url2,5,iconimage,art+'Main/Fanart_A.jpg',1)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

# MODE=5 - list of songs by selected artist
def ARTIST_SONG_INDEX(url, name):
        html=OPEN_URL(url)

        try:
            link=html.split('<div id="listAlbum">')[1]
            link=link.split('<script type="text/javascript">')[0]
        except:
            link=html

        match1 = re.compile('<div class="listalbum-item">.+?">(.+?)</a>').findall(link)

        for mname in match1:
            mname = str(mname).replace("&Agrave;","A").replace('&eacute;','e').replace('&ecirc;','e').replace('&egrave;','e').replace("&agrave;","A")
            addDir(mname,name,6,iconimage,art+'Main/Fanart_A.jpg',1)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)


# Mode 7 - list of songs - used for most popular, lates, and browse tracks
def TRACK_INDEX(url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        match = re.compile('<li><span>.+?href=.+?title="(.+?)">.+?> - <.+?>(.+?)</a>').findall(link)
        uniques = []
        for name, url, in match:
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")
                url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")
                name = name+ '   ('+ url+')'
                if not '</a>' in name:
                    if name not in uniques:
                        uniques.append(name)
                        addDir(name,url,9,iconimage,art+'Main/Fanart_T.jpg',1)


# MODE 8 - List of genres
def GENRE(url):
        link=OPEN_URL(url + 'genre')
        match=re.compile('class="thumb_img">.+?<img src="(.+?)".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
        for iconimage, url, name in match:
            addDir(name,url+'?dir=asc&limit=500',10,iconimage,art+'Main/Fanart_G.jpg',1)


# MODE 32 - SUNFLY Genre List (NOT USED)
def GENRESF(url):
        link=OPEN_URL('http://www.sunflykaraoke.com/genre')
        match=re.compile('class="thumb_img">.+?<img src="(.+?)".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
        for iconimage,url,name in match:
            addDir(name,url+'?dir=asc&limit=200&order=latestalbums',33,iconimage,art+'Main/Fanart_G.jpg',1)


# MODE 10 - list of songs in the selected genre
def GENRE_INDEX(name, url, iconimage):
        html=OPEN_URL(url.replace(' ','%20'))
        for p in html.split('<div class="track_det"'):
            match = re.compile('<p><a href=".+?">(.+?)<.+?<p class="trkname">.+?href=".+?">(.+?)<.+?</div>',re.DOTALL).findall(p)
            uniques=[]
            for name, url in match:
                name = str(name).replace("&#39;","'").replace("&amp;","and").replace("&#252;","u").replace("&quot;","")
                url = str(url).replace("&#39;","'").replace("&amp;","and").replace("&#252;","u").replace("&quot;","")
                name = name+ '   ('+ url+')'
                if not '</a>' in name:
                    if name not in uniques:
                        uniques.append(name)
                        addDir(name,name,9,iconimage,art+'Main/Fanart_G.jpg',1)


# Mode 33 - SUNFLY list songs in genres (not used)
def GENRE_INDEXSF(name,url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        match = re.compile('<div class="track_det" style="width:80%">.+?<p><a href=".+?">(.+?)<.+?<p class="trkname">.+?href=".+?">(.+?)<',re.DOTALL).findall(link)
        uniques=[]
        for name, url, in match:
            passto = re.sub('[\(\)\{\}<>]', '', name.replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("&quot;",""))
            name = re.sub('[\(\)\{\}<>]', '', name.replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("&quot;","").replace("'",""))
            url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")
            name = name#+ '   ('+ url+')'
            if not '</a>' in name:
                if name not in uniques:
                    uniques.append(name)

                    addDir('[COLOR '+newfont+']'+'%s[/COLOR] - %s'%(passto,url),name,34,iconimage,art+'Main/Fanart_G.jpg',1)


# MODE 34 - SUNFLY actual list of sources (not used)
def SEARCH_GENRE(url,name):
    passit = False
    db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The|)\s','',url))
    if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
        if 'ft' in artist.lower() or 'feat' in artist.lower():
            passit = True
        if passit == False:
            if artist.lower() in name.split('-')[1].lower().strip():
                addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)
        else:
            if name.split('-')[1].lower().strip():
                addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)


# MODE 6 - the actual list of songs by artist
def ARTIST_SONG_SEARCH(name, url, iconimage, fanart):
        url = str(url).replace(' ','+').replace('_','+')
        name = str(name).replace(' ','+')
        url = 'https://www.youtube.com/results?search_query=%s+%s+karaoke&hl=en-GB&page=' % (name, url)
        html=OPEN_URL(url)
        HtmlToResults(html)


# MODE 9 - actual list of songs by genre index or track index
def TRACK_SEARCH(name, url, fanart):
        name = str(name).replace('   (','+') .replace(' ','+') .replace(')','')
        url = 'https://www.youtube.com/results?search_query=%s+karaoke&hl=en-GB&page=' % (name)
        #print url
        html=OPEN_URL(url)
        HtmlToResults(html)


# MODE 15 - list of videos downloaded (not used)
def DOWNLOADS(downloads):
     import glob
     path = downloads
     for infile in glob.glob(os.path.join(path, '*.*')):
         addFile(infile)


# MODE 31 - SUNFLY list of downloads (not used)
def SFDOWNLOADS(sfdownloads):
     import glob
     path = sfdownloads
     for infile in glob.glob(os.path.join(path, '*.avi')):
         addFileSF(infile)


# MODE 16 - SUNFLY search (not used)
def Sunflysearch(search_entered):
    search_entered = search_entered.replace(',', '')
    favs = ADDON.getSetting('favs').split(',')
    if 'url' in search_entered:
        keyboard = xbmc.Keyboard('', '[COLOR grey3]Search by[/COLOR] [COLOR '+newfont+']'+'Artist[/COLOR] [COLOR grey3]or[/COLOR] [COLOR '+newfont+']'+'Track[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered=keyboard.getText()
            db=GRABBER(4,'artist',search_entered)
            if not db: db=GRABBER(4,'artist',re.sub('\A(a|A|the|THE|The)\s','',search_entered))
            if not db: db=GRABBER(4,'track',search_entered)
            if not db: db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The)\s','',search_entered))
            if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
            for sf,number,artist,track,icon,burl in db:
                addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon)

            if not search_entered in favs:
                favs.append(search_entered)
                ADDON.setSetting('favs', ','.join(favs))

    else:
        db=GRABBER(4,'artist',search_entered)
        if not db: db=GRABBER(4,'artist',re.sub('\A(a|A|the|THE|The)\s','',search_entered))
        if not db: db=GRABBER(4,'track',search_entered)
        if not db: db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The)\s','',search_entered))
        if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
        for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon)


# MODE 25 - SUNFLY search (not used)
def SF_SEARCH(url):
    sunfly = 'SF'
    keyboard = xbmc.Keyboard(sunfly, 'Enter Sunfly Disc Number:-')
    keyboard.doModal()
    if keyboard.isConfirmed():
        db=GRABBER(4,'sunfly_name',keyboard.getText())
        if not db: addLinkSF('[COLOR red]DISC NOT AVAILABLE.[/COLOR]',url,'');return
        for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+newfont+']'+'%s:-%s ~ [/COLOR]%s'%(sf,number,track),burl,icon,split=1)


# MODE 23 - SUNFLY list of artists (not used)
def AZ_ARTIST_SEARCH(name):
    db=GRABBER(5,'artist',name)
    if not db: addLinkSF('[COLOR red]ARTIST NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)


# MODE 24 - SUNFLY browse tracks (not used)
def AZ_TRACK_SEARCH(name):
    db=GRABBER(5,'track',re.sub('\A(a|A|the|THE|The)\s','',name))
    if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+newfont+']'+'%s ~ [/COLOR]%s'%(track,artist),burl,icon,split=0)


def addFile(file):
        name = file.replace(downloads,'').replace('.mp4','')
        name = name.split('-[')[-2]
        thumb = icon(file)[0]
        iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % thumb
        url=file
        liz=xbmcgui.ListItem(name, offscreen=True)
        liz.setArt({'icon':'DefaultVideo.png'})
        liz.setArt({'thumb':iconimage})
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        liz = xbmcgui.ListItem(name, offscreen=True)
        contextMenu = []
        contextMenu.append(('Delete', 'RunPlugin(%s?mode=102&url=%s&iconimage=%s)'% (sys.argv[0], file,iconimage)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url,listitem = liz, isFolder = False)


# (not used)
def addFileSF(file):
        file = xbmcvfs.translatePath(file)
        iconimage = file.replace('.avi','.jpg').replace('.mp4','.jpg')
        name = file.replace(xbmcvfs.translatePath(sfdownloads),'').replace('.avi','').replace('.mp4','')
        url=file
        liz=xbmcgui.ListItem(name, offscreen=True)
        liz.setArt({'icon':'DefaultVideo.png'})
        liz.setArt({'thumb':iconimage})
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        contextMenu = []
        contextMenu.append(('Delete', 'RunPlugin(%s?mode=102&url=%s&iconimage=%s)'% (sys.argv[0], file,iconimage)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url,listitem = liz, isFolder = False)


# (not used)
def deleteFileSF(file,iconimage):
    tries    = 0
    maxTries = 10
    while os.path.exists(file) and tries < maxTries:
        try:
            os.remove(file)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1
    while os.path.exists(iconimage) and tries < maxTries:
        try:
            os.remove(iconimage)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1


    if os.path.exists(file):
        d = xbmcgui.Dialog()
        d.ok('Kodi Karaoke', 'Failed to delete file')


def addDir(name,url,mode,iconimage,fanart,number):
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&iconimage="+urllib.parse.quote_plus(iconimage)+"&fanart="+urllib.parse.quote_plus(fanart)+"&number="+str(number)
        name = ''.join([x for x in name if x in string.printable])
        if name.replace(" ","") == "":
            return
        liz=xbmcgui.ListItem(name, offscreen=True)
        liz.setArt({'icon':'DefaultFolder.png'})
        liz.setArt({'thumb':iconimage})
        liz.setArt({'fanart':fanart})
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        menu=[]
        if (mode == 3 or mode==16) and url!='url' :
            menu.append(('[COLOR orange]Remove Search[/COLOR]','Container.Update(%s?mode=5002&name=%s&url=url)'% (sys.argv[0],name)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
        if (mode == 2000)or mode==103 or mode==203:
            if mode ==203:
                liz.setProperty("IsPlayable","true")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)
        if not mode==1 and mode==20 and mode==19:
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)


def addLink(name,url,iconimage,fanart,showcontext=True):
    u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode=6003&name="+urllib.parse.quote_plus(name)+"&iconimage="+urllib.parse.quote_plus(iconimage)+"&fanart="+urllib.parse.quote_plus(fanart)
    name = ''.join([x for x in name if x in string.printable])
    if name.replace(" ","") == "":
        return
    cmd = 'plugin://plugin.video.youtube/?path=root/video&action=download&videoid=%s' % url
    liz=xbmcgui.ListItem(name, offscreen=True)
    liz.setArt({'icon':'DefaultVideo.png'})
    liz.setArt({'thumb':iconimage})
    liz.setArt({'fanart':fanart})
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true")
    menu = []
    if showcontext:
          if mode!=2:
              found=False
              db = database.connect( db_dir );cur = db.cursor()
              cur.execute("SELECT * FROM favourites")
              cached = cur.fetchall()
              if cached:
                  for fname,artist,track,ficonimage,furl in cached:
                     if url == furl:
                          found=True
                          menu.append(('[COLOR red]Remove[/COLOR] from Karaoke Favorites','RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'delete')))
                          break
              db.close()
              if not found:
                  menu.append(('[COLOR green]Add[/COLOR] to Karaoke Favorites','RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'add')))
          else:
              menu.append(('[COLOR red]Remove[/COLOR] from Karaoke Favorites','RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'delete')))

    liz.addContextMenuItems(items=menu, replaceItems=False)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)


# SUNFLY Links (not used)
def addLinkSF(name,url,iconimage,showcontext=True,split=None):
        if 'http' in Kfolder:
            url=url.replace(' ','%20')
        iconimage = xbmcvfs.translatePath(os.path.join(Kfolder,url)).replace('.mp4','.jpg').replace('.avi','.jpg')

        url = xbmcvfs.translatePath(os.path.join(Kfolder,url))

        liz=xbmcgui.ListItem(name, offscreen=True)
        liz.setArt({'icon':'DefaultVideo.png'})
        liz.setArt({'thumb':iconimage})
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty('mimetype', 'video/x-msvideo')
        liz.setProperty("IsPlayable","true")

        menu = []
        if showcontext:
            menu.append(('[COLOR green]Add[/COLOR] to Kodi Karaoke Favorites','RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'add')))
            menu.append(('[COLOR red]Remove[/COLOR] Kodi Karaoke from Favorites','RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'delete')))
        if ADDON.getSetting('sfenable') == 'true':
            menu.append(('[COLOR orange]Download[/COLOR]', 'Container.Update(%s?&mode=30&url=%s&name=%s&iconimage=%s&split=%s)' %(sys.argv[0],url,name,iconimage,split)))
        liz.addContextMenuItems(items=menu, replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)


def PlayYouTube(name,url,iconimage):
    youtube='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s'% url
    liz = xbmcgui.ListItem(name, offscreen=True)
    liz.setArt({'icon':'DefaultVideo.png'})
    liz.setArt({'thumb':iconimage})
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(str(youtube))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


def setView(viewType):
    if viewType=="VIDEO":
        xbmc.executebuiltin("Container.SetViewMode(500)")
        xbmcplugin.setContent(int(sys.argv[1]), "movies")
    else:
        xbmc.executebuiltin("Container.SetViewMode(55)")


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param



# Initialize all our stuff
THESITE ='kodikaraoke.com'
Kfolder= 'http://'+THESITE+'/payments/karaoke/'
K_db=Kfolder+'Karaoke.db'
updateScreen=False
cacheList=False

ADDON = xbmcaddon.Addon(id='plugin.video.kodikaraoke')
sfdownloads= xbmcvfs.translatePath(os.path.join(ADDON.getSetting('sfdownloads'),''))
db_dir = os.path.join(xbmcvfs.translatePath("special://database"), 'Karaoke.db')

datapath = xbmcvfs.translatePath(ADDON.getAddonInfo('profile'))
newfont=ADDON.getSetting('newfont').lower()

if os.path.exists(datapath)==False:
    os.mkdir(datapath)
#if ADDON.getSetting('sfenable') == True:
#    os.makedirs(sfdownloads)
#if ADDON.getSetting('visitor_ga')=='':
#    from random import randint
#    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))

art= "%s/KaraokeArt/"%ADDON.getAddonInfo("path")
from sqlite3 import dbapi2 as database

db = database.connect(db_dir)
db.execute('CREATE TABLE IF NOT EXISTS tracklist (sunfly_name, number, artist, track, iconimage, url)')
db.execute('CREATE TABLE IF NOT EXISTS favourites (track_name, artist, track, iconimage, url)')
db.commit()
db.close()

params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None

try:
        url=urllib.parse.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.parse.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.parse.unquote_plus(params["iconimage"])
except:
        pass
try:
        switch=urllib.parse.unquote_plus(params["switch"])
except:
        switch='display'
try:
        mode=int(params["mode"])
except:
        pass
try:
        fanart=urllib.parse.unquote_plus(params["fanart"])
except:
        pass
try:
        number=int(params["number"])
except:
        pass
try:
        split=int(params["split"])
except:
        pass



# Print (Debug) All Values
print("Mode: " + str(mode))
print("URL: " + str(url))
print("Name: " + str(name))
print("IconImage: " + str(iconimage))
print("FanartImage: " + str(fanart))
try:print("number: " + str(number))
except:pass



# Now we can RUN!
if mode==None or url==None or len(url)<1:
    MAINMENU('url')

elif mode==1:
    AtoZ(url,number,fanart)
    setView('DEFAULT')
    cacheList=True

elif mode==2:
    FAVORITES(switch,name,iconimage,url)
    if switch == 'display':
       setView('VIDEO')

elif mode==3:
    #print(""+url)
    result=SEARCH(url)
    if not result:
       updateScreen=True
       FirstSearchDir()
    else:
       setView('VIDEO')
       cacheList=True

elif mode==4:
    ARTIST_INDEX(url, iconimage, name)
    setView('DEFAULT')
    cacheList=True

elif mode==5:
    ARTIST_SONG_INDEX(url, name)
    setView('DEFAULT')

elif mode==6:
    ARTIST_SONG_SEARCH(name, url, iconimage, fanart)
    setView('VIDEO')
    cacheList=True

elif mode==7:
    TRACK_INDEX(url, iconimage)
    setView('DEFAULT')

elif mode==8:
    GENRE(url)
    cacheList=True

elif mode==9:
    TRACK_SEARCH(name, url, fanart)
    setView('VIDEO')
    cacheList=True

elif mode==10:
    GENRE_INDEX(name, url, iconimage)
    cacheList=True # This list can be very long

elif mode==13:
    addFavorite(name,url,iconimage,fanart)

elif mode==14:
    rmFavorite(name)

elif mode==15:
    DOWNLOADS(downloads)

elif mode==16:
    Sunflysearch(url)

elif mode==17:
    Sunflyurl(name)

elif mode==20:
    ProKaraoke(url)

elif mode==23:
    AZ_ARTIST_SEARCH(name)

elif mode==24:
    AZ_TRACK_SEARCH(name)

elif mode==25:
    SF_SEARCH(name)

elif mode==26:
    print("")
    LATEST_LIST(url)

elif mode==27:
    addSF_Favorite(name,url,iconimage)

elif mode==28:
    rmSF_Favorite(name)

elif mode==29:
    getSF_Favorites()

elif mode==31:
    SFDOWNLOADS(sfdownloads)

elif mode==32:
    GENRESF(url)

elif mode==33:
    GENRE_INDEXSF(name,url, iconimage)

elif mode==34:
    SEARCH_GENRE(url,name)

elif mode==102:
    deleteFileSF(url,iconimage)
    xbmc.executebuiltin("Container.Refresh")

#elif mode==103:
#    import fixdatabase
#
#elif mode==201:
#    download_DB()
#
#elif mode==202:
#    karaokanta_GET(name,url)
#
#elif mode==203:
#    karaokanta_PLAY(name,url)
#
#elif mode==3000:
#    test()

elif mode == 5002:
    favs = ADDON.getSetting('favs').split(",")
    try:
        favs.remove(name.lower())
        ADDON.setSetting('favs', ",".join(favs))
    except:pass
    updateScreen=True
    FirstSearchDir()

elif mode == 5003:
    FirstSearchDir()

elif mode ==6003:
    PlayYouTube(name,url,iconimage)
    setView('VIDEO')
    cacheList=True

elif mode == 99:
    PlayListHandler(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheList, updateListing=updateScreen)
