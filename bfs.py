import urllib.request
import queue
import re

regex = re.compile('(?:a href=("\/wiki\/[^:]*?"))')



def bfs(homeURL, destURL):
    sMap = {}
    sMap[destURL] = None

    q = queue.Queue()
    parents = {}
    distance = 0
    currPath = []
    pathDistance = float("inf")

    parents[homeURL] = None
    q.put(homeURL)

    if homeURL == destURL:
        return [homeURL, destURL]

    while not q.empty():
        current = q.get()
        distance += 1

        print(current)

        if distance >= pathDistance:
            return currPath

        for currURL in links(current, regex):

            if currURL == destURL:
                parents[currURL] = current
                path = pathCall(parents, currURL)
                pathToSMap(path, sMap)
                return path

            elif currURL in sMap:
                parents[currURL] = current
                print("Found shortcut for " + currURL + " to end")
                path = pathCall(parents, currURL)
                ending = pathCall(sMap, currURL)
                ending.reverse()
                ending.remove(currURL)
                currPath = path + ending
                pathDistance = len(currPath) - 1

            else:
                if currURL not in parents:
                    parents[currURL] = current
                    q.put(currURL)

    return currPath


def pathCall(parents, end):

    path = [end]
    current = end

    while parents[current] is not None:
        path.insert(0, parents[current])
        current = parents[current]

    return path


def pathToSMap(path, sMap):

    for i in range(len(path) - 1):
        sMap[path[i]] = path[i + 1]

def links(inputURL, regex):

    request = urllib.request.urlopen(inputURL)
    html = str(request.read())

    links = set([])

    for link in regex.findall(html):
        links.add("http://en.wikipedia.org" + link.split("\"")[1])

    return links