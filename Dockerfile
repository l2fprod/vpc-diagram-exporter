FROM alpine:3.9.2

RUN apk --no-cache add --update \
  curl \
  graphviz \
  python3 \
  py3-pip \
  msttcorefonts-installer \
  fontconfig && \
  update-ms-fonts && \
  fc-cache -f

RUN curl -fsSL https://clis.ng.bluemix.net/install/linux > /tmp/bxinstall.sh && \
  sh /tmp/bxinstall.sh && \
  rm /tmp/bxinstall.sh

RUN ibmcloud plugin install infrastructure-service -f -r "IBM Cloud"

COPY vpc-diagram-exporter dump.py helpers.py json2gv-styling.json json2gv.py render-to-gv.j2 requirements.txt /app/
RUN cd /app && pip3 install -r requirements.txt

ENV PATH="/app:${PATH}"

VOLUME [ "/home" ]
WORKDIR "/home"
