package puzzles

import util.*

import java.io.File

private fun gaussSum(n: Int): Int{
    return n * (n+1) / 2
}

private fun main() {
    val crabs = File(getInputPath(7)).readLines()[0].split(",").map { it.toInt() }.sorted()

    val min = crabs[0]
    val max = crabs.last()
    var fuel = crabs.sum() - min * crabs.size
    var ans1 = fuel

    var ptr = 0
    while (ptr < crabs.size && crabs[ptr] <= min) ptr += 1

    var leftCost = ptr
    var fuel2 = crabs.map { gaussSum(it - min) }.sum()
    var rightCost = crabs.map { it - min }.sum()
    var ans2 = fuel2

    for (value in min+1..max) {
        fuel -= crabs.size - ptr
        fuel += ptr

        fuel2 += leftCost
        fuel2 -= rightCost
        rightCost -= crabs.size - ptr
        while (ptr < crabs.size && crabs[ptr] <= value) ptr += 1
        leftCost += ptr
        
        if (fuel < ans1) ans1 = fuel
        if (fuel2 < ans2) ans2 = fuel2
    }

    println("$ans1 $ans2")
    File(getOutputPath(7)).printWriter().use { out -> out.write("$ans1 $ans2") }
}