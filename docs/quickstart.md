# Quickstart 

## Overview

This is a quick start guide. If you have a vague idea about how Vimana works and want to get started right away, continue.
For more detailed [click here](install.md)


| Library       | status        |
| ------------- |:-------------:|
| keras         | Supported     |
| pytorch       | coming soon   |
| tensorflow    | coming soon   |

## Install 

## Quick Install 

Install [Tendermint](https://tendermint.com/docs/introduction/quick-start.html#install)

Install Python 3.6+ 

### Install Vimana

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

### Local Node

Start tendermint with a simple in-process application

``` bash
tendermint init --home ".node"

tendermint node --home ".node"
```

Start the Vimana Server

```bash
python3 tmserver/start.py
```

You should be able to send requests to rendermint now. Send curl requests to `25556`


You can use the [client side Application](django.md) to do this.

Made as research internship at Univerisity of Messina by [Gautham Santhosh](gauthamzz.com) under the supervision of Prof. Francesco Long


