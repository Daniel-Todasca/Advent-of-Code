import matplotlib.pyplot as plt
from matplotlib import colors


points = set()
with open("points.in") as file:
    for line in file:
        x, y = [int(it) for it in line.split()]
        points.add((x, y))

min_x, min_y, max_x, max_y = 0, 0, 50, 10

data = [
    [1 if (x, y) in points else 0 for x in range(min_x, max_x)]
    for y in range(min_y, max_y)
]
cmap = colors.ListedColormap(['red', 'blue'])

fig, ax = plt.subplots()
ax.imshow(data, cmap=cmap)

plt.show()