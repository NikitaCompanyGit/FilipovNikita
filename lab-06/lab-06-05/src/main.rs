// Объявляем модули (файлы должны лежать рядом в папке src)
mod ownership;
mod iterators;
mod patterns;
mod errors;
mod tasks;

use tasks::{Product, Fibonacci};

fn main() {
    println!("=== LAB 6: RUST & SYSTEMS FP ===");

    // Запуск теории
    ownership::run();
    iterators::run();
    patterns::run();
    errors::run();

    println!("\n=== PRACTICAL TASKS ===");

    // Тест Задания 1
    let products = vec![
        Product { name: "Laptop".to_string(), price: 1500.0, in_stock: true },
        Product { name: "Mouse".to_string(), price: 50.0, in_stock: true },
        Product { name: "Monitor".to_string(), price: 300.0, in_stock: false },
    ];

    let (avg, available, expensive) = tasks::analyze_products(&products);
    println!("Avg Price: {:.2}", avg);
    println!("Available Count: {}", available);
    println!("Expensive Items (>100): {:?}", expensive);

    // Тест Задания 3
    println!("\nFibonacci first 10:");
    let fib: Vec<u64> = Fibonacci::new().take(10).collect();
    println!("{:?}", fib);
}
