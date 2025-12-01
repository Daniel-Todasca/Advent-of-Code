package puzzles

import util.*

import java.io.File
import kotlin.math.sign

data class Line(val begin: Pair <Int, Int>, val end: Pair <Int, Int>)

private fun main() {
    val lines = File(getInputPath(5)).readLines().map { line ->
        val (x1, y1, x2, y2) = Regex("(\\d+),(\\d+) -> (\\d+),(\\d+)").find(line)!!.destructured.toList().map { Integer.parseInt(it) }
        Line(Pair(x1, y1), Pair(x2, y2))
    }

    val frequency1 = HashMap<Pair<Int, Int>, Int> ().withDefault { 0 }
    val frequency2 = HashMap<Pair<Int, Int>, Int> ().withDefault { 0 }

    for (line in lines) {
        var (x, y) = line.begin
        val stepX = sign((line.end.first - line.begin.first).toDouble()).toInt()
        val stepY = sign((line.end.second - line.begin.second).toDouble()).toInt()
        while (true) {
            if (stepX * stepY == 0)
                frequency1[Pair(x, y)] = frequency1.getValue(Pair(x, y)) + 1
            frequency2[Pair(x, y)] = frequency2.getValue(Pair(x, y)) + 1
            if (x == line.end.first && y == line.end.second) break
            x += stepX
            y += stepY
        }
    }

    val ans1 = frequency1.count { it.value > 1 }
    val ans2 = frequency2.count { it.value > 1 }

    println("$ans1 $ans2")
    File(getOutputPath(5)).printWriter().use { out -> out.write("$ans1 $ans2") }
}