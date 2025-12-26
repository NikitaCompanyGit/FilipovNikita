pub fn run() {
    println!("\n=== Error Handling ===");

    // Option
    let numbers = vec![10, 20, 30];
    let first = numbers.get(0); // Some(10)
    let fourth = numbers.get(3); // None

    println!("First: {:?}, Fourth: {:?}", first, fourth);

    // Result
    match divide(10.0, 2.0) {
        Ok(res) => println!("10 / 2 = {}", res),
        Err(e) => println!("Error: {}", e),
    }

    match divide(10.0, 0.0) {
        Ok(res) => println!("10 / 0 = {}", res),
        Err(e) => println!("Error: {}", e),
    }
}

fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err(String::from("Division by zero"))
    } else {
        Ok(a / b)
    }
}
