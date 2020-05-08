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

## Syncing

```python
from matplotvideo import attach_video_player_to_figure
import matplotlib.pyplot as plt

 # (timestamp, value) pairs
fancy_data = [
  (0, 1), 
  (0.5, 2),
  (1.0, 3),
  (1.5, 2.5),
  (2, 1),
  (2.5, 4),
  # ....
  (200, 12)
]



def on_frame(video_timestamp, line):
    timestamps, y = zip(*[data_point for data_point in fancy_data if abs(data_point[0] - video_timestamp) < 10])
    x = [timestamp - video_timestamp for timestamp in timestamps]
    line.set_data(x, y)
    line.axes.relim()
    line.axes.autoscale_view()
    line.axes.figure.canvas.draw()

def main():
    fig, ax = plt.subplots()
    plt.xlim(-10, 10)
    plt.axvline(x=0, color='k', linestyle='--')
    
    line, = ax.plot([], [], color='blue')

    attach_video_player_to_figure(fig, "your-video.mp4", on_frame, line=line)

    plt.show()

main()
```
