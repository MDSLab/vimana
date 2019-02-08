# Detailed Install Instructions


## Overview

This is a detailed start guide. The address issues not in [Quickstart](quickstart.md) quide

## Install 

## Quick Install 

### Install [Tendermint](https://tendermint.com/docs/introduction/quick-start.html#install)

Install Tendermint using the go path and binary.


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


### Local Node single node

Start tendermint with a simple in-process application

``` sh
tendermint init --home ".node"

tendermint node --home ".node"
```



```sh
tendermint node --proxy_app=tcp://localhost:26658 --consensus.create_empty_blocks=false
```

The proxy_app flag is used to set the localhost to connect to abci. In general abci starts in 26658

Tendermint sends a lot of blank nodes to remove this issue you can use create_empty_blocks flag

Start the Vimana Server

```sh
python3 tmserver/start.py
```

You should be able to send requests to rendermint now. Send curl requests to 25556

You can use the client side Django Application to do this.
## FAQ

### Error with ethereum utils 

This is a quick fix for the bug

```
pip uninstall ethereum-utils eth-utils 
pip install eth-utils
```