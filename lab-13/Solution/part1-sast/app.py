from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Инициализация базы данных пользователей
def prepare_user_database():
    conn = sqlite3.connect('filipov_users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Заполнение тестовыми учетными записями
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password) VALUES (1, 'admin', 'admin@filipov.local', 'adminSecretKey')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, email, password) VALUES (2, 'guest', 'guest@filipov.local', 'guestSecretKey')")
    
    conn.commit()
    conn.close()

# Загрузка API-ключа из переменных окружения для защиты конфиденциальных данных
SECRET_API_KEY = os.environ.get('API_KEY')

if not SECRET_API_KEY:
    raise ValueError("API_KEY environment variable is not defined")

# Шаблон HTML с именем Никиты Филиппова
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>База данных пользователей</title>
</head>
<body>
    <h1>Панель управления пользователями (Филиппов)</h1>
    <form action="/user" method="GET">
        <label>Идентификатор пользователя (ID):</label>
        <input type="text" name="id">
        <button type="submit">Получить информацию</button>
    </form>
    
    <form action="/search" method="GET">
        <label>Поиск по имени пользователя:</label>
        <input type="text" name="username">
        <button type="submit">Поиск</button>
    </form>
    
    <div id="output-box">
        {content}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(MAIN_TEMPLATE.format(content="<p>Введите ID или имя пользователя</p>"))

@app.route('/user')
def fetch_user_record():
    """Безопасный параметризованный запрос получения пользователя"""
    user_id = request.args.get('id')
    
    if not user_id:
        return jsonify({"error": "Параметр id обязателен"}), 400
    
    conn = sqlite3.connect('filipov_users.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
    record = cursor.fetchone()
    conn.close()
    
    if record:
        return jsonify({"id": record[0], "username": record[1], "email": record[2]})
    return jsonify({"error": "Пользователь отсутствует в системе"}), 404

@app.route('/search')
def query_users_table():
    """Безопасный поиск с параметризацией для предотвращения SQLi"""
    search_query = request.args.get('username', '')
    
    conn = sqlite3.connect('filipov_users.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE username LIKE ?"
    cursor.execute(query, (f"%{search_query}%",))
    
    records = cursor.fetchall()
    conn.close()
    
    result = [{"id": r[0], "username": r[1], "email": r[2]} for r in records]
    return jsonify(result)

@app.route('/api/data')
def retrieve_restricted_data():
    """Безопасный доступ к конфиденциальным данным из окружения"""
    return jsonify({"api_key": SECRET_API_KEY, "status": "active"})

@app.route('/execute')
def run_system_tool():
    """Запуск ограниченного набора системных утилит (allow-list)"""
    cmd_param = request.args.get('cmd', '')
    
    ALLOWED_COMMANDS = ['echo', 'date', 'whoami']
    
    import subprocess
    tokens = cmd_param.split()
    if not tokens or tokens[0] not in ALLOWED_COMMANDS:
        return jsonify({"error": "Запуск данной команды заблокирован политикой безопасности"}), 403
        
    try:
        execution_output = subprocess.check_output(tokens)
        return jsonify({"output": execution_output.decode()})
    except Exception as err:
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    prepare_user_database()
    app.run(port=5000)
