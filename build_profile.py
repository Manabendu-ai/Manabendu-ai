import os
import io
import base64
import urllib.request
from PIL import Image

WORKSPACE = "/home/riku/Documents/github"
ASSETS_DIR = os.path.join(WORKSPACE, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

print("Starting asset generation...")

# 1. Fetch WOFF2 Fonts
def get_b64_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    with urllib.request.urlopen(req) as resp:
        return base64.b64encode(resp.read()).decode('utf-8')

print("Fetching Space Grotesk Bold WOFF2...")
space_grotesk_b64 = get_b64_url('https://fonts.gstatic.com/s/spacegrotesk/v22/V8mDoQDjQSkFtoMM3T6r8E7mPbF4C_k3HqU.woff2')

print("Fetching JetBrains Mono 600 WOFF2...")
jetbrains_mono_b64 = get_b64_url('https://fonts.gstatic.com/s/jetbrainsmono/v24/tDbY2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8FqtTOlOVk6OThhvA.woff2')

# 2. Process PNG images
print("Processing id.png...")
id_im = Image.open(os.path.join(WORKSPACE, 'id.png'))
# Resize id.png slightly to ~700px max dimension for optimal SVG embedding without losing quality
id_im.thumbnail((700, 700), Image.Resampling.LANCZOS)
buf_id = io.BytesIO()
id_im.save(buf_id, format='PNG', optimize=True)
id_b64 = base64.b64encode(buf_id.getvalue()).decode('utf-8')
print(f"id.png base64 length: {len(id_b64)}")

print("Processing right_pointing.png...")
right_im = Image.open(os.path.join(WORKSPACE, 'right_pointing.png'))
right_im.thumbnail((700, 700), Image.Resampling.LANCZOS)
buf_right = io.BytesIO()
right_im.save(buf_right, format='PNG', optimize=True)
right_b64 = base64.b64encode(buf_right.getvalue()).decode('utf-8')
print(f"right_pointing.png base64 length: {len(right_b64)}")

print("Fonts and PNGs ready!")
