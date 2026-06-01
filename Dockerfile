FROM python:3.11-slim

# Prevent interactive prompts during apt installations
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies:
# 1. build-essential & cmake for compiling pyopenjtalk
# 2. python3-tk for Tkinter
# 3. Audio tools: portaudio19-dev, libasound2
# 4. Virtual Desktop tools: xvfb, fluxbox, x11vnc, novnc, websockify
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-tk \
    portaudio19-dev \
    libasound2 \
    xvfb \
    fluxbox \
    x11vnc \
    novnc \
    websockify \
    fcitx \
    fcitx-anthy \
    fcitx-hangul \
    fcitx-googlepinyin \
    dbus-x11 \
    fonts-noto-cjk \
    locales \
    nginx \
    flac \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /app

# Copy requirements and install dependencies
# Compiling pyopenjtalk during this step will take a minute or two
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (heavy files are ignored via .dockerignore)
COPY . .

# Ensure the start script is executable
RUN chmod +x start.sh

# Expose the noVNC web port
EXPOSE 8080

# Run the virtual desktop and app
CMD ["/bin/bash", "./start.sh"]
