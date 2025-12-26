pub fn run() {
    println!("\n=== Iterators ===");

    let numbers = vec![1, 2, 3, 4, 5];

    // Map & Filter & Collect
    let squares: Vec<i32> = numbers
        .iter()
        .map(|x| x * x)
        .filter(|x| x > &10)
        .collect();

    println!("Squares > 10: {:?}", squares);

    // Fold (Reduce)
    let sum: i32 = numbers.iter().fold(0, |acc, x| acc + x);
    println!("Sum: {}", sum);
}
