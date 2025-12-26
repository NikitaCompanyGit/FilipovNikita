package lab6

object Collections {
  case class Product(name: String, price: Double, category: String)

  val products = List(
    Product("iPhone", 999.0, "electronics"),
    Product("T-Shirt", 20.0, "clothing"),
    Product("MacBook", 2000.0, "electronics")
  )

  def run(): Unit = {
    println("\n--- Collections ---")
    val electronics = products.filter(_.category == "electronics")
    println(s"Electronics count: ${electronics.length}")

    val totalCost = products.map(_.price).sum
    println(s"Total cost: $totalCost")
  }
}
