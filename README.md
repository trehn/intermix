Intermix provides a Python interface to an HTML5 canvas. It's meant to give command line applications a pixel-based output channel.

Just draw using Intermix' own simplified API or use the full power of the JavaScript interface on up to 8 layers of HTML5 canvases.

Requires Python 3.3 or higher.

Usage
-----

```python
from intermix.ui import UI


class MyUI(UI):
    def draw(self, client):
        with client.layer(0) as layer:
            layer.clear()
            layer.text(50, 50, self.state['text'])
        return 1  # wait 1s before drawing next frame
```

```python
>>> ui = MyUI(state={'text': "initial text"})  # now served on a background thread
>>> print(ui.url)
http://127.0.0.1:8080
>>> ui.state['text'] = "updated live"
>>>
```

See `demo.py` for a more comprehensive example.
