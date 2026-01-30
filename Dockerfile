FROM lscr.io/linuxserver/webtop:ubuntu-kde

RUN apt-get update && apt-get install -y \
    wget unzip lib32gcc-s1 libsdl2-2.0-0 default-jre \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/itsdarklikehell/showet.git /showet

WORKDIR /showet
# COPY . /showet

# RUN cd /showet && install.sh --update
# RUN cd /showet && install.sh --install-showet
# RUN cd /showet && install.sh --install-emulators
# RUN cd /showet && debuild -us -uc -b

WORKDIR /config

RUN chown -R abc:abc /config /showet

EXPOSE 3000 3001 16261