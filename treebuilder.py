import csv

with open('file', 'r') as f:
    reader = csv.reader(f)
    ls = list(reader)

tree = {}

for item in ls:
    t = tree
    for part in item[0].split('.'):
        t = t.setdefault(part, {})

print(tree)
