#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"
echo "🔄 Pulling latest changes from origin/master..."
git pull origin master
git submodule update --init --recursive

apt-get update
sudo apt-get install ffmpeg

# Ensure git-lfs is installed
command -v git-lfs >/dev/null 2>&1 || (brew install git-lfs || sudo apt-get install -y git-lfs && git lfs install)

echo "📦 Pulling large files with Git LFS..."
git lfs pull