package puzzles

import util.*

import java.io.File

private fun main() {
    val energy = File(getInputPath(11)).readLines().map { line -> line.toCharArray().map{ Character.getNumericValue(it) }.toMutableList()}

    val cntSteps = 200000
    var ans1 = 0
    var ans2 = 0

    for (iter in 0 until cntSteps) {
        val flashed = energy.map { line -> line.map { false }.toMutableList() }

        for (i in 0 until 10)
            for (j in 0 until 10)
                energy[i][j] += 1

        var hasChanges = true
        while (hasChanges) {
            hasChanges = false
            for (i in 0 until 10) {
                for (j in 0 until 10) {
                    if (energy[i][j] > 9) {
                        if (flashed[i][j]) continue
                        hasChanges = true
                        if (iter < 100) ans1 += 1
                        flashed[i][j] = true

                        fun inc(x: Int, y: Int) {
                            if (x !in energy.indices) return
                            if (y !in energy[x].indices) return
                            energy[x][y] += 1
                        }

                        inc(i + 1, j + 1)
                        inc(i + 1, j)
                        inc(i + 1, j - 1)
                        inc(i, j + 1)
                        inc(i, j - 1)
                        inc(i - 1, j + 1)
                        inc(i - 1, j)
                        inc(i - 1, j - 1)
                    }
                }
            }
        }

        for (i in 0 until 10)
            for (j in 0 until 10)
                if (flashed[i][j])
                    energy[i][j] = 0

        if (flashed.map { line -> line.count { it }}.sum() == 100) {
            ans2 = iter + 1
            break
        }
    }

    println("$ans1 $ans2")
}