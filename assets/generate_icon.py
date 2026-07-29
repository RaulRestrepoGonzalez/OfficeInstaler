import struct
import math
import os

SIZE = 32
COLOR = (124, 58, 237)
ACCENT = (168, 85, 247)


def create_ico():
    pixels = bytearray()
    and_mask = []
    cx = cy = SIZE // 2
    radius = cx - 3
    inner_r = radius // 2

    for y in range(SIZE):
        for x in range(SIZE):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > radius:
                pixels.extend([0, 0, 0, 0])
                and_mask.append(1)
            else:
                if dist <= inner_r:
                    fill = ACCENT
                else:
                    fill = COLOR
                b, g, r = fill[2], fill[1], fill[0]
                alpha = 255
                fade = max(0, min(255, int((radius - dist) * 8)))
                if dist > radius - 2:
                    alpha = fade
                pixels.extend([b, g, r, alpha])
                and_mask.append(0 if alpha > 128 else 1)

    row_size = ((SIZE + 31) // 32) * 4
    and_data = bytearray()
    for y in range(SIZE):
        for x in range(0, SIZE, 8):
            byte = 0
            for j in range(8):
                idx = y * SIZE + x + j
                if idx < len(and_mask):
                    byte |= (and_mask[idx] << (7 - j))
            and_data.append(byte)
        while len(and_data) < (y + 1) * row_size:
            and_data.append(0)

    xor_data = bytes(pixels)

    bih = struct.pack('<I', 40)
    bih += struct.pack('<i', SIZE)
    bih += struct.pack('<i', SIZE * 2)
    bih += struct.pack('<H', 1)
    bih += struct.pack('<H', 32)
    bih += struct.pack('<I', 0)
    bih += struct.pack('<I', len(xor_data) + len(and_data))
    bih += struct.pack('<i', 0)
    bih += struct.pack('<i', 0)
    bih += struct.pack('<I', 0)
    bih += struct.pack('<I', 0)

    image_data = bih + xor_data + bytes(and_data)

    ico = struct.pack('<H', 0)
    ico += struct.pack('<H', 1)
    ico += struct.pack('<H', 1)

    ico += struct.pack('B', SIZE)
    ico += struct.pack('B', SIZE)
    ico += struct.pack('B', 0)
    ico += struct.pack('B', 0)
    ico += struct.pack('<H', 1)
    ico += struct.pack('<H', 32)
    ico += struct.pack('<I', len(image_data))
    ico += struct.pack('<I', 22)

    ico += image_data
    return ico


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "app.ico")
    with open(out_path, "wb") as f:
        f.write(create_ico())
    print(f"Icono generado: {out_path}")
