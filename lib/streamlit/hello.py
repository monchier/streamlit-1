# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A "Hello World" app."""

import streamlit as st
import inspect
from collections import OrderedDict


def intro():
    st.markdown(
        """
## Intro...

text text text text text text text text text text text text text text text text
text text text text text text text text text text text text text text text text
text text text text text text text text text text text text text text text text
text text text text text text text text text text text text text text text text
text text text text text text text text text text text text text text text text
text text text text text text text text text text text text text text text text
"""
    )


def demo_random_numbers():
    """
    Welcome to Streamlit! we're generating a bunch of random numbers in a loop
    for around 10 seconds. Enjoy!.
    """
    import time
    import numpy as np

    progress_bar, success = None, None
    status_text = st.empty()
    chart = st.line_chart(np.random.randn(10, 1))
    for i in range(1, 101):
        new_rows = np.random.randn(10, 1)
        status_text.text("The latest random number is: %s" % new_rows[-1, 0])
        chart.add_rows(new_rows)
        if progress_bar is None:
            progress_bar = st.progress(0)
            success = st.empty()
        progress_bar.progress(i)
        time.sleep(0.1)
    progress_bar.empty()
    success.success("Complete!")
    st.button("Re-run")


def demo_sinc():
    """
    Welcome to Streamlit! we're generating a bunch of random numbers in a loop
    for around 10 seconds. Enjoy!.
    """
    import time
    import numpy as np

    progress_bar, success = None, None
    status_text = st.empty()
    chart = st.line_chart(np.sinc(np.linspace(-5, 5, 100)))
    for i in range(1, 101):
        new_rows = np.sinc(np.linspace(-5, 5, 100) * i)
        # status_text.text("The latest random number is: %s" % new_rows[-1, 0])
        chart.line_chart(new_rows)
        if progress_bar is None:
            progress_bar = st.progress(0)
            success = st.empty()
        progress_bar.progress(i)
        time.sleep(0.1)
    progress_bar.empty()
    success.success("Complete!")
    st.button("Re-run")


def demo_repetitions():
    """
    In this demo, we ask you to enter your name in the input box below.
    Streamlit will print it out with a number of repetitions given by a
    slider that you can control.
    """
    name = st.text_input("Your name")
    repetitions = st.slider("Repetitions", 1, 100, 10)
    st.write(name + "".join((" %s" % name) * (repetitions - 1)))


def demo_bart_vs_bikes():
    """
    Bart vs bikes!
    """
    import pandas as pd
    import os
    import copy

    @st.cache
    def from_data_file(filename):
        dirname = (
            "https://raw.githubusercontent.com/streamlit/streamlit/develop/examples/"
        )
        url = os.path.join(dirname, "data", filename)
        return pd.read_json(url)

    # Grab some data
    bart_stop_stats = copy.deepcopy(from_data_file("bart_stop_stats.json"))
    bart_path_stats = from_data_file("bart_path_stats.json")
    bike_rental_stats = from_data_file("bike_rental_stats.json")

    # Move bart stop name to the 1st column, so it looks nicer when printed as a
    # table.
    bart_stop_names = bart_stop_stats["name"]
    bart_stop_stats.drop(labels=["name"], axis=1, inplace=True)
    bart_stop_stats.insert(0, "name", bart_stop_names)

    st.deck_gl_chart(
        viewport={"latitude": 37.76, "longitude": -122.4, "zoom": 11, "pitch": 50},
        layers=[
            {
                # Plot number of bike rentals throughtout the city
                "type": "HexagonLayer",
                "data": bike_rental_stats,
                "radius": 200,
                "elevationScale": 4,
                "elevationRange": [0, 1000],
                "pickable": True,
                "extruded": True,
            },
            {
                # Now plot locations of Bart stops
                # ...and let's size the stops according to traffic
                "type": "ScatterplotLayer",
                "data": bart_stop_stats,
                "radiusScale": 10,
                "getRadius": 50,
            },
            {
                # Now Add names of Bart stops
                "type": "TextLayer",
                "data": bart_stop_stats,
                "getText": "name",
                "getColor": [0, 0, 0, 200],
                "getSize": 15,
            },
            {
                # And draw some arcs connecting the stops
                "type": "ArcLayer",
                "data": bart_path_stats,
                "pickable": True,
                "autoHighlight": True,
                "getStrokeWidth": 10,
            },
        ],
    )


