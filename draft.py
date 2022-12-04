
with open("test.py","r") as f:
    data = f.read()
for i in data:
    print(chr(i),i,end=' ')