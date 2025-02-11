import numpy as np
import matplotlib.pyplot as plt


# Define the function f
def f(x):
    if x < -3:
        return float("inf")
    elif -3 <= x < 0:
        return -x + 1
    elif 0 <= x <= 2.5:
        return 1 + 0.3 * x**2
    else:
        return (6 - 2.875) / (4 - 2.5) * (x - 2.5) + 2.875


def M(x, lambda_):
    # Moreau envelope of f at x
    y = [f(xi) + lambda_ / 2 * (xi - x) ** 2 for xi in np.linspace(-6, 6, 500)]
    return np.min(y)


# Generate x values
x = np.linspace(-5, 5, 501)

# Calculate y values using the function f
ys = [f(xi) for xi in x]
Ms = [M(xi, 1) for xi in x]

if False:
    # plt.plot(x, ys, label="Piecewise function f(x)", color="blue", linewidth=2)
    # plt.plot(x, Ms, label="Moreau envelope M(x)", color="red", linewidth=2)

    # # Add labels and title
    # plt.xlabel("x")
    # plt.ylabel("f(x)")
    # plt.title("Plot of the f and line segments")
    # plt.legend()

    # # Show the plot
    # plt.grid(True)
    # plt.show()

    print("\\draw[thick, blue] plot[smooth] coordinates {")
    for i in range(len(x)):
        print(f"({x[i]}, {Ms[i]})")
    print("};")
else:
    plt.plot(x, ys, label="Piecewise function f(x)", color="blue", linewidth=2)
    for v in [-2, -1, 0, 1, 2]:
        lambda_ = 1.0
        ys = [f(xi) + 1 / (2 * lambda_) * (xi - v) ** 2 for xi in x]
        plt.plot(x, ys, linewidth=2)
        print(v)
        print(x[np.argmin(ys)], np.min(ys))
        # for xi in x:
        #     if f(xi) + 1 / (2 * lambda_) * (xi - v) ** 2 <= 6 + 1e-6:
        #         print(xi)
        #         break
        # for xi in x[::-1]:
        #     if f(xi) + 1 / (2 * lambda_) * (xi - v) ** 2 <= 6 + 1e-6:
        #         print(xi)
        #         break

    # Add labels and title
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Plot of the f and proximal operator")
    plt.legend()

    plt.xlim(-5, 5)
    plt.ylim(-1, 8)

    # Show the plot
    plt.grid(True)
    plt.show()
