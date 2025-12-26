#[derive(Debug)]
pub struct Product {
    pub name: String,
    pub price: f64,
    pub in_stock: bool,
}

// Задание 1: Анализ продуктов
pub fn analyze_products(products: &[Product]) -> (f64, usize, Vec<&Product>) {
    let total_sum: f64 = products.iter().map(|p| p.price).sum();
    let count = products.len();
    let avg = if count > 0 { total_sum / count as f64 } else { 0.0 };

    let available_count = products.iter().filter(|p| p.in_stock).count();

    let expensive: Vec<&Product> = products
        .iter()
        .filter(|p| p.price > 100.0)
        .collect();

    (avg, available_count, expensive)
}

// Задание 3: Итератор Фибоначчи
pub struct Fibonacci {
    curr: u64,
    next: u64,
}

impl Fibonacci {
    pub fn new() -> Self {
        Fibonacci { curr: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        let new_next = self.curr + self.next;
        let result = self.curr;

        self.curr = self.next;
        self.next = new_next;

        Some(result)
    }
}
