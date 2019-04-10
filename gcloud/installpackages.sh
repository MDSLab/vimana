# written in bash

declare -a instances=("instance5" "instance6" )

declare RESULT=$(bash create.sh)

echo "The Ip are" $RESULT > ip.txt

echo "installing abci"
for instance in "${instances[@]}" 
do
    gcloud compute ssh $instance --command 'sudo apt -y install gcc python3-dev tmux'
    gcloud compute ssh $instance --command 'wget https://bootstrap.pypa.io/get-pip.py'
    gcloud compute ssh $instance --command 'sudo python3 get-pip.py'
    gcloud compute ssh $instance --command 'git clone https://github.com/mdslab/vimana'
    gcloud compute ssh $instance --command 'pip3 install -r vimana/req.txt --user'
    gcloud compute ssh $instance --command 'pip uninstall -y ethereum-utils eth-utils '
    gcloud compute ssh $instance --command 'pip install eth-utils --user'
done

echo "installing tendermint"

for instance in "${instances[@]}" 
do
    gcloud compute ssh $instance --command 'sudo apt -y install unzip'
    gcloud compute ssh $instance --command 'sudo wget https://github.com/tendermint/tendermint/releases/download/v0.30.0/tendermint_0.30.0_linux_amd64.zip'
    gcloud compute ssh $instance --command 'sudo unzip tendermint*linux_amd64.zip && sudo rm tendermint*linux_amd64.zip && sudo mv tendermint /usr/local/bin'
done


# scp the models and get model ids

# gcloud compute ssh $instance --command ''