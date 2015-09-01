class Layer(object):
    def __init__(self, client, index):
        self.client = client
        self.index = index

    def __enter__(self):
        self._js = []
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client._js.extend(self._js)

    def clear(self, layer=0):
        self.clear_rect(0, 0, self.client.attrs['width'], self.client.attrs['height'])

    def clear_rect(self, x, y, width, height, layer=0):
        self._js.append("ctx_2d[{layer}].clearRect({x},{y},{width},{height});".format(
            layer=layer,
            x=x,
            y=y,
            height=height,
            width=width,
        ))

    def fill(self, color="#000000", layer=0):
        self.fill_rect(
            0,
            0,
            self.client.attrs['width'],
            self.client.attrs['height'],
            color=color,
            layer=0,
        )

    def fill_rect(self, x, y, width, height, color="#000000", layer=0):
        self._js.append("ctx_2d[{layer}].fillStyle=\"{color}\";".format(
            color=color,
            layer=layer,
        ))
        self._js.append("ctx_2d[{layer}].fillRect({x},{y},{width},{height});".format(
            layer=layer,
            x=x,
            y=y,
            height=height,
            width=width,
        ))

    def line(self, from_x, from_y, to_x, to_y, color="#000000", layer=0):
        self._js.append("""
            ctx_2d[{layer}].beginPath();
            ctx_2d[{layer}].fillStyle="{color}";
            ctx_2d[{layer}].moveTo({from_x}, {from_y});
            ctx_2d[{layer}].lineTo({to_x}, {to_y});
            ctx_2d[{layer}].stroke();
        """.format(
            color=color,
            from_x=from_x,
            from_y=from_y,
            layer=layer,
            to_x=to_x,
            to_y=to_y,
        ))

    def text(self, x, y, text, color="#000000", font="Arial", font_size="30px", layer=0):
        self._js.append("""
            ctx_2d[{layer}].font = "{font_size} {font}";
            ctx_2d[{layer}].fillStyle="{color}";
            ctx_2d[{layer}].fillText("{text}",{x},{y});
        """.format(
            color=color,
            font=font,
            font_size=font_size,
            layer=layer,
            text=text,
            x=x,
            y=y,
        ))
