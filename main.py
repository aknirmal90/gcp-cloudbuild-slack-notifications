import json
import base64
import requests


webhook_url = "XXXXXXXXXXXXXXXXX"


class BuildStatus:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"
    QUEUED = "QUEUED"
    WORKING = "WORKING"


def cloud_build_slack_notification(event, context):
    if not "data" in event and not event["data"]:
        raise Exception("Message Body Is Required")

    data = json.loads(base64.b64decode(event['data']).decode('utf-8'))

    project_id = data["projectId"]
    logs_url = data["logUrl"]
    trigger_name = data["substitutions"]["TRIGGER_NAME"]
    branch_name = data["substitutions"]["BRANCH_NAME"]
    status = data["status"]

    payload = _build_slack_attachment(
        project_id=project_id,
        logs_url=logs_url,
        trigger_name=trigger_name,
        branch_name=branch_name,
        status=status
    )
    requests.post(
        webhook_url,
        data=json.dumps(payload)
    )


def _build_slack_attachment(
        project_id, 
        logs_url,
        trigger_name,
        branch_name,
        status
    ):

    if status == BuildStatus.SUCCESS:
        color = "#36a64f"
    elif status in (BuildStatus.FAILURE, BuildStatus.CANCELLED, BuildStatus.TIMEOUT):
        color = "#FF0000"
    # elif status in (BuildStatus.QUEUED, BuildStatus.WORKING):
    elif status == BuildStatus.QUEUED:
        color = "#808080"
    elif status == BuildStatus.WORKING:
        return ""
    else:
        raise ValueError("Unknown Cloud Build Status")

    payload = {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Cloud Build Deployment*: {status}\n*<{logs_url}|Logs URL>*"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Project:*\n{project_id}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Trigger:*\n{trigger_name}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Branch:*\n{branch_name}"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return payload
