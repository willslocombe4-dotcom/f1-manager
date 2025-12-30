# F1 Designer Mobile Chat

A Progressive Web App (PWA) for chatting with the f1-designer agent from your phone. Brainstorm game ideas anywhere and save them to your backlog.

## Features

- **Mobile-first chat UI** - Dark theme, touch-friendly
- **f1-designer integration** - Direct connection to your brainstorming agent
- **Session management** - Resume previous brainstorms
- **Save to backlog** - One tap to save ideas to your feature backlog
- **PWA installable** - Add to home screen for native app feel
- **Remote access** - Chat from anywhere via Tailscale

## Quick Start

### 1. Set Up Tailscale (One-time)

Tailscale creates a secure private network between your devices.

1. Install Tailscale on your PC: https://tailscale.com/download
2. Install Tailscale on your phone (iOS App Store / Google Play)
3. Sign in to the same account on both devices
4. Note your PC's Tailscale IP (looks like `100.x.x.x`)

### 2. Start OpenCode Server

On your PC, run:

```bash
opencode serve --hostname 0.0.0.0 --port 4096
```

This starts the OpenCode server and makes it accessible on your network.

**Tip:** Add this to a script for easy startup:
```bash
# start-server.sh / start-server.bat
cd "D:/game dev/f1_manager"
opencode serve --hostname 0.0.0.0 --port 4096
```

### 3. Serve the PWA

The PWA needs to be served via HTTP (not opened as a local file). Options:

**Option A: Python (simplest)**
```bash
cd "D:/game dev/f1_manager/tools/f1-mobile-chat"
python -m http.server 8080
```

**Option B: Node.js**
```bash
npx serve "D:/game dev/f1_manager/tools/f1-mobile-chat" -p 8080
```

**Option C: VS Code Live Server extension**
- Right-click `index.html` → "Open with Live Server"

### 4. Connect from Your Phone

1. Open your phone's browser
2. Go to: `http://[YOUR-TAILSCALE-IP]:8080`
   - Example: `http://100.64.0.1:8080`
3. Enter your OpenCode server URL: `http://[YOUR-TAILSCALE-IP]:4096`
4. Tap **Connect**

### 5. Install as App (Optional)

**iOS Safari:**
1. Tap the Share button
2. Tap "Add to Home Screen"
3. Tap "Add"

**Android Chrome:**
1. Tap the menu (⋮)
2. Tap "Add to Home Screen"
3. Tap "Add"

## Usage

### Chatting
- Type your game ideas in the input field
- Press Enter or tap Send
- f1-designer will respond with refined ideas

### Saving Ideas
- When you have a good idea, tap the **Save** icon (💾) in the header
- The last assistant response is saved to your backlog
- Ideas are appended to `.opencode/context/f1-designer-context.md`

### Sessions
- Each brainstorm is a separate session
- Tap **+** to start a new session
- Tap a session to resume it

## Troubleshooting

### "Connection failed"
1. Make sure OpenCode server is running (`opencode serve`)
2. Check Tailscale is connected on both devices
3. Verify the IP address and port are correct
4. Try pinging your PC's Tailscale IP from your phone

### Messages not appearing
- SSE (Server-Sent Events) requires a stable connection
- Check your WiFi/cellular connection
- Refresh the page if needed

### Save to backlog fails
- Ensure the `.opencode/context/` folder exists
- Check the server has write permissions

## Architecture

```
Phone (PWA)                     PC
┌─────────────┐           ┌──────────────┐
│ index.html  │───HTTP───►│ opencode     │
│ app.js      │    via    │ serve :4096  │
│ styles.css  │ Tailscale │              │
└─────────────┘           └──────────────┘
```

- **Frontend**: Vanilla JS + CSS (no build step)
- **Backend**: OpenCode Server API
- **Connection**: HTTP over Tailscale VPN
- **Real-time**: Server-Sent Events (SSE)

## File Structure

```
tools/f1-mobile-chat/
├── index.html       # Main page
├── app.js           # Chat logic + OpenCode SDK integration
├── styles.css       # Mobile-first dark theme
├── manifest.json    # PWA manifest
├── service-worker.js # Offline caching
└── README.md        # This file
```

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `GET /global/health` | Check connection |
| `GET /session` | List sessions |
| `POST /session` | Create session |
| `POST /session/:id/prompt_async` | Send message (async) |
| `GET /session/:id/message` | Get messages |
| `POST /session/:id/shell` | Save to backlog |
| `GET /event` | Real-time updates (SSE) |

## Security Notes

- Tailscale encrypts all traffic
- The PWA only connects to your specified server
- No data is sent to external services
- Session data stored locally in browser

## Customization

### Change theme colors
Edit CSS variables in `styles.css`:
```css
:root {
    --accent: #e10600;      /* F1 red */
    --bg-primary: #0d1117;  /* Dark background */
    /* ... */
}
```

### Target different agent
Edit `CONFIG.AGENT` in `app.js`:
```javascript
const CONFIG = {
    AGENT: 'f1-designer',  // Change to any agent name
    // ...
};
```

## Future Ideas

- [ ] Voice input for hands-free brainstorming
- [ ] Image sharing for visual ideas
- [ ] Offline message queue
- [ ] Push notifications for responses
- [ ] Multiple agent selection

---

Built for the F1 Manager project.
