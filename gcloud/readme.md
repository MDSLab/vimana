# How to do google cloud 

Use this fish shell function send models to instances

```
    function sendnode
           sudo rm -rf mytestnet
           tendermint testnet
           cd mytestnet
           gcloud compute scp --recurse node0/ instance-1:~
           gcloud compute scp --recurse node1/ instance-2:~
           gcloud compute scp --recurse node2/ instance-3:~
           gcloud compute scp --recurse node3/ instance-4:~
       end
```

# In the instance on gcp 

First clone and install all the requirements to check if its working 


now you can see the `node0` in the /home/user in your gcp folder 

start the vimana server using `python vimana/tmserver/start.py`

then in a new terminal start the tendermint server using 

```
sudo tendermint node --p2p.persistent_peers "id1@ip1:26656,id2@ip2:26656,id3@ip3:26656,id4f@ip4:26656" --consensus.create_empty_blocks=false --home $NODE
```

id,ip for the respective id and ip address

the $NODE is equal to "node0", "node1", "node2", "node3"

i use fish shell, do convert to bash if you are into it. 

