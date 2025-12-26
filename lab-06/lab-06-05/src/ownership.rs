pub fn run() {
    println!("\n=== Ownership & Borrowing ===");

    // 1. Перемещение (Move)
    let s1 = String::from("Hello");
    let s2 = s1;
    // println!("{}", s1); // Ошибка: s1 перемещена в s2
    println!("Moved: s2 = {}", s2);

    // 2. Клонирование (Clone)
    let s3 = s2.clone();
    println!("Cloned: s2 = {}, s3 = {}", s2, s3);

    // 3. Заимствование (Borrowing)
    let len = calculate_len(&s3); // Передаем ссылку, а не владение
    println!("Length of '{}' is {}", s3, len);
}

fn calculate_len(s: &String) -> usize {
    s.len()
}
