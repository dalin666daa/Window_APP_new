import cv2
from paddleocr import PaddleOCR

class OCRProcessor:
    def __init__(self):
        # Initialize the PaddleOCR with angle classification and English language
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def process_frame(self, frame):
        # Resize the frame for processing
        frame_resized = cv2.resize(frame, (640, 480))
        try:
            # Perform OCR on the resized frame
            results = self.ocr.ocr(frame_resized, cls=True)
            return results
        except Exception as e:
            print(f"Error processing frame: {e}")
            return []

    def display_results(self, results):
        # Extract detected text, confidence, and bounding boxes
        detected_info = []
        for line in results:
            for word_info in line:
                text = word_info[1][0]
                confidence = word_info[1][1]
                box = word_info[0]
                detected_info.append((text, confidence, box))
        return detected_info
