from pytube import YouTube
import re
import urllib.request
import urllib.error
import sys
import time
 
"""
Usage: run this python script with 2 command line arguments:
1: url of youtube playlist
2: directory in which to save mp4s
"""

def FindBestQuality(YTvid):
    """
    Parameters
    ----------
    YTvid : pytube.api.YouTube
        Youtube video to be downloaded

    Returns
    -------
    QualityString : string
        string describing best quality available in mp4 format for this particular video.
    """
    mp4s_available = YTvid.filter('mp4')
    mp4s_strings = [str(option) for option in mp4s_available]
    matches1 = [re.search(regex1, string) for string in mp4s_strings if re.search(regex1, string)]
    matches2 = [re.search(regex2, string) for string in mp4s_strings if re.search(regex2, string)]
    if matches2 == []:
        matches = matches1
    else:
        matches = matches2
    BestQuality = 0
    for index, match in enumerate(matches):
        Quality = int(match.group(0)[2:-1])
        if Quality > BestQuality:
            BestQuality = Quality
            indexOfBestQuality = index    
    QualityString = str(BestQuality) + 'p'
    return(QualityString)

def crawl(url):
    """
    Code sourced from: http://pantuts.com/2013/02/16/youparse-extract-urls-from-youtube/
    
    Parameters
    ----------
    url : string
        Url of youtube playlist

    Returns
    -------
    urlList : list
        List containing strings which are the url's of the videos in the playlist provided through the url parameter.
    """
    sTUBE = ''
    cPL = ''
    amp = 0
    final_url = []
    
    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
            
    else:
        print('Incorrect Playlist.')
        exit(1)
    
    try:
        yTUBE = urllib.request.urlopen(url).read()
        sTUBE = str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)
    
    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)
 
    if mat:
          
        for PL in mat:
            yPL = str(PL)
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])
 
        all_url = list(set(final_url))
 
        i = 0
        while i < len(all_url):
            #sys.stdout.write(all_url[i] + '\n')
            time.sleep(0.04)
            i = i + 1
        
    else:
        print('No videos found.')
        exit(1)
    return(all_url)

if len(sys.argv) != 3:
    raise ValueError("Need 2 command line arguments: url of playlist and Directory to save mp4s")

urlList = crawl(sys.argv[1])
directory = sys.argv[2]

regex1 = re.compile('- ...p')
regex2 = re.compile('- ....p')

for url in urlList:
    YTvid = YouTube(url)
    QualityString = FindBestQuality(YTvid)
    vid = YTvid.get('mp4', QualityString)
    print("Downloading: {}".format(url))
    vid.download(directory)

