import os
from src.util.logger import Logger

class MedalHandler:
    def __init__(self):
        self.logger = Logger()
        self.base_dir = "/root/csgo-checker-api/src/medals/output"

    async def get_image_path(self, image_name: str):
        path = os.path.join(self.base_dir, f"{image_name}.png")
        if not os.path.isfile(path):
            self.logger.log("ERROR", f"Image {image_name}.png does not exist at the expected location.")
            return None
        self.logger.log("INFO", f"Getting image path for {image_name}.png")
        return path
    
    async def delete_image(self, image_name: str):
        path = os.path.join(self.base_dir, f"{image_name}.png")
        if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                self.logger.log("ERROR", f"Error while deleting image: {e}")
                return False
            self.logger.log("INFO", f"Successfully deleted image {image_name}.png")
            return True
        else:
            self.logger.log("ERROR", f"Image {image_name}.png does not exist, so it could not be deleted.")
            return False