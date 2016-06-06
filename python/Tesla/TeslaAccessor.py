from Tesla import Tesla
f = open("myTestFile.txt", 'r')
x = f.readlines()
print(x)
Tesla(x[0], int(x[1]), x[2], x[3], x[4])