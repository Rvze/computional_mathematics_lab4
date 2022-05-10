import matplotlib.pyplot as plt


def plot(x, y, plot_x, plot_ys, labels):
    plt.gcf().canvas.set_window_title("График")

    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.plot(1, 0, marker=">", ms=5, color='k',
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker="^", ms=5, color='k',
            transform=ax.get_xaxis_transform(), clip_on=False)

    plt.plot(x, y, 'ro')
    for i in range(len(plot_ys)):
        plt.plot(plot_x, plot_ys[i], label=labels[i])

    plt.legend()
    plt.show(block=False)
