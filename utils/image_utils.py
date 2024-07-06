from PIL import Image, ImageDraw, ImageFont
import io
import cv2
from PyQt5.QtGui import QImage

def annotate_image(frame, result, result_text, width, height):
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

    buffer = io.BytesIO()
    image = image.resize((width, height), Image.Resampling.LANCZOS)  # Update here
    image.save(buffer, format="PNG")
    buffer.seek(0)
    qimage = QImage.fromData(buffer.getvalue())

    return qimage
