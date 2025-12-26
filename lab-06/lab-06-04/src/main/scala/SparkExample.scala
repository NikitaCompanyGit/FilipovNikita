package lab6

import org.apache.spark.sql.SparkSession

object SparkExample {
  def run(): Unit = {
    println("\n--- Apache Spark ---")

    // Инициализация (отключаем лишние логи)
    val spark = SparkSession.builder()
      .appName("Lab6")
      .master("local[*]") // Запуск локально на всех ядрах
      .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    import spark.implicits._

    val data = Seq(
      ("Java", 20000),
      ("Python", 100000),
      ("Scala", 3000)
    ).toDF("Language", "Users")

    data.show()

    val popular = data.filter($"Users" > 10000)
    println("Popular languages (>10k users):")
    popular.show()

    spark.stop()
  }
}
