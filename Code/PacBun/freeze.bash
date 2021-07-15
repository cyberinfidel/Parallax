#!/bin/bash
cxfreeze -O -c PacBun.py --target-dir Freeze/ --include-path .. --include-files=user.config,game.config,PB_scenes.config,PB_cutscenes.config
cp -r Graphics Freeze/
cp -r Fonts Freeze/
rm -r ~/Desktop/Freeze
cp -r Freeze ~/Desktop