def demo_progress_bar():
    """
    This demo shows how to use Streamlit to implement a progress bar.
    """
    import time

    progress_text = st.text("0%")
    progress_bar = st.progress(0)
    success = st.empty()
    for percent_complete in range(1, 101):
        progress_text.text("%d%%" % percent_complete)
        progress_bar.progress(percent_complete)
        time.sleep(0.1)
    progress_bar.empty()
    success.success("Complete!")
    st.balloons()
    st.button("Re-run")


IMAGE_URL = "https://unsplash.com/photos/k0rVudBoB4c/download?force=true"
counter = 0

# https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib
# https://en.wikipedia.org/wiki/Julia_set
def demo_fractals():
    """
    Fractal! This small app allow you to explore the Julia sets.
    """
    import numpy as np
    import matplotlib.pyplot as plt

    def fig2data(fig):
        """
        @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
        @param fig a matplotlib figure
        @return a numpy 3D array of RGBA values
        """
        # draw the renderer
        fig.canvas.draw()

        # Get the RGBA buffer from the figure
        w, h = fig.canvas.get_width_height()
        buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
        buf.shape = (w, h, 3)

        # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
        # buf = np.roll(buf, 3, axis=2)
        return buf

    iterations = st.slider("Iterations", 0, 250, 100, 10)
    # c = st.selectbox(
    #     "Polynomial constant", [-0.4 + 0.6j, 0.285 + 0.01j, -0.8 + 0.156j, -0.8j]
    # )

    m, n, s = 480, 320, 300
    x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
    y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))
    plot = st.pyplot()
    plt.axis("off")
    for a in np.linspace(0.0, 2 * np.pi, 15):
        c = 0.7885 * np.exp(1j * a)
        Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
        C = np.full((n, m), c)
        M = np.full((n, m), True, dtype=bool)
        N = np.zeros((n, m))

        for i in range(iterations):
            Z[M] = Z[M] * Z[M] + C[M]
            M[np.abs(Z) > 2] = False
            N[M] = i

        plt.imshow(np.flipud(N), cmap="hot")
        plot.pyplot()


def demo_deformation():
    """
    <...>.
    """
    import requests
    from io import BytesIO

    @st.cache(show_spinner=False)
    def load_image():
        return Image.open(BytesIO(requests.get(IMAGE_URL).content))

    import numpy as np
    from PIL import Image

    def griddify(rect, w_div, h_div):
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        x_step = w / float(w_div)
        y_step = h / float(h_div)
        y = rect[1]
        grid_vertex_matrix = []
        for _ in range(h_div + 1):
            grid_vertex_matrix.append([])
            x = rect[0]
            for _ in range(w_div + 1):
                grid_vertex_matrix[-1].append([int(x), int(y)])
                x += x_step
            y += y_step
        grid = np.array(grid_vertex_matrix)
        return grid

    def distort_grid(org_grid, max_shift):
        new_grid = np.copy(org_grid)
        x_min = np.min(new_grid[:, :, 0])
        y_min = np.min(new_grid[:, :, 1])
        x_max = np.max(new_grid[:, :, 0])
        y_max = np.max(new_grid[:, :, 1])
        new_grid += np.random.randint(-max_shift, max_shift + 1, new_grid.shape)
        new_grid[:, :, 0] = np.maximum(x_min, new_grid[:, :, 0])
        new_grid[:, :, 1] = np.maximum(y_min, new_grid[:, :, 1])
        new_grid[:, :, 0] = np.minimum(x_max, new_grid[:, :, 0])
        new_grid[:, :, 1] = np.minimum(y_max, new_grid[:, :, 1])
        return new_grid

    def grid_to_mesh(src_grid, dst_grid):
        assert src_grid.shape == dst_grid.shape
        mesh = []
        for i in range(src_grid.shape[0] - 1):
            for j in range(src_grid.shape[1] - 1):
                src_quad = [
                    src_grid[i, j, 0],
                    src_grid[i, j, 1],
                    src_grid[i + 1, j, 0],
                    src_grid[i + 1, j, 1],
                    src_grid[i + 1, j + 1, 0],
                    src_grid[i + 1, j + 1, 1],
                    src_grid[i, j + 1, 0],
                    src_grid[i, j + 1, 1],
                ]
                dst_quad = [
                    dst_grid[i, j, 0],
                    dst_grid[i, j, 1],
                    dst_grid[i + 1, j, 0],
                    dst_grid[i + 1, j, 1],
                    dst_grid[i + 1, j + 1, 0],
                    dst_grid[i + 1, j + 1, 1],
                    dst_grid[i, j + 1, 0],
                    dst_grid[i, j + 1, 1],
                ]
                dst_rect = (dst_quad[0], dst_quad[1], dst_quad[4], dst_quad[3])
                mesh.append([dst_rect, src_quad])
        return mesh

    p1 = st.sidebar.slider("Parm1", 0, 100, 0, 1)
    image = Image.open("maarten-van-den-heuvel.jpg")

    rect = (0, 0, 1024, 576)
    # dst_grid = griddify(shape_to_rect(image.size), 4, 4)
    dst_grid = griddify(rect, 4, 4)
    src_grid = distort_grid(dst_grid, p1)
    mesh = grid_to_mesh(src_grid, dst_grid)
    im = image.transform(image.size, Image.MESH, mesh)
    st.image(im, use_column_width=True)


