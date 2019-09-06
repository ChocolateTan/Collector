#!/bin/sh
cd /root/Projects/Collector/creator
/usr/bin/python3 collector_info.py
git add -A
git commit -m 'update post'
git pull
git push