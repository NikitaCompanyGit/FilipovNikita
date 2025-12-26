package lab6

object Tasks {
  case class SalesRecord(category: String, amount: Double)

  // Задание 1: Анализ продаж
  def analyzeSales(sales: List[SalesRecord]): Map[String, (Double, Int)] = {
    sales.groupBy(_.category).map { case (cat, records) =>
      val totalAmount = records.map(_.amount).sum
      val count = records.length
      cat -> (totalAmount, count)
    }
  }

  // Задание 2: Цепочка обработки (Option pipeline)
  // Упростим: если число четное -> делим на 2 -> если больше 10 -> успех
  def processNumber(n: Int): Option[Int] = {
    for {
      even <- if (n % 2 == 0) Some(n) else None
      halved = even / 2
      result <- if (halved > 10) Some(halved) else None
    } yield result
  }
}
