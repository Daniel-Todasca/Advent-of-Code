#!/bin/bash

file_name="input.txt"
col_count=$(head -n 1 "$file_name" | awk '{print NF}')
line_count=$(wc -l < "$file_name")

declare -a col_sums
for ((i = 0; i < col_count; i++)); do
    col_sums[$i]=0
done

declare -a col_prod
for ((i = 0; i < col_count; i++)); do
    col_prod[$i]=1
done

for ((line = 1; line <= line_count; line++)); do
    current_line=$(sed -n "${line}p" "$file_name")
    
    col=0
    for num in $current_line; do
        col_sums[$col]=$((col_sums[$col] + num))
        col_prod[$col]=$((col_prod[$col] * num))
        ((col++))
    done
done

sum=0
sign_line=$(tail -n 1 "$file_name")
read -ra ops <<< "$sign_line"

idx=0
for op in "${ops[@]}"; do
    if [[ "$op" == "+" ]]; then
        sum=$((sum + col_sums[idx]))
    elif [[ "$op" == "*" ]]; then
        sum=$((sum + col_prod[idx]))
    fi
    idx=$((idx + 1))
done

echo $sum
