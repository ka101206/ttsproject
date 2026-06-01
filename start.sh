#!/bin/bash
set -e

# Start Xvfb (Virtual Screen)
# Resolution: 1024x768 with 24-bit color
rm -f /tmp/.X99-lock
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99

# Wait for Xvfb to be ready
sleep 2

# Start Fluxbox (Window Manager) for window borders and titlebars
fluxbox -display :99 &

# Start x11vnc (VNC Server attached to the virtual screen)
x11vnc -display :99 -nopw -listen localhost -xkb -forever &

# Replace vnc.html with our wrapper page that auto-scales and includes IME input
cp /app/polyglot_vnc.html /usr/share/novnc/vnc.html

# Start noVNC (HTML5 VNC Client on internal port 6080)
/usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &

# Start Nginx (Reverse Proxy on port 8080)
cp /app/nginx.conf /etc/nginx/nginx.conf
nginx

echo "=========================================================="
echo "🌐 GUI is ready! Open http://localhost:8080/vnc.html?autoconnect=true&resize=scale in your browser."
echo "=========================================================="



# Start the Python Application
python main.py
