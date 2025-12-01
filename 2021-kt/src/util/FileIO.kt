package util

fun getInputPath(day: Int): String {
    return "src/input/day$day.in"
}

fun getOutputPath(day: Int): String {
    return "src/output/day$day.out"
}

private fun main() {
    assert(getInputPath(1) == "src/input/day1.in")
    assert(getOutputPath(22) == "src/output/day22.out")
}