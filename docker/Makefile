# Build linux binary on other platforms
build-linux:
	GOOS=linux GOARCH=amd64 $(MAKE) build

build-docker-localnode:
	cd networks/local
	make
	cd -

# Run a 4-node testnet locally
localnet-start: localnet-stop
	@if ! [ -f build/node0/config/genesis.json ]; then docker run --rm -v $(CURDIR)/build:/tendermint:Z tendermint/localnode testnet --v 4 --o . --populate-persistent-peers --starting-ip-address 192.167.10.2 ; fi
	docker-compose up

# Stop testnet
localnet-stop:
	docker-compose down
