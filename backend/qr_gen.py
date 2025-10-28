import qrcode
from typing import Optional

def make_qr(url: str, out_file: Optional[str] = None):
    img = qrcode.make(url)
    if out_file:
        img.save(out_file)
        return out_file
    return img
