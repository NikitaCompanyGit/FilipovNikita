package lab6

object PatternMatching {
  sealed trait Payment
  case class Card(number: String) extends Payment
  case class Cash(amount: Double) extends Payment

  def process(p: Payment): String = p match {
    case Card(n) if n.startsWith("4") => s"Visa card: $n"
    case Card(n) => s"Unknown card: $n"
    case Cash(a) => s"Cash payment: $a"
  }

  def run(): Unit = {
    println("\n--- Pattern Matching ---")
    println(process(Card("4111222233334444")))
    println(process(Cash(50.0)))
  }
}
