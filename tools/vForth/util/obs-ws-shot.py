#!/usr/bin/env python3
"""obs-ws-shot.py -- PNG of an OBS source through the obs-websocket v5 server.

OBS shows the video output of the real ZX Spectrum Next (HDMI capture card):
this saves exactly what the source renders, at native resolution, with no
window title, no menus and no clipping, even when OBS is minimised.
Fallback with the server off: util/obs-shot.ps1 (capture of the window).

Usage:
    python util/obs-ws-shot.py                 current program scene -> PNG
    python util/obs-ws-shot.py -o shot.png     choose the output file
    python util/obs-ws-shot.py -s "HDMI"       a given source or scene
    python util/obs-ws-shot.py -l              list scenes and their sources

Server: OBS > Tools > WebSocket Server Settings (default port 4455).
Password: read from %USERPROFILE%\\.obs-ws-password (outside the repo,
one per workstation); with authentication disabled the file is not needed.

Standard library only (no websocket package): a minimal RFC 6455 client.
Prints the path of the saved PNG.  Exit code: 0 ok, 1 error.
"""

import argparse
import base64
import hashlib
import json
import os
import socket
import struct
import sys
import tempfile

PW_FILE = os.path.join(os.path.expanduser('~'), '.obs-ws-password')


class WS:
    """Just enough WebSocket client for obs-websocket: text frames only."""

    def __init__(self, host, port, timeout=10):
        self.s = socket.create_connection((host, port), timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        req = ('GET / HTTP/1.1\r\n'
               f'Host: {host}:{port}\r\n'
               'Upgrade: websocket\r\nConnection: Upgrade\r\n'
               f'Sec-WebSocket-Key: {key}\r\n'
               'Sec-WebSocket-Version: 13\r\n'
               'Sec-WebSocket-Protocol: obswebsocket.json\r\n\r\n')
        self.s.sendall(req.encode())
        head = b''
        while b'\r\n\r\n' not in head:
            chunk = self.s.recv(1024)
            if not chunk:
                raise ConnectionError('connection closed during handshake')
            head += chunk
        head, self.buf = head.split(b'\r\n\r\n', 1)
        if b' 101 ' not in head.split(b'\r\n', 1)[0]:
            raise ConnectionError(head.split(b'\r\n', 1)[0].decode())

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.s.recv(65536)
            if not chunk:
                raise ConnectionError('connection closed by OBS')
            self.buf += chunk
        data, self.buf = self.buf[:n], self.buf[n:]
        return data

    def send(self, obj):
        data = json.dumps(obj).encode()
        n = len(data)
        if n < 126:
            hdr = struct.pack('!BB', 0x81, 0x80 | n)
        elif n < 65536:
            hdr = struct.pack('!BBH', 0x81, 0x80 | 126, n)
        else:
            hdr = struct.pack('!BBQ', 0x81, 0x80 | 127, n)
        mask = os.urandom(4)
        body = bytes(b ^ mask[i & 3] for i, b in enumerate(data))
        self.s.sendall(hdr + mask + body)

    def recv(self):
        msg = b''
        while True:
            b0, b1 = self._read(2)
            n = b1 & 0x7F
            if n == 126:
                n = struct.unpack('!H', self._read(2))[0]
            elif n == 127:
                n = struct.unpack('!Q', self._read(8))[0]
            mask = self._read(4) if b1 & 0x80 else None
            data = self._read(n)
            if mask:
                data = bytes(b ^ mask[i & 3] for i, b in enumerate(data))
            op = b0 & 0x0F
            if op == 8:
                code = struct.unpack('!H', data[:2])[0] if len(data) >= 2 else 0
                raise ConnectionError(f'closed by OBS: {code} {data[2:].decode(errors="replace")}')
            if op == 9:                                  # ping -> pong
                mask = os.urandom(4)
                self.s.sendall(struct.pack('!BB', 0x8A, 0x80 | len(data)) + mask
                               + bytes(b ^ mask[i & 3] for i, b in enumerate(data)))
                continue
            if op in (0, 1, 2):
                msg += data
                if b0 & 0x80:                            # FIN
                    return json.loads(msg)


class OBS:
    def __init__(self, host, port):
        self.ws = WS(host, port)
        hello = self.ws.recv()['d']
        ident = {'rpcVersion': 1, 'eventSubscriptions': 0}
        auth = hello.get('authentication')
        if auth:
            try:
                with open(PW_FILE, encoding='utf-8-sig') as f:
                    pw = f.read().strip()
            except OSError:
                raise SystemExit(f'OBS asks for a password: {PW_FILE} not found')
            secret = base64.b64encode(
                hashlib.sha256((pw + auth['salt']).encode()).digest())
            ident['authentication'] = base64.b64encode(
                hashlib.sha256(secret + auth['challenge'].encode()).digest()).decode()
        self.ws.send({'op': 1, 'd': ident})
        self.ws.recv()                                   # op 2 Identified
        self.n = 0

    def call(self, rtype, **data):
        self.n += 1
        rid = str(self.n)
        self.ws.send({'op': 6, 'd': {'requestType': rtype, 'requestId': rid,
                                     'requestData': data}})
        while True:
            m = self.ws.recv()
            if m.get('op') == 7 and m['d'].get('requestId') == rid:
                st = m['d']['requestStatus']
                if not st['result']:
                    raise SystemExit(f'{rtype}: {st.get("code")} {st.get("comment", "")}')
                return m['d'].get('responseData', {})


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('-o', '--out', default=os.path.join(tempfile.gettempdir(), 'obs-shot.png'))
    ap.add_argument('-s', '--source', help='source or scene name (default: current program scene)')
    ap.add_argument('-l', '--list', action='store_true', help='list scenes and sources')
    ap.add_argument('--host', default='localhost')
    ap.add_argument('--port', type=int, default=4455)
    a = ap.parse_args()
    try:
        obs = OBS(a.host, a.port)
    except OSError as e:
        print(f'cannot reach obs-websocket on {a.host}:{a.port}: {e}', file=sys.stderr)
        return 1
    if a.list:
        cur = obs.call('GetCurrentProgramScene')['currentProgramSceneName']
        for sc in obs.call('GetSceneList')['scenes']:
            name = sc['sceneName']
            print(('* ' if name == cur else '  ') + name)
            for it in obs.call('GetSceneItemList', sceneName=name)['sceneItems']:
                print(f'      {it["sourceName"]}  ({it.get("inputKind") or "scene"})'
                      + ('' if it.get('sceneItemEnabled', True) else '  [hidden]'))
        return 0
    src = a.source or obs.call('GetCurrentProgramScene')['currentProgramSceneName']
    out = os.path.abspath(a.out)
    obs.call('SaveSourceScreenshot', sourceName=src, imageFormat='png',
             imageFilePath=out)
    print(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
