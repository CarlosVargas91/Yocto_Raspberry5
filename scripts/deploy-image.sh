#!/bin/bash
# =============================================================================
# deploy-image.sh - Yocto Image Deploy Script (Run on Ubuntu VM)
# Project: yocto-ai-project - Raspberry Pi 5
# Author: Carlos Vargas
# Usage: ./deploy-image.sh [version_tag]
# Example: ./deploy-image.sh v4
# =============================================================================

set -e  # Exit immediately on any error

# =============================================================================
# CONFIGURATION - Edit these variables as needed
# =============================================================================
YOCTO_DIR="$HOME/Documents/Yocto/yocto-ai-project"
BUILD_DIR="$YOCTO_DIR/build-rpi5"
IMAGES_DIR="$BUILD_DIR/tmp/deploy/images/raspberrypi5"
MACHINE="raspberrypi5"
IMAGE_NAME="core-image-base"
VERSION_TAG="${1:-$(date +v%Y%m%d_%H%M%S)}"  # Use arg or timestamp
OUTPUT_IMAGE="rpi5-image-${VERSION_TAG}.wic"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
print_step() {
    echo -e "\n${BLUE}==== $1 ====${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# =============================================================================
# STEP 1: Verify build environment
# =============================================================================
print_step "Step 1: Verifying environment"

if [ ! -d "$YOCTO_DIR" ]; then
    print_error "Yocto directory not found: $YOCTO_DIR"
fi

if [ ! -d "$IMAGES_DIR" ]; then
    print_error "Images directory not found. Did you run bitbake core-image-base?"
fi

print_success "Environment verified"

# =============================================================================
# STEP 2: Find latest image
# =============================================================================
print_step "Step 2: Finding latest image"

# Find the most recent .wic.bz2 file
LATEST_IMAGE=$(ls -t "$IMAGES_DIR"/${IMAGE_NAME}-${MACHINE}-*.rootfs.wic.bz2 2>/dev/null | head -1)

if [ -z "$LATEST_IMAGE" ]; then
    print_error "No .wic.bz2 image found in $IMAGES_DIR"
fi

echo "Found image: $(basename $LATEST_IMAGE)"
echo "Size: $(ls -lh $LATEST_IMAGE | awk '{print $5}')"
echo "Date: $(ls -lh $LATEST_IMAGE | awk '{print $6, $7, $8}')"
print_success "Image found"

# =============================================================================
# STEP 3: Decompress image
# =============================================================================
print_step "Step 3: Decompressing image"

cd "$IMAGES_DIR"

# Remove old decompressed image if exists
if [ -f "$OUTPUT_IMAGE" ]; then
    print_warning "Removing old image: $OUTPUT_IMAGE"
    rm "$OUTPUT_IMAGE"
fi

echo "Decompressing to: $OUTPUT_IMAGE"
echo "This may take a minute..."

bzcat "$LATEST_IMAGE" > "$OUTPUT_IMAGE"

# Verify decompression
if [ ! -f "$OUTPUT_IMAGE" ]; then
    print_error "Decompression failed!"
fi

IMAGE_SIZE=$(ls -lh "$OUTPUT_IMAGE" | awk '{print $5}')
print_success "Image decompressed successfully: $IMAGE_SIZE"

# Verify it's a valid disk image
FILE_TYPE=$(file "$OUTPUT_IMAGE" | grep -c "boot sector" || true)
if [ "$FILE_TYPE" -eq 0 ]; then
    print_warning "Image may not be a valid boot sector - verify manually"
else
    print_success "Valid boot sector detected"
fi

# =============================================================================
# STEP 4: Get VM IP for transfer instructions
# =============================================================================
print_step "Step 4: Network information"

VM_IP=$(ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | cut -d'/' -f1 | head -1)

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Image ready for transfer to Mac!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Image location:"
echo "  $IMAGES_DIR/$OUTPUT_IMAGE"
echo ""
echo -e "${YELLOW}Run this command on your MAC terminal:${NC}"
echo ""
echo -e "${BLUE}  scp goyii@${VM_IP}:${IMAGES_DIR}/${OUTPUT_IMAGE} ~/Downloads/${NC}"
echo ""
echo -e "${YELLOW}Then flash with:${NC}"
echo ""
echo -e "${BLUE}  ~/Downloads/flash-sd.sh ~/Downloads/${OUTPUT_IMAGE}${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"