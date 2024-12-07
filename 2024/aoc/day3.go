package main

import (
	"regexp"
	"strconv"
	"strings"
)

func getStatements(line string) []string {
	pattern := "mul\\(\\d+\\,\\d+\\)|do\\(\\)|don't\\(\\)"
	re, err := regexp.Compile(pattern)
	if err != nil {
		panic("Regex could not be compiled")
	}

	return re.FindAllString(line, -1)
}

func _main3() {
	lines, err := aocReadFile("./inputs/day3/input.txt")
	if err != nil {
		panic(err)
	}

	var total1 int64 = 0
	var total2 int64 = 0
	disableMuls := false
	for _, line := range lines {
		statements := getStatements(line)
		for _, statement := range statements {
			if strings.Contains(statement, "don't") {
				disableMuls = true
				continue
			}

			if strings.Contains(statement, "do") {
				disableMuls = false
				continue
			}

			// println(strings.Split(strings.Split(mul, "(")[1], ",")[0])
			// println(strings.Split(strings.Split(mul, ")")[0], ",")[1])

			num1, err := strconv.Atoi(strings.Split(strings.Split(statement, "(")[1], ",")[0])
			if err != nil {
				panic("Wrong parsing 1: " + statement)
			}
			num2, err := strconv.Atoi(strings.Split(strings.Split(statement, ")")[0], ",")[1])
			if err != nil {
				panic("Wrong parsing 2: " + statement)
			}

			mul := int64(num1) * int64(num2)
			total1 += mul
			if !disableMuls {
				total2 += mul
			}
		}
	}

	println(total1)
	println(total2)
}
