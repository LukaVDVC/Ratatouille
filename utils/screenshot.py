import pyscreenshot
import io

class Screenshot:
    def get_screenshot(self):
        screenshot = pyscreenshot.grab()
        buffer = io.BytesIO()
        screenshot.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer.getvalue()
