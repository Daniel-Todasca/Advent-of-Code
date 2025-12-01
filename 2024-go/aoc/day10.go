package main

var heightmap []string
var heightrows, heightcols int
var trailroads [][]int
var ddir_x = []int{-1, 0, 1, 0}
var ddir_y = []int{0, -1, 0, 1}

func BFS(row int, col int, num int) int {
	queue := make(chan int, heightrows*heightcols)
	defer close(queue)

	queue <- row*heightcols + col
	visited := make([]bool, heightrows*heightcols)
	var totalNines = 0

	for len(queue) > 0 {
		current := <-queue
		row, col := current/heightcols, current%heightcols
		num := heightmap[row][col] - '0'

		if num == 9 {
			totalNines++
			continue
		}

		for dir := 0; dir < 4; dir++ {
			nextRow, nextCol := row+ddir_x[dir], col+ddir_y[dir]
			if nextRow < 0 || nextCol < 0 || nextRow >= heightrows || nextCol >= heightcols {
				continue
			}
			/* comment out for part1
			if visited[nextRow*heightcols+nextCol] {
				continue
			}
			*/
			if heightmap[nextRow][nextCol]-'0' == byte(num+1) {
				visited[nextRow*heightcols+nextCol] = true
				queue <- nextRow*heightcols + nextCol
			}
		}
	}

	return totalNines
}

func initializeTrailroads() {
	heightrows = len(heightmap)
	heightcols = len(heightmap[0])
	trailroads = make([][]int, heightrows)
	for row := range heightmap {
		trailroads[row] = make([]int, heightcols)
		for col := range heightmap[row] {
			trailroads[row][col] = -1
		}
	}
}

func main() {
	var err error
	heightmap, err = aocReadFile("./inputs/day10/input.txt")
	if err != nil {
		panic(err)
	}

	initializeTrailroads()

	totalTrails := 0
	for row := range heightmap {
		for col := range heightmap[row] {
			if heightmap[row][col] == '0' {
				totalTrails += BFS(row, col, 0)
			}
		}
	}

	println(totalTrails)
}
