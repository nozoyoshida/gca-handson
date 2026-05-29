import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'super-secret-key-123'  # VULNERABILITY: hardcoded secret

DATABASE = 'tickets.db'

VALID_STATUSES = ['open', 'in_progress', 'closed']
VALID_PRIORITIES = ['low', 'medium', 'high']


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            priority TEXT NOT NULL DEFAULT 'medium',
            customer_id INTEGER NOT NULL,
            assignee TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')

    count = db.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
    if count == 0:
        customers = [
            ('佐藤 花子', 'sato@example.co.jp', '株式会社ABC商事'),
            ('高橋 太郎', 'takahashi@example.co.jp', 'DEF工業株式会社'),
            ('伊藤 美咲', 'ito@example.co.jp', None),
        ]
        db.executemany(
            'INSERT INTO customers (name, email, company) VALUES (?, ?, ?)',
            customers
        )

        tickets = [
            ('ログインできない', 'パスワードリセット後もログインできません。エラーコード: AUTH-503が表示されます。', 'open', 'high', 1, '山田'),
            ('請求書の金額が間違っている', '先月分の請求書に二重計上があります。注文番号: ORD-2024-0892。', 'in_progress', 'medium', 2, '鈴木'),
            ('商品が届かない', '注文から10日経過しましたが、まだ届いていません。追跡番号: TRK-456789。', 'open', 'high', 3, None),
            ('退会方法がわからない', 'アカウントの退会手続きの方法を教えてください。', 'closed', 'low', 1, '山田'),
        ]
        db.executemany(
            'INSERT INTO tickets (title, description, status, priority, customer_id, assignee) VALUES (?, ?, ?, ?, ?, ?)',
            tickets
        )

    db.commit()
    db.close()


# ----- GUI Routes -----

@app.route('/')
def index():
    db = get_db()
    tickets = db.execute('''
        SELECT tickets.*, customers.name as customer_name
        FROM tickets
        JOIN customers ON tickets.customer_id = customers.id
        ORDER BY tickets.created_at DESC
    ''').fetchall()

    summary = {
        'total': len(tickets),
        'open': sum(1 for t in tickets if t['status'] == 'open'),
        'in_progress': sum(1 for t in tickets if t['status'] == 'in_progress'),
        'closed': sum(1 for t in tickets if t['status'] == 'closed'),
    }

    db.close()
    return render_template('index.html', tickets=tickets, summary=summary)


@app.route('/tickets/<int:ticket_id>/view')
def ticket_view(ticket_id):
    db = get_db()
    ticket = db.execute('''
        SELECT tickets.*, customers.name as customer_name,
               customers.email as customer_email, customers.company as customer_company
        FROM tickets
        JOIN customers ON tickets.customer_id = customers.id
        WHERE tickets.id = ?
    ''', (ticket_id,)).fetchone()
    db.close()

    if ticket is None:
        return render_template('base.html', error='チケットが見つかりません'), 404

    return render_template('ticket_detail.html', ticket=ticket)


# ----- API Routes -----

@app.route('/tickets', methods=['GET'])
def get_tickets():
    db = get_db()
    status = request.args.get('status')
    priority = request.args.get('priority')

    if status:
        # VULNERABILITY: SQL Injection via status filter
        sql = f"SELECT * FROM tickets WHERE status = '{status}'"
        tickets = db.execute(sql).fetchall()
    elif priority:
        sql = f"SELECT * FROM tickets WHERE priority = '{priority}'"
        tickets = db.execute(sql).fetchall()
    else:
        tickets = db.execute('SELECT * FROM tickets ORDER BY created_at DESC').fetchall()

    db.close()
    return jsonify([dict(row) for row in tickets])


@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    db = get_db()
    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    db.close()
    if ticket is None:
        return jsonify({'error': 'Ticket not found'}), 404
    return jsonify(dict(ticket))


@app.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()
    # VULNERABILITY: No input validation
    title = data.get('title', '')
    description = data.get('description', '')
    priority = data.get('priority', 'medium')
    customer_id = data.get('customer_id', 1)

    db = get_db()
    cursor = db.execute(
        'INSERT INTO tickets (title, description, priority, customer_id) VALUES (?, ?, ?, ?)',
        (title, description, priority, customer_id)
    )
    db.commit()
    ticket_id = cursor.lastrowid
    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    db.close()
    return jsonify(dict(ticket)), 201


@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.get_json()
    db = get_db()

    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    if ticket is None:
        db.close()
        return jsonify({'error': 'Ticket not found'}), 404

    title = data.get('title', ticket['title'])
    description = data.get('description', ticket['description'])
    priority = data.get('priority', ticket['priority'])
    assignee = data.get('assignee', ticket['assignee'])

    db.execute(
        "UPDATE tickets SET title = ?, description = ?, priority = ?, assignee = ?, updated_at = datetime('now') WHERE id = ?",
        (title, description, priority, assignee, ticket_id)
    )
    db.commit()
    updated = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    db.close()
    return jsonify(dict(updated))


@app.route('/tickets/<int:ticket_id>/status', methods=['PATCH'])
def update_status(ticket_id):
    data = request.get_json()
    # VULNERABILITY: No validation on status value
    new_status = data.get('status', '')

    db = get_db()
    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    if ticket is None:
        db.close()
        return jsonify({'error': 'Ticket not found'}), 404

    db.execute(
        "UPDATE tickets SET status = ?, updated_at = datetime('now') WHERE id = ?",
        (new_status, ticket_id)
    )
    db.commit()
    updated = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    db.close()
    return jsonify(dict(updated))


@app.route('/tickets/search', methods=['GET'])
def search_tickets():
    q = request.args.get('q', '')
    db = get_db()
    # VULNERABILITY: SQL Injection - uses f-string instead of parameterized query
    sql = f"SELECT * FROM tickets WHERE title LIKE '%{q}%' OR description LIKE '%{q}%'"
    tickets = db.execute(sql).fetchall()
    db.close()
    return jsonify([dict(row) for row in tickets])


if __name__ == '__main__':
    init_db()
    app.run(debug=True)  # VULNERABILITY: debug mode enabled
