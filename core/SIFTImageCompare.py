
import numpy as np
import urllib2
import cv2

import threading
from pprint import pprint


# Initiate SIFT detector
SIFT = cv2.xfeatures2d.SIFT_create()

SIMILARITY_THRESHOLD = 0.75
NUM_THREADS = 10
IMG_HEADERS_REQ = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }


def url_to_image(url):
   
    req = urllib2.Request(url, None, IMG_HEADERS_REQ)
    
    try:
        response = urllib2.urlopen(req)
        image = np.asarray(bytearray(response.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
        
    except:
        return None


def compare(query, source):
        
    # find the keypoints and descriptors with SIFT
    kp1, des1 = SIFT.detectAndCompute(query,None)
    kp2, des2 = SIFT.detectAndCompute(source,None)
    
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    
    rank = 0
    # Apply ratio test
    for m,n in matches:
        if m.distance < SIMILARITY_THRESHOLD * n.distance:
            rank = rank + 1
    
    return rank


def compareFromPATH(pathQueryImg, pathSourceImg):
    
    query = cv2.imread(pathQueryImg)
    source = cv2.imread(pathSourceImg)
    
    return compare(query, source)


def compareFromURL(urlQueryImg, pathSourceImg):

    ### ottieni l'immagine da url
    ### invoca la procedura compare
    
    query = url_to_image(urlQueryImg)
    
    ### se l'url non era corretto, oppure l'immagine non esiste piu', restituisci direttamente 0 (nessun match)
    if query is None:
        return 0
    
    source = cv2.imread(pathSourceImg)
    
    return compare(query, source)


def __compare_from_path_task(pathQueryImg, pathSourceImg, result):
    result[pathQueryImg] = compareFromPATH(pathQueryImg, pathSourceImg)
    return

def __compare_from_url_task(urlQueryImg, pathSourceImg, result):
    result[urlQueryImg] = compareFromURL(urlQueryImg, pathSourceImg)
    return


def multipleCompareFromPATH(listPathQueryImg, pathSourceImg):
    
    threads = []
    results = {}

    counter = len(listPathQueryImg)
    count_era = 0
    
    while counter > NUM_THREADS :
        
        pprint("count_era : " + str(count_era) )
        start = count_era*NUM_THREADS
        end = (count_era+1)*NUM_THREADS - 1
        pprint("start:" + str(start) + "  end:" + str(end) )
        
        for i in range( start, end ):
            t = threading.Thread(target=__compare_from_path_task, args=(listPathQueryImg[i], pathSourceImg, results) )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        threads = []
    
        counter  = counter - NUM_THREADS
        count_era = count_era + 1
        
    
    if counter > 0 :
        
        pprint("(remaining)count_era : " + str(count_era) )
        start = count_era*NUM_THREADS
        end = len(listPathQueryImg)-1
        pprint("start:" + str(start) + "  end:" + str(end) )
        
        for i in range( start, end ):
            t = threading.Thread(target=__compare_from_path_task, args=(listPathQueryImg[i], pathSourceImg, results) )
            t.start()
            threads.append(t)
            
        for t in threads:
            t.join()
            threads = []
    
    return results


def multipleCompareFromURL(listUrlQueryImg, pathSourceImg):
    
    threads = []
    results = {}
    
    counter = len(listUrlQueryImg)
    count_era = 0
    
    
    while counter > NUM_THREADS :
        
        #pprint("count_era : " + str(count_era) )
        start = count_era*NUM_THREADS
        end = (count_era+1)*NUM_THREADS - 1
        #pprint("start:" + str(start) + "  end:" + str(end) )
        
        for i in range( start, end ):
            t = threading.Thread(target=__compare_from_url_task, args=(listUrlQueryImg[i], pathSourceImg, results) )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        threads = []
    
        counter  = counter - NUM_THREADS
        count_era = count_era + 1
    
    
    if counter > 0 :
        
        #pprint("(remaining)count_era : " + str(count_era) )
        start = count_era*NUM_THREADS
        end = len(listUrlQueryImg)-1
        #pprint("start:" + str(start) + "  end:" + str(end) )
        
        for i in range( start, end ):
            t = threading.Thread(target=__compare_from_url_task, args=(listUrlQueryImg[i], pathSourceImg, results) )
            t.start()
            threads.append(t)
            
        for t in threads:
            t.join()
            threads = []
    
    return results



      