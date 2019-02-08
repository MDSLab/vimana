# Quickstart 

## Overview

This is a quick start guide. If you have a vague idea about how Vimana works and want to get started right away, continue.
For more detailed [click here](install.md)

## Install 

## Quick Install 

### Install [Tendermint](https://tendermint.com/docs/introduction/quick-start.html#install)

> Recommended to move binary to /usr/bin, works with Tendermint v0.28, should be able to work with latest.

To download pre-built binaries, see the [releases page](https://github.com/tendermint/tendermint/releases)

Alternatively 

```
wget https://github.com/tendermint/tendermint/releases/download/v0.28.3/tendermint_0.28.3_linux_amd64.zip

unzip tendermint_0.28.3_linux_amd64.zip && rm tendermint_0.28.3_linux_amd64.zip 

mv tendermint /usr/local/bin
```

### Install Vimana

> Recommended to optionally create a virtualenv for Python 3.6+

```sh
virtualenv -p python3 venv
source venv/bin/activate
```

Clone the repository

```sh
git clone https://github.com/MDSLab/vimana
```

go inside the folder 

```sh
cd vimana
```

Install all the requirements

``` sh
pip3 -r req.txt
```


### Local Node

Start tendermint with a simple in-process application

``` sh
tendermint init --home ".node"

tendermint node --home ".node"
```

Start the Vimana Server

```sh
python3 tmserver/start.py
```

You should be able to send requests to rendermint now. Send curl requests to 25556

You can use the client side Django Application to test the network 

## FAQ

### Error with ethereum utils 

This is a quick fix for the bug

```
pip uninstall ethereum-utils eth-utils 
pip install eth-utils
```