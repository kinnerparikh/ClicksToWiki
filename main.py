import bfs

shortcut_mapping = {}

in_start = input("Input Start Wikipedia URL: ")
in_end = input("Input End Wikipedia URL: ")
print(bfs.bfs(in_start, in_end, shortcut_mapping))


