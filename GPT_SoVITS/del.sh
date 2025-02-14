#!/bin/bash
cd /root/autodl-tmp/workdir/GPT-SoVITS
rm -rf GPT_weights/*
rm -rf GPT_weights_v2/*
rm -rf GPT_weights_v3/*
rm -rf SoVITS_weights/*
rm -rf SoVITS_weights_v2/*
rm -rf SoVITS_weights_v3/*

rm -rf input/*
rm -rf output/asr_opt/*
rm -rf output/slicer_opt/*
rm -rf output/uvr5_opt/*
rm -rf output/denoise_opt/*
rm -rf logs/*
rm -rf TEMP/*
rm -rf sweight.txt
rm -rf gweight.txt
rm -rf weight.json

find ~ -name ".ipynb_checkpoints" -exec rm -r {} \;
echo 初始化完成