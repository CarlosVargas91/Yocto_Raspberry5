#!/usr/bin/env python3
"""
Detailed expressive emotion faces
With eyebrows, round eyes, curved mouths, tongue!
"""

def create_happy_face_detailed():
    """Happy face with tongue out! 😋"""
    face = bytearray(1024)
    
    # Page 1: Happy eyebrows (curved up at ends)
    offset = 1 * 128
    # Left eyebrow
    for col in range(25, 50):
        if col < 30:
            face[offset + col] = 0xC0  # Outer edge higher
        elif col < 35:
            face[offset + col] = 0xE0
        elif col < 45:
            face[offset + col] = 0xF0
        else:
            face[offset + col] = 0xE0  # Inner edge lower
    
    # Right eyebrow
    for col in range(78, 103):
        if col < 83:
            face[offset + col] = 0xE0  # Inner edge lower
        elif col < 93:
            face[offset + col] = 0xF0
        elif col < 98:
            face[offset + col] = 0xE0
        else:
            face[offset + col] = 0xC0  # Outer edge higher
    
    # Page 2: Top of round eyes
    offset = 2 * 128
    # Left eye - round top
    for col in range(28, 52):
        if 30 <= col <= 32 or 47 <= col <= 49:
            face[offset + col] = 0x3C  # Edges of circle
        elif 33 <= col <= 46:
            face[offset + col] = 0x18  # Top curve
    
    # Right eye - round top
    for col in range(76, 100):
        if 78 <= col <= 80 or 95 <= col <= 97:
            face[offset + col] = 0x3C
        elif 81 <= col <= 94:
            face[offset + col] = 0x18
    
    # Page 3: Eyes with pupils
    offset = 3 * 128
    # Left eye
    for col in range(28, 52):
        if col < 32 or col > 47:
            face[offset + col] = 0xFF  # Eye whites + outline
        elif 35 <= col <= 43:
            face[offset + col] = 0x00  # Pupil (looking happy!)
        else:
            face[offset + col] = 0xFF  # More white
    
    # Right eye
    for col in range(76, 100):
        if col < 80 or col > 95:
            face[offset + col] = 0xFF
        elif 83 <= col <= 91:
            face[offset + col] = 0x00  # Pupil
        else:
            face[offset + col] = 0xFF
    
    # Page 4: Bottom of eyes
    offset = 4 * 128
    # Left eye - round bottom
    for col in range(28, 52):
        if 30 <= col <= 32 or 47 <= col <= 49:
            face[offset + col] = 0x3C
        elif 33 <= col <= 46:
            face[offset + col] = 0x18
    
    # Right eye - round bottom
    for col in range(76, 100):
        if 78 <= col <= 80 or 95 <= col <= 97:
            face[offset + col] = 0x3C
        elif 81 <= col <= 94:
            face[offset + col] = 0x18
    
    # Page 5: Top of big smile
    offset = 5 * 128
    for col in range(30, 98):
        if col < 35 or col > 93:
            face[offset + col] = 0x01  # Smile edges start
        elif col < 45 or col > 83:
            face[offset + col] = 0x03  # Smile curves
        else:
            face[offset + col] = 0x07  # Wide open mouth top
    
    # Page 6: Big smile with TONGUE!
    offset = 6 * 128
    for col in range(30, 98):
        if col < 35 or col > 93:
            face[offset + col] = 0xC0  # Smile edges
        elif col < 40 or col > 88:
            face[offset + col] = 0xE0  # Smile curves down
        elif 55 <= col <= 73:
            # TONGUE! Sticking out in the middle
            face[offset + col] = 0xFC  # Pink tongue pattern
        else:
            face[offset + col] = 0xF0  # Bottom of smile
    
    # Page 7: Tip of tongue
    offset = 7 * 128
    for col in range(58, 70):
        face[offset + col] = 0x07  # Tongue tip
    
    return bytes(face)

