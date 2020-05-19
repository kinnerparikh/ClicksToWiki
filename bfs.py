import urllib.request
import queue
import re

regex = re.compile('(?:a href=("\/wiki\/[^:]*?"))')


def bfs(start_url, end_url, shortcut_mapping):
    shortcut_mapping[end_url] = None

    q = queue.Queue()
    parents = {}
    dist = 0
    curr_path = []
    path_dist = float("inf")

    parents[start_url] = None
    q.put(start_url)

    if start_url == end_url:
        return [start_url, end_url]

    while not q.empty():

        current = q.get()
        dist += 1

        print("Working with " + current)
        if dist >= path_dist:
            return curr_path

        for nbr in get_Links(current, regex):

            if nbr == end_url:
                parents[nbr] = current
                path = path_traceback(parents, nbr)
                add_path_to_mapping(path, shortcut_mapping)
                return path

            elif nbr in shortcut_mapping:
                parents[nbr] = current
                print("Found shortcut for " + nbr + " to end")
                path = path_traceback(parents, nbr)
                ending = path_traceback(shortcut_mapping, nbr)
                ending.reverse()
                ending.remove(nbr)
                curr_path = path + ending
                path_dist = len(curr_path) - 1

            else:
                if nbr not in parents:
                    parents[nbr] = current
                    q.put(nbr)

    return curr_path


def path_traceback(parents, end):

    path = [end]
    current = end

    while parents[current] is not None:
        path.insert(0, parents[current])
        current = parents[current]

    return path


def add_path_to_mapping(path, shortcut_mapping):

    for idx in range(len(path) - 1):
        shortcut_mapping[path[idx]] = path[idx + 1]

def get_Links(url_in, regex):

    resp = urllib.request.urlopen(url_in)
    html = str(resp.read())

    links_set = set([])

    for link in regex.findall(html):
        links_set.add("http://en.wikipedia.org" + link.split("\"")[1])

    return links_set