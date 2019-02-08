# Run Local cluster using Docker

> Running a local cluster using docker containers, requires installing docker before starting. 

## Install 

You need to have tendermint installed via binary and have Go Path set, see [Tendermint docs](https://tendermint.com/docs)

1. Build tendermint localnode in the tendermint go path.

```
 cd $GOPATH/src/github.com/tendermint/tendermint/ 
 ```

2. Build the linux 

```
make build-linux
```

copy the `docker/abci.Dockerfile` and `docker/docker-compose.yml` to `$GOPATH/src/github.com/tendermint/tendermint/`

3. Optionally run 

```
make build-docker-localnode
```

also build the abci.Dockerfile to abcinode, if not it will throw error

4. Start the nodes

```
make localnode-start
```

to stop run 
```
make localnode-stop
```


## How this works

We create 4 nodes of Tendermint and 4 nodes for the abci. They are connected via docker network. 