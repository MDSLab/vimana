 function sendmodels 
      gcloud compute scp --recurse models.zip instance-1:~
      gcloud compute scp --recurse models.zip instance-2:~
      gcloud compute scp --recurse models.zip instance-3:~
      gcloud compute scp --recurse models.zip instance-4:~
  end
