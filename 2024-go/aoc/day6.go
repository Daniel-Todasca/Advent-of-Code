package main

type direction int

const (
	up int = iota
	right
	down
	left
)

var pos_x, pos_y = 0, 0
var start_x, start_y = 0, 0
var dir = up
var rows, cols = 0, 0
var dir_x = []int8{-1, 0, 1, 0}
var dir_y = []int8{0, 1, 0, -1}
var block_x, block_y = -1, -1
var positions map[int]struct{} = make(map[int]struct{})

func findInitialPosition(matrix []string) {
	rows = len(matrix)
	cols = len(matrix[0])
	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			if matrix[row][col] == '^' {
				pos_x, pos_y = row, col
				start_x, start_y = row, col
				return
			}
		}
	}
	panic("Starting position not found")
}

func outOfBounds(x int, y int) bool {
	if x < 0 || y < 0 || x >= rows || y >= cols {
		return true
	}
	return false
}

func moveToNextPosition(matrix []string) {
	x2, y2 := pos_x+int(dir_x[dir]), pos_y+int(dir_y[dir])
	if !outOfBounds(x2, y2) && (matrix[x2][y2] == '#' || (block_x == x2 && block_y == y2)) {
		dir = (dir + 1) % 4
		moveToNextPosition(matrix)
	} else {
		pos_x, pos_y = x2, y2
	}
}

func _main6() {
	matrix, err := aocReadFile("./inputs/day6/input.txt")
	if err != nil {
		panic(err)
	}

	findInitialPosition(matrix)
	for !outOfBounds(pos_x, pos_y) {
		positions[pos_x*10000+pos_y] = struct{}{}
		moveToNextPosition(matrix)
	}

	println(len(positions))

	totalOptions := 0
	for key, _ := range positions {
		block_x, block_y = key/10000, key%10000
		if block_x == start_x && block_y == start_y {
			continue
		}
		if matrix[block_x][block_y] == '#' {
			continue
		}
		pos_x = start_x
		pos_y = start_y
		dir = up

		var states map[int]struct{} = make(map[int]struct{})
		for !outOfBounds(pos_x, pos_y) {
			key = pos_x*10000 + pos_y*4 + dir
			_, exists := states[key]
			if exists {
				break
			}
			states[key] = struct{}{}
			moveToNextPosition(matrix)
		}

		if !outOfBounds(pos_x, pos_y) {
			totalOptions++
		}
	}

	println(totalOptions)
}
