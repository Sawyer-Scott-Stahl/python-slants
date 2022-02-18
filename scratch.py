path = [0, 1, 2, 3, 0]
newpath = []
for i in range(1, len(path)):
    newpath.append(path[i])
print(path)
print(newpath)
if path[0] in newpath:
    print("ye")
