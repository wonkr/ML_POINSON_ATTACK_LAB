#!/bin/bash

cd simple_ml_server && ./run.sh&
cd /crawler && ./crawl_train_data_from_internet.py&
cd /

echo "ready! run 'docker exec -it $HOSTNAME /bin/zsh' to attach to this node" >&2
for f in /proc/sys/net/ipv4/conf/*/rp_filter; do echo 0 > "$f"; done
tail -f /dev/null
