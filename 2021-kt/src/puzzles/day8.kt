package puzzles

import util.*

import java.io.File

val easyDigits = arrayOf(2, 4, 3, 7)
val decoder = mapOf (
    "abcefg"    to 0, "cf"      to 1, "acdeg"   to 2,
    "acdfg"     to 3, "bcdf"    to 4, "abdfg"   to 5,
    "abdefg"    to 6, "acf"     to 7, "abcdefg" to 8,
    "abcdfg"    to 9
)

private fun main() {
    val entries = File(getInputPath(8)).readLines().map { entry -> entry.split("|") }
        .map { line -> Pair(line[0].split(' ').filter { it.isNotEmpty() },
                            line[1].split(' ').filter { it.isNotEmpty() }) }
    val ans1 = entries.map { entry -> entry.second.count { it.length in easyDigits }}.sum()
    val ans2 = entries.map { entry ->
        // a - 8, b - 6, c - 8, d- 7, e - 4, f - 9, g - 7
        val frequency = entry.first.map { it.toList() }.flatten().groupingBy { it }.eachCount()
        val b = frequency.filterValues { it == 6 }.keys.elementAt(0)
        val e = frequency.filterValues { it == 4 }.keys.elementAt(0)
        val f = frequency.filterValues { it == 9 }.keys.elementAt(0)
        val number1 = entry.first.filter { it.length == 2 }[0]
        val c = if (number1[0] == f) number1[1] else number1[0]
        val number4 = entry.first.filter { it.length == 4 }[0]
        val d = number4.first { it !in arrayOf(b, c, f) }
        val number7 = entry.first.filter { it.length == 3 }[0]
        val a = number7.first { it !in arrayOf(c, f) }
        val g = frequency.keys.first { it !in arrayOf(a, b, c, d, e, f)}

        val perm = mapOf(a to 'a', b to 'b', c to 'c', d to 'd', e to 'e', f to 'f', g to 'g')

        entry.second.map { it2 -> decoder[CharArray(it2.length) { perm[it2[it]]!! }.sorted().joinToString("")] }
            .reduce { acc, i -> acc!!*10 + i!! }!!.toInt()
    }.sum()

    println("$ans1 $ans2")
    File(getOutputPath(8)).printWriter().use{ out -> out.write("$ans1 $ans2") }
}