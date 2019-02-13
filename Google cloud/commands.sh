# NODE="node0"
# NODE="node1"
# NODE="node2"
# NODE="node3"

# cd /home/gautham
# sudo tendermint show_node_id --home $NODE

# function sendcommands
#       gcloud compute scp --recurse commands.sh instance1:~
#       gcloud compute scp --recurse commands.sh instance2:~
#       gcloud compute scp --recurse commands.sh instance3:~
#       gcloud compute scp --recurse commands.sh instance4:~
#   end

id1=d7c0f625ab03e00f8721ac0b732d157079a516e1
id2=a7dc8aac74719d0932a7e1b088676840404f8fbe
id3=fbc1b6c4854c941b9a5f1f740109b72662e10257
id4=904063ddc67bf72f85ba8bbaba17c8bd326b255b
IP1=35.246.37.44
IP2=104.196.99.158
IP3=35.243.82.202
IP4=35.201.7.200

ip1=$IP1:26656
ip2=$IP3:26656
ip3=$IP3:26656
ip4=$IP4:26656

alias tmrun='
sudo tendermint unsafe_reset_all --home node
sudo tendermint node --p2p.persistent_peers "$id1@$ip1,$id2@$ip2,$id3@$ip3,$id4@$ip4" --consensus.create_empty_blocks=false --home $NODE
'

# alias vmm='

# if [ ! -d "models" ]; then
#   sudo unzip /home/gautham/models.zip -d /home/gautham/models/ 
# fi
# MODEL=$1
# sudo cp models/$MODEL /home/gautham/vimana/tmserver/model.h5
# python3 /home/gautham/vimana/tmserver/start.py
# '

cd /home/gautham