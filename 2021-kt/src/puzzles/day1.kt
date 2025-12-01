package puzzles

import java.io.File

import util.*

private fun getIncreasingConsecutivePairs(list: List<Int>): Int {
    return list.zipWithNext().count { it.first < it.second }
}

private fun adjacentSums(list: List<Int>, window: Int): List <Int> {
    val ans = ArrayList <Int> ()
    var sum = list.subList(0, window).sum()
    ans.add(sum)
    for (i in window until list.size) {
        sum -= list[i-window]
        sum += list[i]
        ans.add(sum)
    }
    return ans
}

private fun main() {
    val depths = File(getInputPath(1)).readLines().map { it.toInt() }
    val output = File(getOutputPath(1)).printWriter()

    val ans1 = getIncreasingConsecutivePairs(depths)
    val ans2 = getIncreasingConsecutivePairs(adjacentSums(depths, 3))

    println(ans1)
    println(ans2)

    output.write("$ans1 $ans2")
    output.close()
}