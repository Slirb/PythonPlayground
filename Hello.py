import datetime

nums = ["1","2","3"]
for i in nums:
    print (i)

print(datetime.datetime.now())

total = 0

for x in range(1, 101):
    total += x

print(total)

pydict ={
  "First": "V",
  "Last": "Curtis",
  "Age": 32,
  "BirthDay": datetime.datetime(1988, 7, 10),
  "Location": "Bridgman"
}

for y in pydict:
    print(pydict[y])