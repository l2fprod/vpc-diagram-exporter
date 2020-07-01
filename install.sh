#!/bin/bash
curl -fsSL https://clis.ng.bluemix.net/install/linux > /tmp/bxinstall.sh && \
  sh /tmp/bxinstall.sh && \
  rm /tmp/bxinstall.sh

ibmcloud plugin install vpc-infrastructure -f -r "IBM Cloud"
ibmcloud plugin install tg -f -r "IBM Cloud"

pip3 install -r requirements.txt

curl -O https://mycatalog.mybluemix.net/generated/resources.json
mkdir -p icons

SERVICES=(
  transit.gateway
)

for service in "${SERVICES[@]}"
do
  pngIcon=$(cat resources.json | jq -r '.[] | select(.name=="'$service'") | .localPngIcon')
  pngIcon=${pngIcon/public/}
  echo "Downloading icon $pngIcon for $service"
  curl -o icons/$service.png https://mycatalog.mybluemix.net$pngIcon
done

