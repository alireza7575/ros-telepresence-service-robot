# Audio Prototype

Socket-based audio streaming experiment.

- `server.py` listens on TCP port `4000` and broadcasts audio packets between connected clients.
- `client.py` connects to the robot/server IP, records microphone audio, sends it to the server, and plays received audio.

Run the server:

```bash
python apps/audio/server.py
```

Run the client:

```bash
python apps/audio/client.py <robot-ip>
```
