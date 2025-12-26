enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

pub fn run() {
    println!("\n=== Pattern Matching ===");

    let msg = Message::Move { x: 10, y: 20 };
    process_message(msg);
    process_message(Message::Write(String::from("Rust")));
    process_message(Message::Quit);
}

fn process_message(msg: Message) {
    match msg {
        Message::Quit => println!("Action: Quit"),
        Message::Move { x, y } => println!("Action: Move to ({}, {})", x, y),
        Message::Write(text) => println!("Action: Write '{}'", text),
    }
}
