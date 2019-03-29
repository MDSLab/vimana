ZONE1='europe-west2-c'
ZONE2='us-east1-b'
ZONE3='asia-northeast1-b'
ZONE4='australia-southeast1-b'

echo "creating instance at" $ZONE1 $ZONE2 $ZONE3 $ZONE4

gcloud compute instances create instance1 --source-instance-template instance-template-1	 --zone=$ZONE1
gcloud compute instances create instance2 --source-instance-template instance-template-1	 --zone=$ZONE2
gcloud compute instances create instance3 --source-instance-template instance-template-1	 --zone=$ZONE3
gcloud compute instances create instance4 --source-instance-template instance-template-1	 --zone=$ZONE4


echo "Instance Created"
