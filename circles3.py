import math

import matplotlib.pyplot as plt


def plotpoint(x, y):  # this function plots points
    p = plt.Circle((x, y), 0.02, color="red")
    ax.add_patch(p)


def fourth(F, A, L, CR):
    # this function uses a cross ratio and three points to plot a
    # fourth point.
    CR = -CR
    B = (CR * (F - A) * L - F * (L - A)) / (CR * (F - A) - L + A)
    return B


def dist(p, q):  # calculates distance between points p and q
    return math.sqrt((p.real - q.real) ** 2 + (p.imag - q.imag) ** 2)


def squiggle(x, y, z, CR_i, h, H_max, dis):
    global cross_ratios
    global visited
    B = None
    if h == 0:
        h = h + 1
        for w in [x, y, z]:
            visited = visited + [w]

        points = [(x, y, z), (y, z, x), (z, x, y)]
        for i, (F, A, L) in enumerate(points):
            B = fourth(F, A, L, cross_ratios[i])
            visited = visited + [B]
            squiggle(F, L, B, i, h, H_max, dis)

    elif h < H_max:  # <== number of iterations
        CR_i_orig = CR_i
        if dist(x, z) > dis:
            CR_i = (CR_i_orig + 2) % 3
            B = fourth(x, y, z, cross_ratios[CR_i])
            if B not in visited:
                visited = visited + [B]
                squiggle(x, z, B, CR_i, h + 1, H_max, dis)
            else:
                print("duplicate B value", B)
                plotpoint(B.real, B.imag)

        if dist(z, y) > dis:
            CR_i = (CR_i_orig + 1) % 3
            B = fourth(z, x, y, cross_ratios[CR_i])
            if B not in visited:
                visited = visited + [B]
                squiggle(z, y, B, CR_i, h + 1, H_max, dis)
            else:
                print("duplicate B value", B)
                plotpoint(B.real, B.imag)
        return


"""Below is where we have our parameters and variables"""

# initializing the plots
fig, ax = plt.subplots()
ax = plt.gca()

# F,A,L are initial points
F = 1j
A = math.sqrt(3) / 2 - math.sqrt(1) / 2 * 1j
L = -math.sqrt(3) / 2 - math.sqrt(1) / 2 * 1j

visited = []  # initializing the set of points

# a,b,c correspond to cross ratios A,B,C where
# A = 1+ai, B=1+bi, C=1+ci
a = 200000
b = 200000
c = (1 / ((1 + a * 1j) * (1 + b * 1j)) - 1) / (1j)
cross_ratios = [1 + a * 1j, 1 + b * 1j, 1 + c * 1j]
print(cross_ratios)

# H_max is the maximum number of iterations
H_max = 100

# distance is the distance we check for between points
distance = 0.001

# below is the maximum number of points that can be plotted
# given the number of iterations
print("maximum points", 3 * 2**H_max)

# squiggle is the recursive funtion call
squiggle(F, A, L, 0, 0, H_max=H_max, dis=distance)

# below tells us how many points were plotted
print("plotted", len(visited), "points")


"""below is how points are plotted"""


# note we must use plt.subplots, not plt.subplot


max_real = max(visited, key=lambda c: c.real).real
max_imag = max(visited, key=lambda c: c.imag).imag
min_real = min(visited, key=lambda c: c.real).real
min_imag = min(visited, key=lambda c: c.imag).imag

# change default domain and range
ax.set_xlim((min_real - 0.05, max_real + 0.05))
ax.set_ylim((min_imag - 0.05, max_imag + 0.05))

# below draws the unit circle
circle1 = plt.Circle((0, 0), 1, fill=False)
ax.add_patch(circle1)

xAH = [B.real for B in visited]
yAH = [B.imag for B in visited]

ax.plot(
    xAH,
    yAH,
    marker="o",
    markersize=0.15,
    linewidth=0,
    markeredgecolor="blue",
    markerfacecolor="blue",
)

figure_text = (
    f"A: {1 + a * 1j:.1f}, B: {1 + b * 1j:.1f}, "
    + f"C: {1 + c * 1j:.7f}\nh_max: {H_max}, distance: {distance}"
)
fig.text(
    0.1, 0, figure_text, va="bottom", wrap=True, fontsize="small"
)


plt.show()
