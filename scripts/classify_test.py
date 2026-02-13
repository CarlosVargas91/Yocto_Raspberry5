#!/usr/bin/env python3
"""
Real AI Image Classification
MobileNetV1 on Raspberry Pi 5 - Yocto Linux
Carlos Vargas - meta-homeai
"""

import numpy as np
import tflite_runtime.interpreter as tflite
import time

print("=" * 60)
print("  Real AI Inference - Image Classification")
print("  MobileNetV1 on Raspberry Pi 5")
print("=" * 60)

# Load the model
print("\n[1/5] Loading MobileNetV1 model...")
interpreter = tflite.Interpreter(model_path="/home/root/models/mobilenet_v1_1.0_224_quant.tflite")
interpreter.allocate_tensors()
print("    ✅ Model loaded successfully")

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("\n[2/5] Model Information:")
print(f"    Input shape: {input_details[0]['shape']}")
print(f"    Input type: {input_details[0]['dtype']}")
print(f"    Output shape: {output_details[0]['shape']}")
print(f"    Output type: {output_details[0]['dtype']}")

# Load labels
print("\n[3/5] Loading ImageNet labels...")
with open("/home/root/models/labels_mobilenet_quant_v1_224.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]
print(f"    ✅ Loaded {len(labels)} class labels")

# Create a random test image (simulating camera input)
print("\n[4/5] Creating test image (random data)...")
input_shape = input_details[0]['shape']
test_image = np.random.randint(0, 256, input_shape, dtype=np.uint8)
print(f"    Input shape: {test_image.shape}")
print(f"    Input dtype: {test_image.dtype}")

# Run inference
print("\n[5/5] Running AI inference...")
interpreter.set_tensor(input_details[0]['index'], test_image)

# Measure inference time
start = time.time()
interpreter.invoke()
inference_time = (time.time() - start) * 1000

# Get results
output_data = interpreter.get_tensor(output_details[0]['index'])
top_5_indices = np.argsort(output_data[0])[-5:][::-1]

print(f"\n    ⚡ Inference time: {inference_time:.2f}ms")
print(f"    🚀 FPS capability: {1000/inference_time:.1f} frames/sec")

print("\n    Top 5 Predictions (random image):")
for i, idx in enumerate(top_5_indices, 1):
    confidence = output_data[0][idx] / 255.0 * 100
    print(f"    {i}. {labels[idx]:30s} {confidence:5.2f}%")

print("\n" + "=" * 60)
print("  ✅ AI Inference Working!")
print(f"  Performance: {inference_time:.2f}ms per image")
print(f"  Model: MobileNetV1 (INT8 quantized)")
print(f"  Device: Raspberry Pi 5 - Custom Yocto Linux")
print("=" * 60)
print("\n💡 Next: Connect a camera for real-time classification!")
