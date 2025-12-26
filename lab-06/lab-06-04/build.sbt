name := "lab6-scala"

version := "0.1"

scalaVersion := "2.13.18"

// Зависимости для Spark
libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.5.0",
  "org.apache.spark" %% "spark-sql" % "3.5.0"
)

// Отключаем логирование Spark при запуске (слишком много шума в консоли)
fork := true
javaOptions ++= Seq("-Dlog4j.configuration=log4j.properties")
