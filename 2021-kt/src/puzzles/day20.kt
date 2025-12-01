package puzzles

import util.getInputPath
import util.getOutputPath

import java.io.*

private data class Pixel(val iter: Int, val x: Int, val y: Int)

private lateinit var alg: String
private lateinit var image: List <String>

private fun getZone(x: Int, y: Int): List <Pair <Int, Int>> {
    return listOf(Pair(x-1, y-1), Pair(x, y-1), Pair(x+1, y-1),
        Pair(x-1, y),   Pair(x, y),   Pair(x+1, y),
        Pair(x-1, y+1), Pair(x, y+1), Pair(x+1, y+1))
}

private fun characterIntValue(ch: Char): Int {
    return if (ch == '#') 1 else 0
}

private val memoPixels = HashMap<Pixel, Int> ()
private fun computePixel(iter: Int, x: Int, y: Int): Int {
    val pixel = Pixel(iter, x, y)
    if (pixel in memoPixels) return memoPixels.getValue(pixel)

    val ans = (
        if (iter == 0) {
            when {
                y !in image.indices -> 0
                x !in image[y].indices -> 0
                else -> characterIntValue(image[y][x])
            }
        }
        else {
            val bytes = getZone(x, y).map { pt -> computePixel(iter-1, pt.first, pt.second) }
                    .joinToString(separator = "")
            val num = Integer.parseInt(bytes, 2)
            characterIntValue(alg[num])
        })

    memoPixels[pixel] = ans
    return ans
}

private fun litPixels(iter: Int): Int {
    val x1 = -iter
    val x2 = image.size + iter
    val y1 = -iter
    val y2 = image[0].length + iter
    var ans = 0
    for (x in x1..x2)
        for (y in y1..y2) {
            ans += computePixel(iter, x, y)
        }
    return ans
}

private fun main() {
    val input = File(getInputPath(20)).readLines()
    alg = input[0]
    image = input.subList(2, input.size)

    val ans1 = litPixels(2)
    val ans2 = litPixels(50)

    println("$ans1 $ans2")
    File(getOutputPath(20)).printWriter().use { out -> out.write("$ans1 $ans2") }
}