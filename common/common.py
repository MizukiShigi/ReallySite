import requests

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = 'N5hLvSnDWk1rHRgRiicCXVIde7nGxLY1ACZ8LYzcLNB'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)