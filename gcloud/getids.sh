gcloud compute ssh instance1 --command 'sudo tendermint show_node_id --home /home/gautham/node0' >> ids.txt
gcloud compute ssh instance2 --command 'sudo tendermint show_node_id --home /home/gautham/node1' >> ids.txt
gcloud compute ssh instance3 --command 'sudo tendermint show_node_id --home /home/gautham/node2' >> ids.txt
gcloud compute ssh instance4 --command 'sudo tendermint show_node_id --home /home/gautham/node3' >> ids.txt
