# MIT License

# Copyright (c) 2016 Stefan Zapf, Christopher Kraushaar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Load libraries
import math

import matplotlib.pyplot as plt
import numpy as np
import sys
import csv
import warnings

warnings.filterwarnings("ignore")


def get_angles(orbit, number_of_datapoints, ax):
    start = (2 * math.pi) / 11 * (orbit - 1)
    stop = start + (math.pi / 2)
    if orbit > 0:
        ax.text(0, orbit - 0.1, "{0:.1f}".format(1 - float(orbit) / 10), verticalalignment="top",
                horizontalalignment="center", color="lightgray")
    return np.linspace(start, stop, number_of_datapoints, endpoint=True)


def get_y(angle, radius):
    return math.sin(angle) * radius


def get_x(angle, radius):
    return math.cos(angle) * radius


def label_to_idx(labels, label):
    center_idx_bool = labels == label
    return np.asscalar(np.where(center_idx_bool)[0]), center_idx_bool


def transform_to_correlation_dist(data):
    y_corr = np.corrcoef(data.T)
    # we just need the magnitude of the correlation and don't care whether it's positive or not
    abs_corr = np.abs(y_corr)
    return np.nan_to_num(abs_corr)


def transform_to_positive_corrs(data, sun_idx):
    y_corr = np.corrcoef(data.T)
    positive = y_corr[sun_idx]
    positive = positive >= 0
    return positive


def solar_corr(data, labels, center, orbits=10, show_window=True, image_path="solar.png", save_png=True):
    labels = np.array(labels)
    center_idx, center_idx_bool = label_to_idx(labels, center)

    all_idx = np.logical_not(center_idx_bool)
    positive = transform_to_positive_corrs(data, center_idx)
    corr_dist = transform_to_correlation_dist(data)
    sun_corr_dist = corr_dist[center_idx]
    colors = np.linspace(0, 1, num=len(sun_corr_dist))

    step = 1.0 / orbits
    last_orbit = 0.0
    fig = plt.gcf()
    fig.set_size_inches(20, 20)
    labels_idx = np.array([center_idx])

    color_map = plt.get_cmap("Paired")
    color_map_circle = plt.get_cmap("Accent")

    ax = fig.add_subplot(111)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_position([0.01, 0.01, 0.98, 0.98])  # set a new position

    # place sun:
    plt.scatter(0, 0, color=color_map(colors[center_idx]), s=600, label=labels[center_idx])
    ax.text(0.2, 0.2, str(labels[center_idx]), verticalalignment="bottom", horizontalalignment='left', color="gray")

    for orbit in range(1, orbits + 1):
        new_orbit = step * orbit + 0.1
        idx = (sun_corr_dist >= (1 - last_orbit)) & (sun_corr_dist > (1 - new_orbit)) & all_idx
        idx_int = np.where(idx)[0]

        corr_dists = []
        for index in idx_int:
            corr_dists = np.append(corr_dists, corr_dist[center_idx][index])
        sort_args = np.argsort(corr_dists)
        idx_int = idx_int[sort_args]

        labels_idx = np.append(labels_idx, idx_int)
        planets = sum(idx)
        angles = get_angles(orbit, planets, ax)

        # place planets
        while np.any(idx):
            remaining = sum(idx)
            current_planet = planets - remaining
            current_idx = idx_int[current_planet]
            angle = angles[current_planet]
            x = get_x(angle, orbit)
            y = get_y(angle, orbit)
            # current_idx = idx_int[current_planet]
            color = colors[current_idx]
            plt.scatter(x, y, color=color_map(color), s=250, label=labels[current_idx])
            planet_idx = current_idx
            idx[planet_idx] = False
            all_idx[planet_idx] = False

            planet_corr = corr_dist[planet_idx]
            # ax.text(x-0.35, y+0.2, "{0:.3f}".format(planet_corr[center_idx]))
            col = "#03C03C" if positive[planet_idx] else "#FF6961"
            if orbit == orbits:
                col = "grey"
            ax.text(x + 0.15, y + 0.15, str(labels[planet_idx]), verticalalignment="bottom", horizontalalignment='left',
                    color=col)
            moon_idx = (planet_corr >= 0.8) & all_idx
            moon_idx_int = np.where(moon_idx)[0]
            moons = sum(moon_idx)
            moon_angles = get_angles(0, moons, ax)

            # add orbit around planet if it has moons
            if np.any(moon_idx):
                moon_orbit = 0.5
                circle = plt.Circle((x, y), moon_orbit, color='lightgrey', alpha=0.8, fill=True, zorder=0)
                fig.gca().add_artist(circle)

            while np.any(moon_idx):
                remaining_moons = sum(moon_idx)
                current_moon = moons - remaining_moons
                current_moon_idx = moon_idx_int[current_moon]
                angle = moon_angles[current_moon]
                m_x = get_x(angle, moon_orbit) + x
                m_y = get_y(angle, moon_orbit) + y
                color = colors[current_moon_idx]
                plt.scatter(m_x, m_y, color=color_map(color), s=100, label=labels[current_moon_idx])
                col = "#03C03C" if positive[current_moon_idx] else "#FF6961"
                if orbit == orbits:
                    col = "grey"
                ax.text(m_x + 0.15, m_y + 0.05, str(labels[current_moon_idx]), verticalalignment="bottom",
                        horizontalalignment='left', color=col)
                moon_idx[current_moon_idx] = False
                idx[current_moon_idx] = False
                all_idx[current_moon_idx] = False

        last_orbit = new_orbit

        circle = plt.Circle((0, 0), orbit, color=color_map_circle(1 - ((orbit - 1) * step)), fill=False, zorder=0)
        fig.gca().add_artist(circle)

    labels_pos = np.array(labels)[labels_idx]
    recs = []
    ax = plt.gca()

    ax.axis("equal")
    plt.axis([-10, 10, -10, 10])
    if save_png:
        plt.savefig(image_path)

    if show_window:
        plt.show()


def main(input_csv, sun, image_path):
    # Load data
    data = np.genfromtxt(input_csv, delimiter=",", skip_header=1)
    labels = csv.DictReader(open(input_csv), skipinitialspace=True).fieldnames
    solar_corr(data, labels, sun, image_path=image_path)


if __name__ == "__main__":
    try:
        image_path = sys.argv[3] if len(sys.argv) > 3 else "solar.png"
        main(sys.argv[1], sys.argv[2], image_path)
    except:
        print("python -m solar_correlation_map CSV_FILE_PATH SUN_VARIABLE [IMAGE_FILE_NAME]")
        print("example: python -m solar_correlation_map jedi.csv JEDI jedi.png")
