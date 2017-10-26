ls = ['one.two.three.four', 'one.six.seven.eight', 'five.nine.ten', 'twelve.zero']
tree = {}

for item in ls:
    t = tree
    for part in item.split('.'):
        t = t.setdefault(part, {})

print(tree)