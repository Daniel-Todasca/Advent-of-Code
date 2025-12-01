package puzzles

import util.*

import java.io.File

val bits = mapOf("0" to "0000", "1" to "0001", "2" to "0010", "3" to "0011",
    "4" to "0100", "5" to "0101", "6" to "0110", "7" to "0111", "8" to "1000",
    "9" to "1001", "A" to "1010", "B" to "1011", "C" to "1100", "D" to "1101",
    "E" to "1110", "F" to "1111")

var idx = 0
var ans1 = 0

private fun parse(input: String) {
    val version = input.subSequence(idx, idx + 3)
    idx += 3

    ans1 += Integer.parseInt(version.toString(), 2)

    val type = input.subSequence(idx, idx + 3)
    idx += 3
    if (type == "100") {
        var size = 0
        if (input[idx] == '1') {
            idx += 5
            size += 5
        }
        else {
            while (size % 4 != 0) {
                size ++
                idx ++
            }
        }
    }
    else {
        val length = input.subSequence(idx, idx + 1)
        idx ++
        if (length == "0") {
            val plength = Integer.parseInt(input.subSequence(idx, idx + 15).toString(), 2)
            idx += 15
            val idx2 = idx
            while (idx - idx2 != plength) {
                println(idx)
                parse(input)
                println(idx)
            }
        }
        else if (length == "1") {
            val no = Integer.parseInt(input.subSequence(idx, idx + 11).toString(), 2)
            idx += 11
            for (i in 0 until no) parse(input)
        }
    }
}

private fun main() {
    val input = File(getInputPath(16)).readLines()[0].toCharArray().map { bits[it.toString()] }.joinToString("")
    parse(input)
    println(ans1)
}