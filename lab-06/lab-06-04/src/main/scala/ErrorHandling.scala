package lab6

object ErrorHandling {
  def divide(a: Int, b: Int): Option[Int] = {
    if (b == 0) None else Some(a / b)
  }

  def validate(age: Int): Either[String, Int] = {
    if (age < 18) Left("Too young") else Right(age)
  }

  def run(): Unit = {
    println("\n--- Error Handling ---")

    // Option
    println(s"Divide 10/2: ${divide(10, 2)}")
    println(s"Divide 10/0: ${divide(10, 0)}")

    // Either
    validate(15) match {
      case Left(err) => println(s"Validation failed: $err")
      case Right(age) => println(s"Welcome, age $age")
    }
  }
}
