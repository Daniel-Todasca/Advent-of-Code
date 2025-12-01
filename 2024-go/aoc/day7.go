package main

import (
	"fmt"
	"regexp"
	"strconv"
	"sync"
	"sync/atomic"
)

var sumOfPossibleEquations atomic.Int64
var sumOfConcatEquations atomic.Int64
var linesWaitGroups sync.WaitGroup

func concat(a int64, b int64) int64 {
	num, err := strconv.ParseInt(strconv.FormatInt(a, 10)+strconv.FormatInt(b, 10), 10, 64)
	if err != nil {
		panic(fmt.Sprintf("Could not concatenate 2 numbers: %d and %d", a, b))
	}
	return num
}

func processLine(line string) {
	defer linesWaitGroups.Done()

	numberTokens := regexp.MustCompile(`[\s:]+`).Split(line, -1)
	var numbers []int64 = make([]int64, len(numberTokens))
	for idx, token := range numberTokens {
		num, err := strconv.ParseInt(token, 10, 64)
		if err != nil {
			panic("Error parsing: " + token)
		}
		numbers[idx] = num
	}
	result := numbers[0]

	equations := []int64{numbers[1]}
	equationsWithConcat := []int64{numbers[1]}
	for idx := 2; idx < len(numbers); idx++ {
		var wg sync.WaitGroup
		wg.Add(2)

		go func() {
			defer wg.Done()
			nextEquations := []int64{}
			for _, num := range equations {
				nextEquations = append(nextEquations, num+numbers[idx], num*numbers[idx])
			}
			equations = nextEquations
		}()

		go func() {
			defer wg.Done()
			nextConcat := []int64{}
			for _, num := range equationsWithConcat {
				nextConcat = append(nextConcat, num+numbers[idx], num*numbers[idx], concat(num, numbers[idx]))
			}
			equationsWithConcat = nextConcat
		}()

		wg.Wait()
	}

	for _, partialEqu := range equations {
		if result == partialEqu {
			sumOfPossibleEquations.Add(int64(result))
			break
		}
	}

	for _, partialEqu := range equationsWithConcat {
		if result == partialEqu {
			sumOfConcatEquations.Add(int64(result))
			break
		}
	}
}

func _main7() {
	lines, err := aocReadFile("./inputs/day7/input.txt")
	if err != nil {
		panic(err)
	}

	for _, line := range lines {
		linesWaitGroups.Add(1)
		go processLine(line)
	}

	linesWaitGroups.Wait()
	println(sumOfPossibleEquations.Load())
	println(sumOfConcatEquations.Load())
}
