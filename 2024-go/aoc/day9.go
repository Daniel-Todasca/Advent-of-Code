package main

import (
	"fmt"
)

type Sequence struct {
	idx, len, id int
}

var freePositions chan int
var diskMap []int
var diskSize int = 0
var totalUsedSpaces int = 0
var freeSequences []Sequence
var filledSequences []Sequence

func printDiskMap(diskMap []int) {
	for idx := 0; idx < diskSize; idx++ {
		if diskMap[idx] == -1 {
			fmt.Print(".")
		} else {
			fmt.Print(diskMap[idx])
		}
	}
	fmt.Println()
}

func processInput(line string) {
	diskMap = make([]int, len(line)*9)
	freePositions = make(chan int, len(line)*9)

	diskIndex := 0
	id := 0
	for idx := 0; idx < len(line); idx++ {
		num := int(line[idx] - '0')
		if num < 0 || num > 9 {
			panic(fmt.Sprintf("Error parsing %c", line[idx]))
		}

		if idx%2 == 0 {
			filledSequences = append(filledSequences, Sequence{idx: diskIndex, len: num, id: id})
			for size := 0; size < num; size++ {
				diskMap[diskIndex+size] = id
				totalUsedSpaces++
			}
			id++
		} else {
			freeSequences = append(freeSequences, Sequence{idx: diskIndex, len: num, id: id})
			for size := 0; size < num; size++ {
				diskMap[diskIndex+size] = -1
				freePositions <- (diskIndex + size)
			}
		}

		diskIndex += num
	}

	diskSize = diskIndex
	// printDiskMap(diskMap)
}

var filesystemChecksum int64 = 0

func moveToFreeSpaces() {
	idx := diskSize - 1
	for idx >= totalUsedSpaces {
		if diskMap[idx] == -1 {
			idx--
			continue
		}

		freeSpot, exists := <-freePositions
		if !exists {
			panic("Error while dequeuing")
		}
		diskMap[freeSpot] = diskMap[idx]
		diskMap[idx] = -1
		idx--
	}
}

func moveSequencesToFreeSpaces() {
	for idx := len(filledSequences) - 1; idx >= 0; idx-- {
		seq := filledSequences[idx]
		for idx2 := 0; idx2 < len(freeSequences); idx2++ {
			other := freeSequences[idx2]
			if other.idx <= seq.idx && seq.len <= other.len {
				freeSequences[idx2].len -= seq.len
				freeSequences[idx2].idx += seq.len
				for off := 0; off < seq.len; off++ {
					diskMap[seq.idx+off] = -1
					diskMap[other.idx+off] = seq.id
				}
				break
			}
		}
	}
}

func _main9() {
	lines, err := aocReadFile("./inputs/day9/input.txt")
	if err != nil {
		panic(err)
	}
	if len(lines) != 1 {
		panic("Input is wrong - should have a single line")
	}
	line := lines[0]

	processInput(line)
	// moveToFreeSpaces()
	moveSequencesToFreeSpaces()

	// printDiskMap(diskMap)
	for idx, val := range diskMap {
		if val == -1 {
			continue
		}
		filesystemChecksum += int64(val * idx)
	}

	println(filesystemChecksum)
}
