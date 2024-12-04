package main

import (
	"bufio"
	"os"
	"strconv"
)

func aocReadFile(filename string) ([]string, error) {
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

func aocAbs(num int) int {
	if num < 0 {
		return -num
	}
	return num
}

func aocStringSliceToIntSlice(slice []string) ([]int, error) {
	var intSlice []int
	for _, str := range slice {
		num, err := strconv.Atoi(str)
		if err != nil {
			return nil, err
		}
		intSlice = append(intSlice, num)
	}
	return intSlice, nil
}