# Data for demo_5 derived from
# https://www.kaggle.com/rounakbanik/the-movies-dataset
DATASET_URL = (
    "https://streamlit-demo-data.s3-us-west-2.amazonaws.com/movies-revenue.csv.gz"
)


def demo_movies():
    """
    Discover the gross revenue of a movie of your liking!
    Note that the network loading and preprocessing of the data is cached
    by using Streamlit st.cache annotation.
    """
    import pandas as pd

    @st.cache
    def load_dataframe_from_url():
        return pd.read_csv(DATASET_URL).transform(
            {"title": lambda x: x, "revenue": lambda x: round(x / 1000 / 1000)}
        )

    df = load_dataframe_from_url()
    movie = st.text_input("Search movie titles")
    df = df[df.title.str.contains(movie, case=False)].sort_values(
        ascending=False, by="revenue"
    )
    st.markdown("#### Result dataframe for %d movie(s)" % df.shape[0])
    st.dataframe(df.rename(columns={"title": "Title", "revenue": "Revenue [$1M]"}))


DEMOS = OrderedDict(
    {
        "---": intro,
        "Number Generator": demo_random_numbers,
        "Bart vs Bikes": demo_bart_vs_bikes,
        "Fractals": demo_fractals,
        "Image Deformation": demo_deformation,
        "Movies": demo_movies,
    }
)


def run():
    st.title("Welcome to Streamlit!")
    st.write(
        """
        Streamlit is the best way to create bespoke apps.
        """
    )

    demo_name = st.selectbox("Choose a demo", list(DEMOS.keys()), 0)
    demo = DEMOS[demo_name]

    if demo_name != "---":
        st.markdown("## %s Demo" % demo_name)
        st.write(inspect.getdoc(demo))
        st.markdown("---")
        demo()
        st.markdown("---\n ### Code")
        sourcelines, n_lines = inspect.getsourcelines(demo)
        sourcelines = reset_indentation(remove_docstring(sourcelines))
        st.code("".join(sourcelines))
    else:
        demo()


# This function parses the lines of the function and removes the docstring
# if found.
def remove_docstring(lines):
    if len(lines) < 3 and '"""' not in lines[1]:
        return lines
    #  lines[2] is the first line of the docstring, past the inital """
    index = 2
    while '"""' not in lines[index]:
        index += 1
        # limit to ~100 lines
        if index > 100:
            return lines
    # lined[index] is the closing """
    return lines[index + 1 :]


# This function remove the common leading indentation from a code block
def reset_indentation(lines):
    if len(lines) == 0:
        return []
    spaces = len(lines[0]) - len(lines[0].lstrip())
    return [line[spaces:] if len(line) > spaces else "\n" for line in lines]


if __name__ == "__main__":
    run()
