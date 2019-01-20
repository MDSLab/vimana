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

RUN cd vimana && \
    pip3 install -r req.txt
# RUN git clone https://github.com/davebryson/py-abci
EXPOSE 8000 26658

# RUN pip3 install abci
# RUN -d python3 py-abci/examples/counter.py
# CMD ["python3", "py-abci/examples/counter.py"]

CMD ["python3", "vimana/tendermint/app.py"]
# docker run -d -p 0.0.0.0:8003:8000 q python3 vimana/manage.py runserver 0.0.0.0:8000