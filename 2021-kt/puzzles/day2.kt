package puzzles

import java.io.File
import java.lang.IllegalStateException

import util.*

private class Command constructor(val dir: String, val units: Int) {
    fun next (gps: Triple <Int, Int, Int> = Triple (0, 0, 0)): Triple <Int, Int, Int> {
        return when (dir) {
            "forward" ->    Triple(gps.first + units, gps.second + units * gps.third, gps.third)
            "down" ->       Triple(gps.first, gps.second, gps.third + units)
            "up" ->         Triple(gps.first, gps.second, gps.third - units)
            else ->         throw IllegalStateException("$dir is not valid direction")
        }
    }
}

private fun main() {
    val cmds = File(getInputPath(2)).readLines().map { line ->
        val arr = line.split(" ")
        Command(arr[0], arr[1].toInt())
    }

    var gps = Triple (0, 0, 0)
    cmds.forEach { cmd -> gps = cmd.next(gps) }

    val ans = gps.first * gps.second
    println(ans)
    File(getOutputPath(2)).printWriter().use { out -> out.write(ans.toString()) }
}