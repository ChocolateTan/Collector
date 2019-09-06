#!/bin/sh
cd /root/Projects/Collector/creator
git pull
/usr/bin/python3 collector_info.py
git add -A
git commit -m 'update post'
git push