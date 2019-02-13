declare -a instances=("instance1" "instance2" "instance3" "instance4")
for instance in "${instances[@]}" 
do
    ($(gcloud compute ssh $instance --command 'sudo tendermint show_node_id --home /home/gautham/node')) >> ids.txt
done
