package puzzles

import util.*
import java.io.File
import java.util.*

open class SnailElement {
    var parent: SnailElement? = null
    open fun magnitude(): Long { return 0 }
    open fun copy(): SnailElement { return this }
}
class SnailNumber(var number: Int) : SnailElement() {
    override fun toString(): String = number.toString()

    fun split() {
        val pairParent = (parent as SnailPair)
        val halfPair = SnailPair(SnailNumber(number/2), SnailNumber((number+1)/2))
        halfPair.parent = pairParent
        if (pairParent.right == this) pairParent.right = halfPair
        else pairParent.left = halfPair
    }

    override fun magnitude(): Long { return number.toLong() }

    override fun copy(): SnailElement { return SnailNumber(number) }
}
class SnailPair(var left: SnailElement, var right: SnailElement) : SnailElement() {
    init {
        left.parent = this
        right.parent = this
    }
    override fun toString(): String = "[$left,$right]"

    fun isNumberPair(): Boolean {
        return left is SnailNumber && right is SnailNumber
    }

    private fun getPairParent(): SnailPair? {
        return if (parent != null) (parent as SnailPair) else null
    }

    private fun setZero() {
        if (parent == null) return
        if (parent !is SnailPair) return
        val cast = (parent as SnailPair)
        if (cast.left == this) {
            cast.left = SnailNumber(0)
            cast.left.parent = cast
        }
        else {
            cast.right = SnailNumber(0)
            cast.right.parent = cast
        }
    }

    private fun explodeUpdateLeft() {
        val leftValue = (this.left as SnailNumber).number
        var previous: SnailElement? = null
        var p: SnailPair? = this

        while (p != null) {
            if (p.getPairParent() != null && p.getPairParent()!!.right == p) {
                previous = p.getPairParent()!!.left
                while (previous is SnailPair)
                    previous = previous.right
                break
            }
            p = p.getPairParent()
        }
        if (previous is SnailNumber) previous.number += leftValue
    }

    private fun explodeUpdateRight() {
        val rightValue = (right as SnailNumber).number
        var next: SnailElement? = null
        var p: SnailPair? = this

        while (p != null) {
            if (p.getPairParent() != null && p.getPairParent()!!.left == p) {
                next = p.getPairParent()!!.right
                while (next is SnailPair)
                    next = next.left
                break
            }
            p = p.getPairParent()
        }
        if (next is SnailNumber) next.number += rightValue
    }

    fun explode() {
        explodeUpdateLeft()
        explodeUpdateRight()
        setZero()
    }

    override fun magnitude(): Long {
        return left.magnitude() * 3 + right.magnitude() * 2
    }

    override fun copy(): SnailElement { return SnailPair(left.copy(), right.copy()) }
}

private fun parseLine(line: String): SnailPair {
    val stack = Stack <SnailElement> ()
    line.toCharArray().forEach { ch ->
        when {
            Regex("[0-9]").matches(ch.toString()) ->
                stack.add(SnailNumber(Character.getNumericValue(ch)))
            ch == ']' -> {
                val pop1 = stack.pop()
                val pop2 = stack.pop()
                stack.add(SnailPair(pop2, pop1))
            }
        }
    }
    return (stack.first() as SnailPair)
}

private fun findLeftmostExplode(snail: SnailElement, depth: Int = 0): SnailPair? {
    when (snail) {
        is SnailNumber -> return null
        is SnailPair -> {
            if (depth >= 4 && snail.isNumberPair())
                return snail
            return findLeftmostExplode(snail.left, depth + 1) ?: return findLeftmostExplode(snail.right, depth + 1)
        }
    }
    return null
}

private fun findLeftmostSplit(snail: SnailElement): SnailNumber? {
    when (snail) {
        is SnailPair -> return findLeftmostSplit(snail.left) ?: return findLeftmostSplit(snail.right)
        is SnailNumber -> {
            if (snail.number >= 10)
                return snail
        }
    }
    return null
}

private fun sumPairs(pair1: SnailPair, pair2: SnailPair): SnailPair {
    val finalNumber = SnailPair(pair1, pair2)
    while (true) {
        val explode = findLeftmostExplode(finalNumber)
        if (explode != null) {
            explode.explode()
        }
        else {
            val split = findLeftmostSplit(finalNumber)
            if (split != null) {
                split.split()
            }
            else break
        }
    }
    return finalNumber
}

private fun main() {
    val input = File(getInputPath(18)).readLines().map { parseLine(it) }

    val finalNumber = input.reduce { acc, snailElement -> sumPairs(acc.copy() as SnailPair, snailElement.copy() as SnailPair) }

    val ans1 = finalNumber.magnitude()
    val ans2 = input.map { p1 -> input.map { p2 -> sumPairs(p1.copy() as SnailPair, p2.copy() as SnailPair).magnitude()}
        .maxOf { it } }.maxOf { it }

    println("$ans1 $ans2")
    File(getOutputPath(18)).printWriter().use { out -> out.write("$ans1 $ans2") }
}