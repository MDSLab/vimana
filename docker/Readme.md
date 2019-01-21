# To run locally 

1. Build tendermint localnode in the tendermint go path.

` cd $GOPATH/src/github.com/tendermint/tendermint/ `

2. Build the linux 

` make build-linux`

3. Optionally run 

`make build-docker-localnode`

also build the abci.Dockerfile to abcinode, if not it will throw error

4. Start the nodes

`make localnode-start`

to stop run `make localnode-stop`