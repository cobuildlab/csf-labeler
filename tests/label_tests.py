import unittest
import uuid
import os
from unittest.mock import patch


class LabelTestCase(unittest.TestCase):

    def test_draw(self):
        with patch('config.FONT_PATH', new='/Users/alacret/workspace/csf-labeler/assets/arial.ttf') as mocked_font_path:
            self.assertIsNotNone(mocked_font_path)
            from label import generate_label
            unique_id = str(uuid.uuid4())
            printer_serial = "PRINTER_SERIAL_ID"
            label_src = "./label.png"
            generate_label(1, 3, "0.5", "TBA1234567890", unique_id, printer_serial, label_src)
            self.assertTrue(os.path.exists(label_src))


if __name__ == '__main__':
    unittest.main()
