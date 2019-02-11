# Install Instructions


## Overview

This is a detailed start guide. The address issues not in [Quickstart](quickstart.md) quide

## Install 

## Quick Install 

### Install [Tendermint](https://tendermint.com/docs/introduction/quick-start.html#install)

Install Tendermint using the go path and binary.

Alternatively 

Downlaod the binary and to move binary to `/usr/bin`, works with Tendermint `v0.28`, should be able to work with latest.

```bash
sudo apt install unzip && sudo unzip tendermint*.zip && sudo rm tendermint*.zip &&sudo  mv tendermint /usr/local/bin
```

To download pre-built binaries, see the [releases page](https://github.com/tendermint/tendermint/releases)


```
wget https://github.com/tendermint/tendermint/releases/download/v0.28.3/tendermint_0.28.3_linux_amd64.zip

unzip tendermint_0.28.3_linux_amd64.zip && rm tendermint_0.28.3_linux_amd64.zip 

mv tendermint /usr/local/bin
```

### Install Vimana

> Recommended to optionally create a virtualenv for Python 3.6+

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

Clone the repository

```bash
git clone https://github.com/MDSLab/vimana
```

go inside the folder 

```bash
cd vimana
```

Install all the requirements

``` bash
pip3 -r req.txt
```


### Local Node single node

Start tendermint with a simple in-process application

``` bash
tendermint init --home ".node"

tendermint node --home ".node"
```



```bash
tendermint node --proxy_app=tcp://localhost:26658 --consensus.create_empty_blocks=false
```

The proxy_app flag is used to set the localhost to connect to abci. In general abci starts in 26658

Tendermint sends a lot of blank nodes to remove this issue you can use create_empty_blocks flag

Start the Vimana Server

```bash
python3 tmserver/start.py
```

[![asciicast](https://asciinema.org/a/DAO2t73j6WHdDmZm8r9ZbekO1.svg)](https://asciinema.org/a/DAO2t73j6WHdDmZm8r9ZbekO1)

You bashould be able to send requests to rendermint now. Send curl requests to 25556

You can use the [client side Application](django.md) to do this.
