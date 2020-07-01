FROM alpine:3.9.2

RUN apk --no-cache add --update \
  bash \
  curl \
  graphviz \
  jq \
  python3 \
  py3-pip \
  msttcorefonts-installer \
  fontconfig && \
  update-ms-fonts && \
  fc-cache -f

COPY vpc-diagram-exporter \
  dump.py helpers.py \
  json2gv-styling.json \
  json2gv.py \
  all-to-gv.j2 \
  render-to-gv.j2 \
  requirements.txt \
  install.sh \
  /app/

WORKDIR /app
RUN ./install.sh

ENV PATH="/app:${PATH}"
VOLUME [ "/home" ]
WORKDIR "/home"
