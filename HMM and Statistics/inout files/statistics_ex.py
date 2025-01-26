data = open('DataFile.txt', 'r')
count = 0
sum = 0
sumPow2 = 0
for line in data:
    for num in map(int, line.split()):
        if count == 0:
            max_num = min_num = num
        else:
            if num > max_num:
                max_num = num
            if num < min_num:
                min_num = num
        count += 1
        sum += num
        sumPow2 += num ** 2
data.close()
average = sum / count
var = (sumPow2 - count * (average ** 2)) / count
Standard_Deviation = (var ** 0.5)

print('Average:', average)
print('Variance:', var)
print('Standard Deviation:', Standard_Deviation)
print('Minimum:', min_num)
print('Maximum:', max_num)

# finding Percentile 60%

data = open('DataFile.txt', 'r')
found = False
while not found:
    mid = (max_num + min_num) / 2
    smaller = 0
    bigger = 0
    for line in data:
        for num in map(int, line.split()):
            if num <= mid:
                smaller += 1
            elif num >= mid:
                bigger += 1
    data.seek(0)
    if 0.595 <= smaller / count <= 0.605:
        found = True
    else:
        if smaller / count < 0.6:
            min_num = mid
        else:
            max_num = mid
print('Percentile 60%:', mid)
