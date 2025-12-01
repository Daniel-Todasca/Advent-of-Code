package puzzles

import util.*

import java.io.File
import java.util.Scanner

private class BingoCard constructor(val bingoArray: ArrayList<Int>) {
    private fun getRow(row: Int): List <Int> {
        return bingoArray.subList(row * 5, row * 5 + 5)
    }

    private fun getColumn(col: Int): List <Int> {
        return bingoArray.slice(col..24 step 5)
    }

    fun getScore(order: Map <Int, Int>): Pair <Int, Int> {
        var round = 0
        val candidates = ArrayList <List <Int>> ()
        for (i in 0 until 5) {
            candidates.add(getRow(i))
            candidates.add(getColumn(i))
        }

        while (true) {
            val done = candidates.any { candidate -> (candidate.map { order[it]}.maxByOrNull { it!! }!! <= round) }
            val sum = bingoArray.sumBy { if (order[it]!! > round) it else 0 }
            if (done) return Pair(round, sum)
            round += 1
        }
    }
}

private val cards = ArrayList <BingoCard> ()
lateinit var order: Map <Int, Int>

private fun parseInput() {
    val scanner = Scanner(File(getInputPath(4)).bufferedReader())
    order = scanner.nextLine().split(",").map { it.toInt() }.withIndex().associate { it.value to it.index }
    while (scanner.hasNextLine()) {
        scanner.nextLine()
        val bingoArray = ArrayList<Int> ()
        for (i in 0 until 25)
            bingoArray.add(scanner.nextInt())
        cards.add(BingoCard(bingoArray))
    }
    scanner.close()
}

private fun main() {
    parseInput()
    val results = cards.map { it.getScore(order) }.sortedBy { it.first }

    val ans1 = results[0]       .second * order.keys.elementAt(results[0]       .first)
    val ans2 = results.last()   .second * order.keys.elementAt(results.last()   .first)

    println(ans1)
    println(ans2)

    File(getOutputPath(4)).printWriter().use { out -> out.write("$ans1 $ans2") }
}