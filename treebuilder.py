import csv

with open(r"file", 'r') as f:
    reader = csv.reader(f)
    ls = list(reader)

tree = {}

for item in ls:
    t = tree
    counter = 0
    for part in item[0].split('.'):
        if (counter == 0):
            t = t.setdefault(part, {})
        elif (counter == 1):
            t = t.setdefault(part, [])
        elif (counter == 3):
            t = t.append(part)
        counter += 1

with open(r"file", 'w') as f:
    f.write(str(tree))
