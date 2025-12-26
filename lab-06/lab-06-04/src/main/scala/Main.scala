package lab6

object Main {
  def main(args: Array[String]): Unit = {
    println("=== LAB 6: SCALA & BIG DATA ===")

    BasicScala.run()
    Collections.run()
    ErrorHandling.run()
    PatternMatching.run()

    println("\n--- Practical Tasks ---")
    val sales = List(
      Tasks.SalesRecord("Books", 500),
      Tasks.SalesRecord("Books", 100),
      Tasks.SalesRecord("Electronics", 2000)
    )
    println(s"Sales Analysis: ${Tasks.analyzeSales(sales)}")

    println(s"Process Number (40): ${Tasks.processNumber(40)}") // Some(20)
    println(s"Process Number (10): ${Tasks.processNumber(10)}") // None (10/2 = 5 < 10)

    // Запуск Spark может занять время
    try {
      SparkExample.run()
    } catch {
      case e: Exception => println(s"\n[WARNING] Spark failed to start (expected on Windows without winutils): ${e.getMessage}")
    }
  }
}
