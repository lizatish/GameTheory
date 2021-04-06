import numpy as np
import matplotlib.pyplot as plt



def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)

fig = plt.figure()
ax = fig.add_subplot(111)

x1 = [0, 1]
y1 = [5, 10]
x2 = [1, 0]
y2 = [4, 6]

ax.plot(x1, y1, color='lightblue',linewidth=3)
ax.plot(x2, y2, color='darkgreen', marker='^')

# Get the common range, from `max(x1[0], x2[0])` to `min(x1[-1], x2[-1])`
x_begin = max(x1[0], x2[0])
x_end = min(x1[-1], x2[-1])

points1 = [t for t in zip(x1, y1) if x_begin<=t[0]<=x_end]  # [(3, 50), (4, 120), (5, 55), (6, 240), (7, 50), (8, 25)]
points2 = [t for t in zip(x2, y2) if x_begin<=t[0]<=x_end]  # [(3, 25), (4, 35), (5, 14), (6, 67), (7, 88), (8, 44)]


x, y = get_intersect((0, 5), (1, 10), (1, 4), (0, 6))
ax.scatter(x, y, s=100, color='red')



plt.show()