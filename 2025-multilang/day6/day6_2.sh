#!/bin/bash

file_name="input.txt"
file_content=$(cat "$file_name")

line_count=$(wc -l < "$file_name")
max_length=$(head -n 1 "$file_name" | wc -c)

op_line=$(tail -n 1 "$file_name")

sum=0
current_number=""
current_op=""
col_sum=0
col_prod=1

for ((col = 0; col < max_length; col++)); do
    column_str=$(echo "$file_content" | awk -v col=$((col+1)) 'NR<='"$line_count"' {s=s substr($0, col, 1)} END {print s}')
    op_char="${op_line:$col:1}"
    
    column_clean="${column_str// /}"
    if [[ -z "$column_clean" ]]; then
        if [[ "$current_op" == "+" ]]; then
            sum=$((sum + col_sum))
        elif [[ "$current_op" == "*" ]]; then
            sum=$((sum + col_prod))
        fi
        current_op=""
        col_sum=0
        col_prod=1
        continue
    fi
    
    if [[ "$op_char" == "+" || "$op_char" == "*" ]]; then
        current_op="$op_char"
    fi
    
    echo $col $max_length
    col_prod=$((col_prod * (column_clean == 0 ? 1 : column_clean)))
    col_sum=$((col_sum + column_clean))
done

if [[ "$current_op" == "+" ]]; then
    sum=$((sum + col_sum))
elif [[ "$current_op" == "*" ]]; then
    sum=$((sum + col_prod))
fi

echo "Result: $sum"