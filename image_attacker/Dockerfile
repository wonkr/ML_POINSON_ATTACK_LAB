FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip git
RUN pip3 install numpy scikit-learn imageio tensorflow matplotlib

COPY Attacker /Attacker
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]

