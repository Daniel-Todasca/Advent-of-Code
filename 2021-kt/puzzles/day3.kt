package puzzles

import util.*

import java.io.File

private fun getOxygen(bits: List <String>, index: Int = 0): Int {
    if (bits.size == 1) return Integer.parseInt(bits[0], 2)
    val bit = bits.groupingBy { it[index] }.eachCount().maxWithOrNull(compareBy({it.value}, {it.key}))!!.key
    return getOxygen(bits.filter { it[index] == bit }, index + 1)
}

private fun getCO2(bits: List <String>, index: Int = 0): Int {
    if (bits.size == 1) return Integer.parseInt(bits[0], 2)
    val bit = bits.groupingBy { it[index] }.eachCount().minWithOrNull(compareBy({it.value}, {it.key}))!!.key
    return getCO2(bits.filter { it[index] == bit }, index + 1)
}

private fun main() {
    val bits = File(getInputPath(3)).readLines()
    val maxBit = bits[0].length

    var gamma = 0
    for (bitIndex in 0 until maxBit) {
        val bit = bits.groupingBy { it[maxBit - bitIndex - 1] }.eachCount().maxByOrNull { it.value }!!.key
        gamma += bit.toString().toInt() * (1 shl bitIndex)
    }

    val epsilon = ((1 shl maxBit) - 1) xor gamma
    val oxygen = getOxygen(bits)
    val co2 = getCO2(bits)

    val powerConsumption = gamma * epsilon
    val lifeSupport = oxygen * co2

    println("$powerConsumption $lifeSupport")
    File(getOutputPath(3)).printWriter().use { out -> out.write("$powerConsumption $lifeSupport") }
}