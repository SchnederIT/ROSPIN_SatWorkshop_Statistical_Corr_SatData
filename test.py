from stat_analysis.dummy_bitmaps import X, Y
from stat_analysis.grad_analysis import gradient_difference
from bitmap_plot.mapplot import plot_matrix_color_scale
import matplotlib.pyplot as plt

if __name__ == '__main__':
    Result = gradient_difference(X, Y)
    plot_matrix_color_scale(X, "X")
    plot_matrix_color_scale(Y, "Y")

    plot_matrix_color_scale(Result, "Gradient difference X-Y")
    plot_matrix_color_scale(gradient_difference(X, X), "Gradient diff X-X")

    plt.show()