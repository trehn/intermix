from asyncio import coroutine, get_event_loop
from json import loads
from queue import Empty, Queue
from os.path import dirname, join
from threading import Thread
from time import sleep, time

from aiohttp import MsgType, web
from mako.template import Template


with open(join(dirname(__file__), "intermix_client.html"), 'rb') as f:
    HTML = f.read()


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


class Client(object):
    def __init__(self, websocket, layers):
        self._js = []
        self._ws = websocket
        self.attrs = {}
        self.layers = layers

    def _dump_js(self):
        js = "".join(self._js)
        self._js = []
        return js

    def layer(self, index):
        if index < 0 or index >= self.layers:
            raise ValueError("no such layer: {}".format(index))
        return Layer(self, index)

    def raw_js(self, js):
        self._js.append(js)


class UI(object):
    def __init__(self, layers=1, state=None, title="Intermix", host="127.0.0.1", port=8080):
        self.html = Template(HTML).render(layers=layers, port=port, title=title)
        self.layers = layers
        self.url = "http://{host}:{port}/".format(host=host, port=port)

        self.state = state
        self._running = True

        self.app = web.Application()
        self.app.router.add_route('GET', "/", self._html_client)
        self.app.router.add_route('GET', "/ws", self._websocket_handler)
        self.handler = self.app.make_handler()

        self.loop = get_event_loop()
        server_init = self.loop.create_server(self.handler, host, port)
        self.server = self.loop.run_until_complete(server_init)
        self.thread = Thread(target=self._thread_body, daemon=True)
        self.thread.start()

    @coroutine
    def _html_client(self, request):
        return web.Response(body=self.html.encode('utf-8'))

    def _thread_body(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.handler.finish_connections(0.1))
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())
            self.loop.run_until_complete(self.app.finish())

    @coroutine
    def _websocket_handler(self, request):
        ws = web.WebSocketResponse()
        ws.start(request)
        client = Client(ws, self.layers)
        while self._running:
            start = time()
            msg = yield from ws.receive()
            if msg.tp in (MsgType.close, MsgType.error):
                break
            elif msg.tp != MsgType.text:
                continue
            client.attrs = loads(msg.data)
            delay = self.draw(client)
            client.raw_js("send_info();")
            ws.send_str(client._dump_js())
            sleep(max(0, delay - (time() - start)))
        return ws

    def draw(self, output):
        pass

    def stop(self):
        self._running = False
        self.loop.stop()
