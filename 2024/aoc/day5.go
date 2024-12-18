package main

import (
	"slices"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
)

var prereqNumbers map[int][]int = make(map[int][]int)
var totalNumbersInMiddle atomic.Int32
var totalNumbersInMiddleWithReordering atomic.Int32
var waitGroup sync.WaitGroup

func processPageOrder(pages []int) {
	var isOrdered bool = true
	var numberRestrictions map[int]struct{} = make(map[int]struct{})
	for _, num := range pages {
		_, exists := numberRestrictions[num]
		if exists {
			isOrdered = false
			break
		}

		for _, restriction := range prereqNumbers[num] {
			numberRestrictions[restriction] = struct{}{}
		}
	}

	if isOrdered {
		totalNumbersInMiddle.Add(int32(pages[len(pages)/2]))
	} else {
		slices.SortFunc(pages, func(page int, other int) int {
			if slices.Contains(prereqNumbers[page], other) {
				return 1
			}
			if slices.Contains(prereqNumbers[other], page) {
				return -1
			}
			return 0
		})
		totalNumbersInMiddleWithReordering.Add(int32(pages[len(pages)/2]))
	}
	waitGroup.Done()
}

func _main5() {
	input, err := aocReadFile("./inputs/day5/input.txt")
	if err != nil {
		panic(err)
	}

	var parseLineIndex int = 0
	for len(input[parseLineIndex]) > 1 {
		rule := input[parseLineIndex]
		parseLineIndex++

		nums := strings.Split(rule, "|")
		left, err := strconv.Atoi(nums[0])
		if err != nil {
			panic("Error parsing left: " + nums[0])
		}
		right, err := strconv.Atoi(nums[1])
		if err != nil {
			panic("Error parsing right: " + nums[1])
		}

		prereqNumbers[right] = append(prereqNumbers[right], left)
	}

	parseLineIndex++

	for parseLineIndex < len(input) {
		pages := strings.Split(input[parseLineIndex], ",")
		var pages_int []int = make([]int, 0)
		for _, page := range pages {
			page_int, err := strconv.Atoi(page)
			if err != nil {
				panic("Error parsing page: " + page)
			}
			pages_int = append(pages_int, page_int)
		}
		waitGroup.Add(1)
		go processPageOrder(pages_int)
		parseLineIndex++
	}

	waitGroup.Wait()
	println(totalNumbersInMiddle.Load())
	println(totalNumbersInMiddleWithReordering.Load())
}
