import os
import datetime
from PIL import Image, ImageDraw, ImageFont
import cv2

def save_detected_frame(frame, result, result_text):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    if 'person_info' in result:
        for person in result['person_info']:
            location = person['location']
            draw.rectangle(
                [(location['left'], location['top']),
                 (location['left'] + location['width'], location['top'] + location['height'])],
                outline="red", width=2
            )
            draw.text((location['left'], location['top'] - 10), "Person", fill="red", font=font)

    if 'vehicle_info' in result:
        for vehicle in result['vehicle_info']:
            location = vehicle['location']
            draw.rectangle(
                [(location['left'], location['top']),
                 (location['left'] + location['width'], location['top'] + location['height'])],
                outline="blue", width=2
            )
            draw.text((location['left'], location['top'] - 10), vehicle['type'], fill="blue", font=font)

    draw.text((10, 10), result_text, fill="white", font=font)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = os.path.join(os.getcwd(), "annotated_frames", timestamp)
    os.makedirs(output_path, exist_ok=True)

    image_filename = f"annotated_frame_{timestamp}.png"
    image.save(os.path.join(output_path, image_filename))
    print(f"Annotated image saved to {output_path}/{image_filename}")

    info_filename = f"recognition_info_{timestamp}.txt"
    info_path = os.path.join(output_path, info_filename)
    with open(info_path, 'w') as f:
        f.write(f"检测到的人数：{result.get('person_num', 0)}\n")
        f.write("检测到的车辆：\n")
        for k, v in result.get('vehicle_num', {}).items():
            f.write(f"{k}：{v}\n")
    print(f"Recognition information saved to {info_path}")
