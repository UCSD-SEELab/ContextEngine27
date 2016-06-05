#!/bin/bash

image_path='dataset/test'
total=0
success_count=0
for class in "$image_path"/*
do
        for file in "$class"/*
        do
            success=$(python getClass.py -i "$file")
            success_count=$((success_count + success))
            echo "$success"
            total=$((total + 1))
        done
done
echo "$success_count" out of "$total"
