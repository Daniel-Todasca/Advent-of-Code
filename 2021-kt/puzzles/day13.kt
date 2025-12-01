package puzzles

import util.*

import java.io.File

private fun fold(point: Pair<Int,Int>, changes:List<Pair<Char,Int>>): Pair<Int,Int> {
    var ans = point
    for (change in changes) {
        if (change.first == 'x' && change.second < ans.first)
            ans = Pair(2*change.second - ans.first, ans.second)
        else if (change.first == 'y' && change.second < ans.second)
            ans = Pair(ans.first, 2*change.second - ans.second)
    }
    return ans
}

private fun fold(points: List<Pair<Int,Int>>, changes:List<Pair<Char,Int>>): List <Pair<Int,Int>> {
    return points.map { fold(it, changes) }.distinct()
}

private fun main() {
    val inputFile = File(getInputPath(12)).readLines()
    val points = inputFile.mapNotNull { line -> Regex("(\\d+),(\\d+)").find(line) }
        .map { it.destructured.toList() }.map { Pair(it[0].toInt(), it[1].toInt()) }
    val changes = inputFile.mapNotNull { line -> Regex("fold along ([x|y])=(\\d+)").find(line) }
        .map { it.destructured.toList() }.map { Pair(it[0].single(), it[1].toInt()) }

    val ans1 = fold(points, listOf(changes[0])).size
    var output = fold(points, changes)

    val minX = output.minOf { it.first }
    val minY = output.minOf { it.second }
    output = output.map { Pair(it.first - minX, it.second - minY) }

    File("src/draw/points.in").printWriter()
        .use { out ->
            out.write(output.joinToString("\n") { it.first.toString() + " " + it.second })
        }

    val ans2 = "PZFJHRFZ"

    println("$ans1 $ans2")
    File(getOutputPath(13)).printWriter().use { out -> out.write("$ans1 $ans2") }
}