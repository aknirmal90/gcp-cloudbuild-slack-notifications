# Overview

This application uses the following GCP components to deploy a slack notifier for your cloud build jobs
1. Pub / Sub Topics
2. Cloud Functions using Python Framework

![alt text](assets/image.png?raw=true)

## 1. Retrieve Slack Webhook URL
Before you start, ensure that you have a slack webhook available. The cloud function which will be deployed by this repository will send POST requests to the slack webhook you configure within `main.py`

For more information on how to retrieve the slack webhook, visit this <a href="https://api.slack.com/messaging/webhooks">link</a>

## 2. Enable GCP APIs 
Your application will use Cloud Functions, Pub/Sub and Cloud Build.
Ensure that you turn on APIs for these services <a href="https://console.cloud.google.com/flows/enableapi?apiid=pubsub.googleapis.com,cloudfunctions,cloudbuild.googleapis.com&redirect=https://cloud.google.com/functions/quickstart">here</a>.


## 3. Create a Pub/Sub topic which can receive notifications from Cloud Build
```
gcloud pubsub topics create cloud-builds
```
Use `cloud-builds` exactly as topic name as it seems to be a default provided by GCP
https://cloud.google.com/build/docs/subscribe-build-notifications

## 4. Create a service account
This service account will encapsulate the permissions your cloud functions app will require.
Give this service account the following permissions
- Pub/Sub Subscriber 
- Cloud Functions Invoker

Once completed, keep track of the email assigned to this service account, it will have a structure similar to 
`cloudfunctions-slack-notifier@<projectid>.iam.gserviceaccount.com`

## 5. Deploy the cloud function
Update the webhook url on `main.py` to reflect the URL you would like to send notifications to and run
```
gcloud functions deploy cloud_build_slack_notification \
    --runtime python37 \
    --region us-central1 \
    --entry-point cloud_build_slack_notification \
    --trigger-topic cloud-builds \
    --allow-unauthenticated \
    --service-account cloudfunctions-slack-notifier@<projectid>.iam.gserviceaccount.com
```

# References
1. <a href="https://cloud.google.com/build/docs/configuring-notifications/configure-slack">Configuring Slack notifications</a> 
2. <a href="https://cloud.google.com/build/docs/subscribe-build-notifications">Subscribing to build notifications</a>
3. <a href="https://api.slack.com/messaging/webhooks">Getting Started with Slack Webhooks</a>
4. <a href="https://github.com/GoogleCloudPlatform/functions-framework-python">Python Functions Framework</a>
5. <a href="https://cloud.google.com/build/docs/api/reference/rest/v1/projects.builds">Cloud Build Notifications Schema</a>