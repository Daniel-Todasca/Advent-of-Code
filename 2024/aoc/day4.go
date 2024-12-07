package main

import (
	"strings"
	"sync"
	"sync/atomic"
)

var dir_row = []int8{-1, -1, -1, 0, 0, 1, 1, 1}
var dir_col = []int8{-1, 0, 1, -1, 1, -1, 0, 1}
var xmasCount atomic.Int32
var xmasGroup sync.WaitGroup

func countXmas(row int, col int, matrix []string) {
	total := 0
	for idx, row_offset := range dir_row {
		col_offset := dir_col[idx]
		var buffer strings.Builder
		row2 := row
		col2 := col

		for i := 0; i < 4; i++ {
			if !(0 <= row2 && row2 < len(matrix)) || !(0 <= col2 && col2 < len(matrix[0])) {
				break
			}
			buffer.WriteByte(matrix[row2][col2])
			row2 += int(row_offset)
			col2 += int(col_offset)
		}

		word := buffer.String()
		// out of bounds while iterating
		if len(word) != 4 {
			continue
		}
		// we check just XMAS, the SAMX entries would be numbered twice for the symmetric function call
		if word == "XMAS" {
			total++
		}
	}
	xmasCount.Add(int32(total))
	xmasGroup.Done()
}

var mas_row = []int8{-1, 0, 1, 1, -1}
var mas_col = []int8{-1, 0, 1, -1, 1}
var masCount atomic.Int32
var masGroup sync.WaitGroup

func countMas(row int, col int, matrix []string) {
	var buffer strings.Builder
	for idx, row_offset := range mas_row {
		col_offset := mas_col[idx]
		row2 := row + int(row_offset)
		col2 := col + int(col_offset)

		if !(0 <= row2 && row2 < len(matrix)) || !(0 <= col2 && col2 < len(matrix[0])) {
			break
		}
		buffer.WriteByte(matrix[row2][col2])
	}
	word := buffer.String()

	// diferent variations (MAS-MAS, MAS-SAM, SAM-MAS, SAM-SAM)
	if word == "MASMS" || word == "MASSM" || word == "SAMMS" || word == "SAMSM" {
		masCount.Add(1)
	}
	masGroup.Done()
}

func main() {
	matrix, err := aocReadFile("./inputs/day4/input.txt")
	if err != nil {
		panic(err)
	}

	for row, line := range matrix {
		for col, _ := range line {
			xmasGroup.Add(1)
			go countXmas(row, col, matrix)
			masGroup.Add(1)
			go countMas(row, col, matrix)
		}
	}

	xmasGroup.Wait()
	masGroup.Wait()
	println(xmasCount.Load())
	println(masCount.Load())
}
