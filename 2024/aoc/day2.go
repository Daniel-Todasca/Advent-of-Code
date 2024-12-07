package main

import "strings"

func isSafe(report []int) bool {
	if len(report) < 2 {
		// all lines should have more than 2 reports (even more than 5)
		panic("Report line is too small")
	}

	if report[0] > report[1] {
		// reverse the list if seems like decreasing order for simplicity
		for l, r := 0, len(report)-1; l < r; l, r = l+1, r-1 {
			report[l], report[r] = report[r], report[l]
		}
	}

	for i := 1; i < len(report); i++ {
		if report[i] < report[i-1] {
			// means it's not in increasing order
			return false
		}
		diff := report[i] - report[i-1]
		if diff < 1 || diff > 3 {
			return false
		}
	}

	return true
}

func _main2() {
	lines, err := aocReadFile("./inputs/day2/input.txt")
	if err != nil {
		panic(err)
	}

	var reports [][]int
	for _, line := range lines {
		levels := strings.Fields(line)
		slice, err := aocStringSliceToIntSlice(levels)
		if err != nil {
			panic("Error converting strings to ints")
		}
		reports = append(reports, slice)
	}

	total1 := 0
	total2 := 0
	for _, report := range reports {
		if isSafe(report) {
			total1++
			total2++
			continue
		}

		for idx := 0; idx < len(report); idx++ {
			sublist := make([]int, len(report))
			copy(sublist, report)
			sublist = append(sublist[:idx], sublist[idx+1:]...)
			if isSafe(sublist) {
				total2++
				break
			}
		}

	}

	println(total1)
	println(total2)
}
