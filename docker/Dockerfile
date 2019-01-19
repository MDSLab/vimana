FROM gw000/keras:2.1.4-py3-tf-cpu

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
