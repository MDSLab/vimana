FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y unzip && apt-get install -y wget && wget https://github.com/tendermint/tendermint/releases/download/v0.27.3/tendermint_0.27.3_linux_amd64.zip
RUN unzip tendermint_0.27.3_linux_amd64.zip && rm tendermint_0.27.3_linux_amd64.zip && mv tendermint /usr/local/bin
# RUN apt-get install -y ufw && apt-get install -y sudo && apt-get install vim && useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo 
# RUN  echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN tendermint init

CMD ["tendermint", "node"]