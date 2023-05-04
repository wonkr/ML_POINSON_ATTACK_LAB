FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN  apt-get update && apt-get install -y --no-install-recommends python3 python3-pip git
RUN pip3 install numpy scikit-learn imageio tensorflow matplotlib
RUN pip3 install flask
RUN pip3 install bs4

COPY simple_ml_server /simple_ml_server
COPY crawler /crawler
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]

