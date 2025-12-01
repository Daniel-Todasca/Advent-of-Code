package puzzles

import util.getInputPath
import util.getOutputPath

import java.io.File

private val edges = HashMap <String, MutableList <String>> ()

private fun addEdge(from: String, dest: String) {
    if (!edges.containsKey(from)) edges[from] = mutableListOf()
    edges[from]!!.add(dest)
}

private fun getPaths(src: String, dest: String, smallUsed: MutableSet <String> = mutableSetOf()): List <List <String>> {
    if (src == dest) return listOf (listOf(dest))
    val ans = mutableListOf<List <String>> ()
    if (Regex("^[a-z]+$").matches(src)) smallUsed.add(src)
    edges[src]!!.forEach { adj ->
        if (!smallUsed.contains(adj)) {
            getPaths(adj, dest, smallUsed.toMutableSet()).forEach {
                ans.add(listOf(src) + it)
            }
        }
    }
    return ans
}

private fun getPathsTwice(src: String = "start", twice: String? = null,
                          smallUsed: MutableSet <String> = mutableSetOf())
: List <List <String>> {
    if (src == "end") return listOf (listOf("end"))
    val ans = mutableListOf<List <String>> ()
    if (Regex("^[a-z]+$").matches(src)) smallUsed.add(src)
    edges[src]!!.forEach { adj ->
        if (adj != "start") {
            if (!smallUsed.contains(adj)) {
                getPathsTwice(adj, twice, smallUsed.toMutableSet()).forEach {
                    ans.add(listOf(src) + it)
                }
            }
            else if (twice == null) {
                getPathsTwice(adj, adj, smallUsed.toMutableSet()).forEach {
                    ans.add(listOf(src) + it)
                }
            }
        }
    }
    return ans
}

private fun main() {
    File(getInputPath(12)).readLines().map { it.split("-") }.forEach { pair ->
        addEdge(pair[0], pair[1])
        addEdge(pair[1], pair[0])
    }

    val paths = getPaths("start", "end")
    val ans1 = paths.size

    val paths2 = getPathsTwice()
    val ans2 = paths2.size

    println("$ans1 $ans2")
    File(getOutputPath(13)).printWriter().use { out -> out.write("$ans1 $ans2") }
}