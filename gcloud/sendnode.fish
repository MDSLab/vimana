function sendnode
    sudo rm -rf mytestnet
    tendermint testnet
    cd mytestnet
    gcloud compute scp --recurse node0/ instance-1:~
    gcloud compute scp --recurse node1/ instance-2:~
    gcloud compute scp --recurse node2/ instance-3:~
    gcloud compute scp --recurse node3/ instance-4:~
    cd ..
end


# easily send nodes to the server 

# This creates a testnet and send all the data to all the vm instance in the gloud 