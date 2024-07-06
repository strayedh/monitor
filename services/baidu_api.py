import requests
import base64
import cv2  # Ensure cv2 is imported

class BaiduAPI:
    def __init__(self):
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': 'MKTFGlag5FYOhmU9mOkOud8m',  # Replace with your client_id
            'client_secret': 'pUgCL5rifTeiKnkjjn4eT9PzdlburXHK'  # Replace with your client_secret
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception("Failed to get access token")

    def detect(self, frame):
        img_base64 = self.get_image_base64(frame)
        person_result = self.make_request("https://aip.baidubce.com/rest/2.0/image-classify/v1/body_num", img_base64)
        vehicle_result = self.make_request("https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect", img_base64)
        return {
            'person_info': person_result.get('person_info', []),
            'vehicle_info': vehicle_result.get('vehicle_info', []),
            'person_num': person_result.get('person_num', 0),
            'vehicle_num': vehicle_result.get('vehicle_num', {})
        }

    def get_image_base64(self, img):
        _, buffer = cv2.imencode('.jpg', img)
        return base64.b64encode(buffer).decode()

    def make_request(self, url, img_base64):
        params = {"image": img_base64}
        url = f"{url}?access_token={self.access_token}"
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=params, headers=headers)
        return response.json()
