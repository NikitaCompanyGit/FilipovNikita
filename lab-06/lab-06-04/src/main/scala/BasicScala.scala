package lab6

object BasicScala {
  val square: Int => Int = (x: Int) => x * x

  def factorial(n: Int): Int = {
    if (n <= 1) 1 else n * factorial(n - 1)
  }

  def run(): Unit = {
    println("\n--- Basic Scala ---")
    println(s"Square 5: ${square(5)}")
    println(s"Factorial 5: ${factorial(5)}")
  }
}
