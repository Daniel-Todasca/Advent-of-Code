package main

import "fmt"

type Coord2D struct {
	row, col int
}

var antennaMap = make(map[rune][]Coord2D)
var matrix [][]rune

func findAntennas(matrix [][]rune) {
	for row, line := range matrix {
		for col, char := range line {
			if char != '.' {
				antennaMap[char] = append(antennaMap[char], Coord2D{row: row, col: col})
			}
		}
	}

	for key, coords := range antennaMap {
		fmt.Printf("%c: %v\n", key, coords)
	}
}

func checkPosition(pos Coord2D, char rune) bool {
	n_rows := len(matrix)
	n_cols := len(matrix[0])
	if pos.row < 0 || pos.col < 0 {
		return false
	}
	if pos.row >= n_rows || pos.col >= n_cols {
		return false
	}

	if char == '#' {
		matrix[pos.row][pos.col] = '#'
	} else if matrix[pos.row][pos.col] != '#' {
		matrix[pos.row][pos.col] = char
	}
	return true
}

func checkPair(antenna Coord2D, other Coord2D) {
	row_diff, col_diff := other.row-antenna.row, other.col-antenna.col
	checkPosition(Coord2D{row: antenna.row - row_diff, col: antenna.col - col_diff}, '#')
	checkPosition(Coord2D{row: other.row + row_diff, col: other.col + col_diff}, '#')

	x, y := antenna.row, antenna.col
	for checkPosition(Coord2D{row: x, col: y}, '%') {
		x -= row_diff
		y -= col_diff
	}

	x, y = other.row, other.col
	for checkPosition(Coord2D{row: x, col: y}, '%') {
		x += row_diff
		y += col_diff
	}
}

func main() {
	lines, err := aocReadFile("./inputs/day8/input.txt")
	if err != nil {
		panic(err)
	}

	matrix = make([][]rune, len(lines))
	for idx, line := range lines {
		matrix[idx] = []rune(line)
	}

	findAntennas(matrix)

	for _, coords := range antennaMap {
		for i := 0; i < len(coords); i++ {
			for j := i + 1; j < len(coords); j++ {
				checkPair(coords[i], coords[j])
			}
		}
	}

	for _, line := range matrix {
		println(string(line))
	}

	totalAntinodes := 0
	totalExtendedAntinodes := 0
	for _, line := range matrix {
		for _, char := range line {
			if char == '#' {
				totalAntinodes++
				totalExtendedAntinodes++
			} else if char == '%' {
				totalExtendedAntinodes++
			}
		}
	}
	println(totalAntinodes)
	println(totalExtendedAntinodes)
}
