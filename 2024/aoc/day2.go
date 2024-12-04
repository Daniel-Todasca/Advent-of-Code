package main

import "strings"

func main() {
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
	for _, levels := range reports {
		if len(levels) < 2 {
			// all lines should have more than 2 reports (even more than 5)
			panic("Report line is too small")
		}

		if levels[0] > levels[1] {
			// reverse the list if seems like decreasing order for simplicity
			for l, r := 0, len(levels)-1; l < r; l, r = l+1, r-1 {
				levels[l], levels[r] = levels[r], levels[l]
			}
		}

		safe := true
		for i := 1; i < len(levels); i++ {
			if levels[i] < levels[i-1] {
				// means it's not in increasing order
				safe = false
				break
			}
			diff := levels[i] - levels[i-1]
			if diff < 1 || diff > 3 {
				safe = false
				break
			}
		}

		if safe {
			total1++
		}
	}

	println(total1)
	println(total2)
}
