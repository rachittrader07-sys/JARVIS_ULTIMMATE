"""
👁️ Screen Analyzer
Analyzes screen content for errors and information
"""

import cv2
import numpy as np
import pyautogui
import pytesseract
from colorama import Fore, Style
from PIL import Image, ImageGrab


class ScreenAnalyzer:
    def __init__(self, config):
        self.config = config
        # Set tesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def capture_screen(self):
        """👁️ Capture entire screen"""
        try:
            screenshot = ImageGrab.grab()
            return screenshot
        except Exception as e:
            print(Fore.RED + f"❌ Screen capture failed: {str(e)}" + Style.RESET_ALL)
            return None

    def capture_region(self, x, y, width, height):
        """👁️ Capture specific screen region"""
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            return screenshot
        except:
            return None

    def find_error_popups(self):
        """👁️ Find error popups on screen"""
        try:
            # Capture screen
            screenshot = self.capture_screen()
            if not screenshot:
                return []

            # Convert to OpenCV format
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Look for common error colors (red, yellow)
            error_colors = [
                ([0, 0, 200], [100, 100, 255]),  # Red
                ([0, 200, 200], [100, 255, 255]),  # Yellow
            ]

            errors = []

            for lower, upper in error_colors:
                lower = np.array(lower, dtype="uint8")
                upper = np.array(upper, dtype="uint8")

                # Create mask
                mask = cv2.inRange(screenshot_cv, lower, upper)

                # Find contours
                contours, _ = cv2.findContours(
                    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )

                for contour in contours:
                    if cv2.contourArea(contour) > 1000:  # Minimum size
                        x, y, w, h = cv2.boundingRect(contour)

                        # Extract text from region
                        region = screenshot.crop((x, y, x + w, y + h))
                        text = self.extract_text(region)

                        if text and any(
                            word in text.lower()
                            for word in [
                                "error",
                                "failed",
                                "invalid",
                                "problem",
                                "issue",
                            ]
                        ):
                            errors.append(
                                {
                                    "x": x,
                                    "y": y,
                                    "width": w,
                                    "height": h,
                                    "text": text[:200],  # Limit text length
                                    "type": "error_popup",
                                }
                            )

            return errors

        except Exception as e:
            print(
                Fore.RED
                + f"❌ Error popup detection failed: {str(e)}"
                + Style.RESET_ALL
            )
            return []

    def find_dialog_boxes(self):
        """👁️ Find dialog boxes on screen"""
        try:
            # Look for standard dialog box patterns
            screenshot = self.capture_screen()
            if not screenshot:
                return []

            # Convert to grayscale
            gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            # Edge detection
            edges = cv2.Canny(gray, 50, 150)

            # Find rectangles (dialog boxes are usually rectangular)
            contours, _ = cv2.findContours(
                edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            dialogs = []

            for contour in contours:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

                # Check if it's a rectangle (4 corners)
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(contour)

                    # Check if it's dialog-sized (not too small or too large)
                    if 200 < w < 800 and 100 < h < 600:
                        # Extract text
                        region = screenshot.crop((x, y, x + w, y + h))
                        text = self.extract_text(region)

                        if text:
                            dialogs.append(
                                {
                                    "x": x,
                                    "y": y,
                                    "width": w,
                                    "height": h,
                                    "text": text[:200],
                                    "type": "dialog_box",
                                }
                            )

            return dialogs

        except Exception as e:
            print(Fore.RED + f"❌ Dialog detection failed: {str(e)}" + Style.RESET_ALL)
            return []

    def extract_text(self, image):
        """👁️ Extract text from image using OCR"""
        try:
            # Use pytesseract
            text = pytesseract.image_to_string(image)
            return text.strip()
        except:
            # Fallback: try easyocr
            try:
                import easyocr

                reader = easyocr.Reader(["en"])
                result = reader.readtext(np.array(image))
                text = " ".join([item[1] for item in result])
                return text
            except:
                return ""

    def analyze_current_window(self):
        """👁️ Analyze current active window"""
        try:
            # Get active window title
            import pygetwindow as gw

            windows = gw.getActiveWindow()

            if not windows:
                return None

            window_title = windows.title

            # Capture window region
            x, y, width, height = (
                windows.left,
                windows.top,
                windows.width,
                windows.height,
            )
            window_screenshot = self.capture_region(x, y, width, height)

            if not window_screenshot:
                return {"window_title": window_title, "errors": [], "dialogs": []}

            # Analyze for errors in this window
            errors = self.find_errors_in_image(window_screenshot)

            return {
                "window_title": window_title,
                "position": {"x": x, "y": y, "width": width, "height": height},
                "errors": errors,
                "screenshot": window_screenshot,
            }

        except Exception as e:
            print(Fore.RED + f"❌ Window analysis failed: {str(e)}" + Style.RESET_ALL)
            return None

    def find_errors_in_image(self, image):
        """👁️ Find errors in specific image"""
        errors = []

        try:
            # Convert to OpenCV
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            # Look for error text patterns
            text = self.extract_text(image)

            error_keywords = [
                "error",
                "failed",
                "invalid",
                "problem",
                "issue",
                "cannot",
                "unable",
                "not found",
                "missing",
                "corrupt",
                "access denied",
                "permission denied",
                "timeout",
                "crash",
            ]

            for keyword in error_keywords:
                if keyword in text.lower():
                    errors.append(
                        {
                            "type": "text_error",
                            "keyword": keyword,
                            "context": self.get_context(text, keyword),
                        }
                    )

            # Look for error icons/symbols (simplified)
            # This would need actual image recognition in production

            return errors

        except:
            return errors

    def get_context(self, text, keyword):
        """👁️ Get context around keyword in text"""
        try:
            index = text.lower().find(keyword)
            if index == -1:
                return ""

            # Get 50 characters before and after
            start = max(0, index - 50)
            end = min(len(text), index + len(keyword) + 50)

            return text[start:end]
        except:
            return ""

    def take_action_on_error(self, error_info):
        """👁️ Take action based on detected error"""
        error_type = error_info.get("type", "")
        text = error_info.get("text", "").lower()

        actions = []

        # Common error patterns and suggested actions
        if "close" in text or "ok" in text:
            actions.append(
                {
                    "action": "click_button",
                    "button": "close/ok",
                    "description": "Click the close or OK button",
                }
            )

        if "retry" in text or "try again" in text:
            actions.append(
                {
                    "action": "click_button",
                    "button": "retry",
                    "description": "Click the retry button",
                }
            )

        if "ignore" in text or "continue" in text:
            actions.append(
                {
                    "action": "click_button",
                    "button": "ignore",
                    "description": "Click ignore or continue",
                }
            )

        if "details" in text or "more info" in text:
            actions.append(
                {
                    "action": "click_button",
                    "button": "details",
                    "description": "Click for more details",
                }
            )

        # If no specific actions found, suggest generic action
        if not actions:
            actions.append(
                {
                    "action": "read_error",
                    "description": "Read the error message carefully",
                }
            )

        return actions
