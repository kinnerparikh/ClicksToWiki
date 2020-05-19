import bfs


startURL = input("Input Start Wikipedia URL: ")
print(bfs.bfs(startURL, "https://en.wikipedia.org/wiki/Toilet_paper_orientation"))


