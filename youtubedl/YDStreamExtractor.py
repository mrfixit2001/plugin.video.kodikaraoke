import os
import time
import xbmc
import sys

from youtubedl import YoutubeDLWrapper
from youtubedl.yd_private_libs import util

import urllib.parse as urlparse
from urllib.parse import urlencode
import http.client as httplib

###############################################################################
# Private Methods
###############################################################################
def _getQualityLimits(quality):
    minHeight = 0
    maxHeight = 480
    if quality > 2:
        minHeight = 0
        maxHeight = 999999
    elif quality > 1:
        minHeight = 721
        maxHeight = 1080
    elif quality > 0:
        minHeight = 481
        maxHeight = 720
    return minHeight, maxHeight


def _selectVideoQuality(r):
    """
    Quality is 0=SD, 1=720p, 2=1080p, 3=Highest Available
    Default is 1080p
    """
    import xbmcaddon
    ADDON = xbmcaddon.Addon(id='plugin.video.kodikaraoke')
    qStr=ADDON.getSetting('video_quality').lower()
    quality=2
    if qStr == "sd":
        quality = 0
    elif qStr == "720p":
        quality = 1
    elif qStr == "max":
        quality = 3

    util.LOG('YTDL Quality Setting: {0}'.format(quality), debug=True)

    disable_dash = False
    skip_no_audio = True

    entries = r.get('entries') or [r]
    minHeight, maxHeight = _getQualityLimits(quality)

    urls = []
    idx = 0
    for entry in entries:
        defFormat = None
        defMax = 0
        defPref = -1000

        prefFormat = None
        prefMax = 0
        prefPref = -1000

        index = {}
        formats = entry.get('formats') or [entry]

        for i in range(len(formats)):
            index[formats[i]['format_id']] = i

        keys = sorted(index.keys())
        fallback = formats[index[keys[0]]]
        for fmt in keys:
            fdata = formats[index[fmt]]

            h = None
            if 'height' in fdata:
                h = fdata['height']
            if h is None:
                h = 1

            p = fdata.get('preference', 1)
            if p is None:
                p = 1

            w = None
            if 'width' in fdata:
                w = fdata['width']
            if w is None:
                w = 1

            #util.LOG("Checking format " + str(fdata['format_id']) + ": " + str(w) + "x" + str(h) + "(" + str(fdata['vcodec']) + "/" + str(fdata['acodec']) + ")")
            if skip_no_audio:
                if 'acodec' not in fdata:
                    continue
                if str(fdata['acodec']) == 'none':
                    continue;

            if disable_dash and 'dash' in fdata.get('format_note', '').lower():
                continue

            if h >= minHeight and h <= maxHeight:
                if (h >= prefMax and p > prefPref) or (h > prefMax and p >= prefPref):
                    prefFormat = fdata
                    prefMax = h
                    prefPref = p

            elif(h >= defMax and h <= maxHeight and p > defPref) or (h > defMax and h <= maxHeight and p >= defPref):
                defFormat = fdata
                defMax = h
                defPref = p

        formatID = None
        if prefFormat:
            info = prefFormat
            logBase = '[{3}] Using Preferred Format: {0} ({1}x{2})'
        elif defFormat:
            info = defFormat
            logBase = '[{3}] Using Default Format: {0} ({1}x{2})'
        else:
            info = fallback
            logBase = '[{3}] Using Fallback Format: {0} ({1}x{2})'

        url = info['url']
        formatID = info['format_id']
        util.LOG(logBase.format(formatID, info.get('width', '?'), info.get('height', '?'), entry.get('title', '').encode('ascii', 'replace')))
        if url.find("rtmp") == -1:
            url += '|' + urlencode({'User-Agent': entry.get('user_agent') or YoutubeDLWrapper.std_headers['User-Agent']})
        else:
            url += ' playpath=' + fdata['play_path']

        new_info = dict(entry)
        new_info.update(info)
        urls.append(
            {
                'xbmc_url': url,
                'url': info['url'],
                'title': entry.get('title', ''),
                'thumbnail': entry.get('thumbnail', ''),
                'formatID': formatID,
                'idx': idx,
                'ytdl_format': new_info
            }
        )
        idx += 1

    return urls


# Recursively follow redirects until there isn't a location header
# Credit to: Zachary Witte @ http://www.zacwitte.com/resolving-http-redirects-in-python
def resolve_http_redirect(url, depth=0):
    if depth > 10:
        raise Exception("Redirected " + depth + " times, giving up.")
    o = urlparse.urlparse(url, allow_fragments=True)
    conn = httplib.HTTPConnection(o.netloc)
    path = o.path
    if o.query:
        path += '?' + o.query
    conn.request("HEAD", path, headers={'User-Agent': YoutubeDLWrapper.std_headers['User-Agent']})
    res = conn.getresponse()
    headers = dict(res.getheaders())
    if 'location' in headers and headers['location'] != url:
        return resolve_http_redirect(headers['location'], depth + 1)
    else:
        return url

def _getYoutubeDLVideo(url):
    resolve_redirects = True
    if resolve_redirects:
        try:
            url = resolve_http_redirect(url)
        except Exception:
            util.ERROR('_getYoutubeDLVideo(): Failed to resolve URL')
            return None

    ytdl = YoutubeDLWrapper._getYTDL()
    ytdl.clearDownloadParams()
    try:
        r = ytdl.extract_info(url, download=False)
    except YoutubeDLWrapper.DownloadError:
        util.ERROR('_getYoutubeDLVideo(): Download Error')
        return None

    urls = _selectVideoQuality(r)
    if not urls:
        util.ERROR('_getYoutubeDLVideo(): Failed to select video quality')
        return None

    info = YoutubeDLWrapper.VideoInfo(r.get('id', ''))
    info._streams = urls
    info.title = r.get('title', urls[0]['title'])
    info.description = r.get('description', '')
    info.thumbnail = r.get('thumbnail', urls[0]['thumbnail'])
    info.sourceName = r.get('extractor', '')
    info.info = r
    return info

def getVideoInfo(url):
    """
    Returns a VideoInfo object or None.
    """
    try:
        info = _getYoutubeDLVideo(url)
        if not info:
            return None
    except Exception:
        util.ERROR('_getYoutubeDLVideo() failed', hide_tb=True)
        return None
    return info

def overrideParam(key, val):
    """
    Override a youtube_dl parmeter.
    """
    YoutubeDLWrapper._OVERRIDE_PARAMS[key] = val
