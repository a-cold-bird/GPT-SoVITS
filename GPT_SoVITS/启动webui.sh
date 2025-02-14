#!/bin/bash
find ~ -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
export is_share=true
HF_ENDPOINT=https://hf-mirror.com python /root/autodl-tmp/workdir/GPT-SoVITS/webui.py zh_CN
