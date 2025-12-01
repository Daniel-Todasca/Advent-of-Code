package puzzles

import util.*

import java.io.File

private fun bigger(heightmap: List<List<Int>>, x1: Int, y1: Int, x2: Int, y2: Int): Boolean {
    if (x2 !in heightmap.indices || y2 !in heightmap[x2].indices) return false
    return heightmap[x1][y1] >= heightmap[x2][y2]
}

private fun fill(heightmap: List<List<Int>>, visited: List<MutableList<Boolean>>, x: Int, y: Int): Int {
    if (x !in heightmap.indices || y !in heightmap[x].indices) return 0
    if (heightmap[x][y] == 9) return 0
    if (visited[x][y]) return 0
    visited[x][y] = true
    var ans = 1
    ans += fill(heightmap, visited, x, y+1)
    ans += fill(heightmap, visited, x, y-1)
    ans += fill(heightmap, visited, x+1, y)
    ans += fill(heightmap, visited, x-1, y)
    return ans
}

private fun main() {
    val heightmap = File(getInputPath(9)).readLines().map { line -> line.toCharArray().map { Character.getNumericValue(it) } }

    var ans1 = 0
    for (row in heightmap.indices) {
        for (column in heightmap[row].indices) {
            if (bigger(heightmap, row, column, row, column-1)) continue
            if (bigger(heightmap, row, column, row, column+1)) continue
            if (bigger(heightmap, row, column, row-1, column)) continue
            if (bigger(heightmap, row, column, row+1, column)) continue
            ans1 += heightmap[row][column] + 1
        }
    }

    val sizes = ArrayList <Int> ()
    val visited = heightmap.map { line -> line.map { false }.toMutableList() }
    for (row in heightmap.indices) {
        for (column in heightmap[row].indices) {
            if (visited[row][column]) continue
            if (heightmap[row][column] == 9) continue
            sizes.add(fill(heightmap, visited, row, column))
        }
    }

    val ans2 = sizes.sortedBy{ -it }.subList(0, 3).reduce { acc, i -> acc*i }
    println("$ans1 $ans2")
    File(getOutputPath(9)).printWriter().use { out -> out.write("$ans1 $ans2") }
}