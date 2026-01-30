FROM lscr.io/linuxserver/webtop:ubuntu-kde

RUN apt-get update && apt-get install -y \
    wget unzip lib32gcc-s1 libsdl2-2.0-0 default-jre \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/itsdarklikehell/showet.git /app

WORKDIR /app
# COPY . /app

# RUN install.sh --update
# RUN install.sh --install-showet
# RUN install.sh --install-emulators
# RUN debuild -us -uc -b

WORKDIR /config

RUN chown -R abc:abc /config /showet

EXPOSE 3000 3001 16261