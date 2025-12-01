package puzzles

import util.*

import java.io.File

typealias Stack<T> = MutableList<T>
fun <T> Stack<T>.push(item: T) = add(item)
fun <T> Stack<T>.pop(): T? = if (isNotEmpty()) removeAt(lastIndex) else null
fun <T> Stack<T>.peek(): T? = if (isNotEmpty()) last() else null

val bracketsPair = mapOf("(".single() to ")".single(),
    "[".single() to "]".single(),
    "{".single() to "}".single(),
    "<".single() to ">".single())

private fun getCorruptionScore(line: String): Int {
    val score = mapOf(")".single() to 3,
        "]".single() to 57,
        "}".single() to 1197,
        ">".single() to 25137)

    val stack = mutableListOf<Char>()
    line.forEach { ch ->
        if (ch in bracketsPair.keys)
            stack.push(ch)
        else {
            if (bracketsPair[stack.peek()] != ch)
                return score[ch]!!
            stack.pop()
        }
    }
    return 0
}

private fun getIncompleteScore(line: String): Long {
    val score = mapOf(")".single() to 1,
        "]".single() to 2,
        "}".single() to 3,
        ">".single() to 4)

    val stack = mutableListOf<Char>()
    line.forEach { ch ->
        if (ch in bracketsPair.keys) stack.push(ch)
        else stack.pop()
    }

    return stack.map { bracketsPair[it] }.reversed().map { score[it]!!.toLong() }.reduce { acc, i -> acc*5 + i }
}

private fun main() {
    var input = File(getInputPath(10)).readLines()
    val ans1 = input.map { getCorruptionScore(it) }.sum()
    input = input.filter { getCorruptionScore(it) == 0 }
    val scores = input.map { getIncompleteScore(it) }.sorted().toList()
    val ans2 = scores[scores.size / 2]

    println("$ans1 $ans2")
    File(getOutputPath(10)).printWriter().use { out -> out.write("$ans1 $ans2") }
}