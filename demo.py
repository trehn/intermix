import sys
from time import sleep

from intermix.ui import UI


class MyUI(UI):
    def draw(self, client):
        with client.layer(0) as layer:
            layer.fill(color="#88FF88")
            layer.line(0, 0, client.attrs['width'], client.attrs['height'])

        with client.layer(1) as layer:
            layer.clear()
            layer.text(20, 50, str(self.state['i']))

        return 1  # wait 1s before drawing next frame


if __name__ == '__main__':
    # immediately starts web server
    ui = MyUI(layers=2, state={'i': 0}, host="0.0.0.0", port=8080)
    print(ui.url)
    try:
        while True:
            ui.state['i'] += 1
            sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
