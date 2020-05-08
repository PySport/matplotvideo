# matplotvideo - syncing video and matplotlib

[![PyPI Latest Release](https://img.shields.io/pypi/v/matplotvideo.svg)](https://pypi.org/project/matplotvideo/)
[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-PySport-orange.svg?style=flat&colorA=104467&colorB=007D8A)](https://pysport.org)
--------
## What is it?

**matplotvideo** is a Python package providing an easy way to sync matplotlib plots to video. 

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/PySport/matplotvideo

Installers for the latest released version are available at the [Python
package index](https://pypi.org/project/matplotvideo).

```sh
# or PyPI
pip install matplotvideo
```

The package requires `cv2` to be installed. When you don't have it installed yet, check out [opencv-python](https://pypi.org/project/opencv-python/).

## Video player controls:
![example](examples/example.gif)
- **'a'** 1 frame back
- **'d'** 1 frame forward
- **space** toggle paused / play
- **playback speed** can be changed with the slider

## Usage
Import `attach_video_player_to_figure` and attach to matplotlib figure. You can pass additional keyword arguments to `attach_video_player_to_figure` that are passed to the `on_frame` callback on each invocation. 

```python
from matplotvideo import attach_video_player_to_figure
import matplotlib.pyplot as plt

# (timestamp, value) pairs

# sample: big bunny scene cuts
fancy_data = [
    (0, 1),
    (11.875, 1),
    (11.917, 2),
    (15.75, 2),
    (15.792, 3),
    (23.042, 3),
    (23.083, 4),
    (47.708, 4),
    (47.75, 5),
    (56.083, 5),
    (56.125, 6),
    (60, 6)
]


def on_frame(video_timestamp, line):
    timestamps, y = zip(*[data_point for data_point in fancy_data])
    x = [timestamp - video_timestamp for timestamp in timestamps]

    line.set_data(x, y)
    line.axes.relim()
    line.axes.autoscale_view()
    line.axes.figure.canvas.draw()


def main():
    fig, ax = plt.subplots()
    plt.xlim(-15, 15)
    plt.axvline(x=0, color='k', linestyle='--')

    line, = ax.plot([], [], color='blue')

    attach_video_player_to_figure(fig, "BigBuckBunny.mp4", on_frame, line=line)

    plt.show()


main()
```
