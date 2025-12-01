package puzzles

import util.*

import java.io.File
import java.math.BigInteger

val memo = HashMap<Pair<Int, Int>, BigInteger> ()
private fun getSpawnCount(timer: Int, days: Int): BigInteger {
    val memoKey = Pair (timer, days)
    if (timer >= days) return BigInteger("1")
    if (memo.containsKey(memoKey)) return memo.getValue(memoKey)

    memo[memoKey] = getSpawnCount(6, days-timer-1) + getSpawnCount(8, days-timer-1)
    return memo.getValue(memoKey)
}

private fun main() {
    val timers = File(getInputPath(6)).readLines()[0].split(",").map { it.toInt() }
    val ans1 = timers.map { getSpawnCount(it, 80) }.reduce { acc, bigInteger -> acc + bigInteger }
    val ans2 = timers.map { getSpawnCount(it, 256) }.reduce { acc, bigInteger -> acc + bigInteger }
    println("$ans1 $ans2")
    File(getOutputPath(6)).printWriter().use { out -> out.write("$ans1 $ans2") }
}