def create_sad_face_detailed():
    """Sad face with droopy eyebrows and frown 😢"""
    face = bytearray(1024)
    
    # Page 1: Sad eyebrows (curved down at ends)
    offset = 1 * 128
    # Left eyebrow - droops down on outer edge
    for col in range(25, 50):
        if col < 30:
            face[offset + col] = 0xE0  # Outer edge lower
        elif col < 35:
            face[offset + col] = 0xF0
        elif col < 45:
            face[offset + col] = 0xF0
        else:
            face[offset + col] = 0xC0  # Inner edge higher
    
    # Right eyebrow - droops down on outer edge
    for col in range(78, 103):
        if col < 83:
            face[offset + col] = 0xC0  # Inner edge higher
        elif col < 93:
            face[offset + col] = 0xF0
        elif col < 98:
            face[offset + col] = 0xF0
        else:
            face[offset + col] = 0xE0  # Outer edge lower
    
    # Page 2-4: Eyes (same structure as happy but sadder pupils)
    offset = 2 * 128
    for col in range(28, 52):
        if 30 <= col <= 32 or 47 <= col <= 49:
            face[offset + col] = 0x3C
        elif 33 <= col <= 46:
            face[offset + col] = 0x18
    for col in range(76, 100):
        if 78 <= col <= 80 or 95 <= col <= 97:
            face[offset + col] = 0x3C
        elif 81 <= col <= 94:
            face[offset + col] = 0x18
    
    offset = 3 * 128
    for col in range(28, 52):
        if col < 32 or col > 47:
            face[offset + col] = 0xFF
        elif 37 <= col <= 41:  # Pupils looking sad (centered low)
            face[offset + col] = 0x00
        else:
            face[offset + col] = 0xFF
    for col in range(76, 100):
        if col < 80 or col > 95:
            face[offset + col] = 0xFF
        elif 85 <= col <= 89:
            face[offset + col] = 0x00
        else:
            face[offset + col] = 0xFF
    
    offset = 4 * 128
    for col in range(28, 52):
        if 30 <= col <= 32 or 47 <= col <= 49:
            face[offset + col] = 0x3C
        elif 33 <= col <= 46:
            face[offset + col] = 0x18
    for col in range(76, 100):
        if 78 <= col <= 80 or 95 <= col <= 97:
            face[offset + col] = 0x3C
        elif 81 <= col <= 94:
            face[offset + col] = 0x18
    
    # Page 6: Frown (upside-down smile)
    offset = 6 * 128
    for col in range(35, 93):
        if col < 40 or col > 88:
            face[offset + col] = 0x07  # Frown edges
        elif col < 50 or col > 78:
            face[offset + col] = 0x03  # Curve down
        else:
            face[offset + col] = 0x01  # Bottom of frown
    
    # Page 7: Bottom of frown curves
    offset = 7 * 128
    for col in range(35, 93):
        if col < 40 or col > 88:
            face[offset + col] = 0xE0
        elif col < 50 or col > 78:
            face[offset + col] = 0xC0
        else:
            face[offset + col] = 0x80
    
    return bytes(face)

def create_neutral_face_detailed():
    """Neutral face with straight eyebrows and mouth 😐"""
    face = bytearray(1024)
    
    # Page 1: Straight eyebrows
    offset = 1 * 128
    for col in range(25, 50):
        face[offset + col] = 0xF0  # Left eyebrow
    for col in range(78, 103):
        face[offset + col] = 0xF0  # Right eyebrow
    
    # Page 2-4: Eyes (same as others)
    offset = 2 * 128
    for col in range(28, 52):
        if 30 <= col <= 32 or 47 <= col <= 49:
            face[offset + col] = 0x3C
        elif 33 <= col <= 46:
            face[offset + col] = 0x18
    for col in range(76, 100):
        if 78 <= col <= 80 or 95 <= col <= 97:
            face[offset + col] = 0x3C
        elif 81 <= col <= 94:
            face[offset + col] = 0x18
    
    offset = 3 * 128
    for col in range(28, 52):
        if col < 32 or col > 47:
            face[offset + col] = 0xFF
        elif 38 <= col <= 42:
            face[offset + col] = 0x00  # Centered pupils
        else:
            face[offset + col] = 0xFF
    for col in range(76, 100):
        if col < 80 or col > 95:
            face[offset + col] = 0xFF
        elif 86 <= col <= 90:
            face[offset + col] = 0x00
        else:
            face[offset + col] = 0xFF
    
    offset = 4 * 128
    for col in range(28, 52):
        if 30 <= col <= 32 or 47 <= col <= 49:
            face[offset + col] = 0x3C
        elif 33 <= col <= 46:
            face[offset + col] = 0x18
    for col in range(76, 100):
        if 78 <= col <= 80 or 95 <= col <= 97:
            face[offset + col] = 0x3C
        elif 81 <= col <= 94:
            face[offset + col] = 0x18
    
    # Page 5: Straight mouth line
    offset = 5 * 128
    for col in range(40, 88):
        face[offset + col] = 0xFF  # Horizontal line
    
    return bytes(face)

# Generate detailed faces
HAPPY_FACE = create_happy_face_detailed()
SAD_FACE = create_sad_face_detailed()
NEUTRAL_FACE = create_neutral_face_detailed()

if __name__ == "__main__":
    print("✅ Detailed emotion faces generated!")
    print(f"   Happy (with tongue!): {len(HAPPY_FACE)} bytes")
    print(f"   Sad (droopy brows): {len(SAD_FACE)} bytes")
    print(f"   Neutral (meh): {len(NEUTRAL_FACE)} bytes")
