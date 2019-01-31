FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3-pip libssl-dev 

# install dependencies from debian packages
RUN apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    python3-matplotlib \
    python3-pillow \
    python3-pip\
    python3-dev \ 
    git

# install dependencies from python packages
RUN pip3 --no-cache-dir install \
    pandas \
    scikit-learn \
    statsmodels 

RUN git clone https://github.com/gauthamzz/vimana 

RUN cd vimana && git checkout analytics_mnist

RUN cd vimana && \
    pip3 install -r req.txt
# RUN git clone https://github.com/davebryson/py-abci
# EXPOSE 

# RUN pip3 install abci
# RUN -d python3 py-abci/examples/counter.py
# CMD ["python3", "py-abci/examples/counter.py"]

# RUN apt-get install -y unzip && apt-get install -y wget && wget https://github.com/tendermint/tendermint/releases/download/v0.27.3/tendermint_0.27.3_linux_amd64.zip
# RUN unzip tendermint_0.27.3_linux_amd64.zip && rm tendermint_0.27.3_linux_amd64.zip && mv tendermint /usr/local/bin

# RUN tendermint init

EXPOSE 26656 26657 8000 26658

# VOLUME [ /tendermint ]
# WORKDIR /tendermint

# CMD ["python3", "~/vimana/tendermint/app.py"]
# docker run -d -p 0.0.0.0:26656-26657:26656-26657  w tendermint node --consensus.create_empty_blocks=false 
# docker exec -it agitated_swartz   /bin/bash
# cd vimana/tendermint
# python app.py



# docker build -t abci1 -f abci.Dockerfile .
# docker run -it -p 0.0.0.0:26665:26658 abci1 python3 vimana/tendermint/app.py


# tendermint node --proxy_app=tcp://localhost:26658 --home "./tendermint/node0" --consensus.create_empty_blocks=false