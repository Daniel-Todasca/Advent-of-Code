package main

import (
	"fmt"
	"strings"
	"strconv"
	"bufio"
	"os"
	"sort"
)

func readFile(filename string) ([]string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return lines, nil
}

type Range struct {
	left, right int64
}

func solvePart1(ranges []Range, ids []int64) {
	var totalPart1 int32 = 0

	for _, id := range ids {
		valid := false
		for _, pair := range ranges {
			if id >= pair.left && id <= pair.right {
				valid = true
				break
			}
		}

		if valid {
			totalPart1 ++
		}
	}

	fmt.Println("Part 1: ", totalPart1)
}

func solvePart2(ranges []Range, ids []int64) {
	var totalPart2 int64 = 0
	
	sort.Slice(ranges, func(i, j int) bool {
		if ranges[i].left == ranges[j].left {
			return ranges[i].right < ranges[j].right
		}
		return ranges[i].left < ranges[j].left
	})

	ptr1, ptr2 := 0, 1
	for ptr2 < len(ranges) && ptr1 < len(ranges) {
		if ranges[ptr1].right >= ranges[ptr2].left {
			ranges[ptr1].right = max(ranges[ptr1].right, ranges[ptr2].right)
			ptr2++
		} else {
			totalPart2 += ranges[ptr1].right - ranges[ptr1].left + 1
			ptr1 = ptr2
			ptr2++
		}
	}

	totalPart2 += ranges[ptr1].right - ranges[ptr1].left + 1
	fmt.Println("Part 2: ", totalPart2)
}

func main() {
    lines, err := readFile("input.txt")
	if err != nil {
		fmt.Println("Error reading file: ", err)
		return
	}

	var ranges []Range 
	var ids []int64

	lineIdx := 0
	for len(lines[lineIdx]) > 0 {
		nums := strings.Split(lines[lineIdx], "-")
		left, _ := strconv.ParseInt(nums[0], 10, 64)
		right, _ := strconv.ParseInt(nums[1], 10, 64)
		ranges = append(ranges, Range{left, right} )
		lineIdx ++
	}
	lineIdx ++

	for ; lineIdx < len(lines); lineIdx++ {
		num, _ := strconv.ParseInt(lines[lineIdx], 10, 64)
		ids = append(ids, num)
	}

	solvePart1(ranges, ids)
	solvePart2(ranges, ids)
}