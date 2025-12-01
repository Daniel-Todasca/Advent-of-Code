package main

import (
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func _main() {
	lines, err := aocReadFile("./inputs/day1/input.txt")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to read file: %v\n", err)
		return
	}

	var list1 []int
	var list2 []int
	for _, line := range lines {
		fields := strings.Fields(line)
		first, err := strconv.Atoi(fields[0])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error converting to int")
		}
		second, err := strconv.Atoi(fields[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error converting to int")
		}
		list1 = append(list1, first)
		list2 = append(list2, second)
	}

	slices.Sort(list1)
	slices.Sort(list2)

	var total int = 0
	for i := 0; i < len(list1); i++ {
		total += aocAbs(list2[i] - list1[i])
	}

	fmt.Println(total)

	var similarity int = 0
	var counter int = 0
	var secondArrayPtr int = 0
	for i := 0; i < len(list1); i++ {
		if i > 0 && list1[i-1] == list1[i] {
			total += list1[i] * counter
			continue
		}

		for secondArrayPtr < len(list2) && list2[secondArrayPtr] < list1[i] {
			secondArrayPtr++
		}

		counter = 0
		for secondArrayPtr < len(list2) && list2[secondArrayPtr] == list1[i] {
			secondArrayPtr++
			counter++
		}
		similarity += list1[i] * counter
	}

	fmt.Println(similarity)
}
