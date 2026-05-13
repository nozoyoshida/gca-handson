import os
import re
import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-in-production')

DATABASE = 'tickets.db'

VALID_STATUSES = ['open', 'in_progress', 'closed']
VALID_PRIORITIES = ['low', 'medium', 'high']
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 5000


def get_db():
    """データベース接続を取得する。"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def strip_html_tags(text):
    """文字列から HTML タグを除去する。"""
    return re.sub(r'<[^>]+>', '', text)


def validate_ticket_input(data, require_all=True):
    """チケットの入力データをバリデーションする。

    Args:
        data: リクエストのJSONデータ
        require_all: True の場合、title と description を必須とする

    Returns:
        (validated_data, error_message) のタプル。エラー時は validated_data が None。
    """
    if data is None:
        return None, 'リクエストボディが必要です'

    validated = {}

    if 'title' in data or require_all:
        title = data.get('title', '')
        if not title or not title.strip():
            return None, 'title は必須です'
        title = strip_html_tags(title.strip())
        if len(title) > MAX_TITLE_LENGTH:
            return None, f'title は{MAX_TITLE_LENGTH}文字以内にしてください'
        validated['title'] = title

    if 'description' in data or require_all:
        description = data.get('description', '')
        if not description or not description.strip():
            return None, 'description は必須です'
        description = strip_html_tags(description.strip())
        if len(description) > MAX_DESCRIPTION_LENGTH:
            return None, f'description は{MAX_DESCRIPTION_LENGTH}文字以内にしてください'
        validated['description'] = description

    if 'priority' in data:
        priority = data.get('priority')
        if priority not in VALID_PRIORITIES:
            return None, f'priority は {", ".join(VALID_PRIORITIES)} のいずれかを指定してください'
        validated['priority'] = priority

    if 'assignee' in data:
        validated['assignee'] = data.get('assignee')

    if 'customer_id' in data:
        customer_id = data.get('customer_id')
        if not isinstance(customer_id, int) or customer_id < 1:
            return None, 'customer_id は正の整数を指定してください'
        validated['customer_id'] = customer_id

    return validated, None


def init_db():
    """データベースを初期化し、サンプルデータを投入する。"""
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
    db.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            responder TEXT NOT NULL,
            message TEXT NOT NULL,
            is_internal BOOLEAN DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (ticket_id) REFERENCES tickets(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS sla_policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority TEXT NOT NULL UNIQUE,
            response_deadline_hours INTEGER NOT NULL,
            resolution_deadline_hours INTEGER NOT NULL
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

        sla_policies = [
            ('high', 1, 4),
            ('medium', 4, 24),
            ('low', 24, 72),
        ]
        db.executemany(
            'INSERT INTO sla_policies (priority, response_deadline_hours, resolution_deadline_hours) VALUES (?, ?, ?)',
            sla_policies
        )

    db.commit()
    db.close()


# ----- GUI Routes -----

@app.route('/')
def index():
    """GET / チケット一覧画面を表示する。"""
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
    """GET /tickets/<id>/view チケット詳細画面を表示する。"""
    db = get_db()
    ticket = db.execute('''
        SELECT tickets.*, customers.name as customer_name,
               customers.email as customer_email, customers.company as customer_company
        FROM tickets
        JOIN customers ON tickets.customer_id = customers.id
        WHERE tickets.id = ?
    ''', (ticket_id,)).fetchone()

    responses = db.execute(
        'SELECT * FROM responses WHERE ticket_id = ? ORDER BY created_at ASC',
        (ticket_id,)
    ).fetchall()

    db.close()

    if ticket is None:
        return render_template('base.html', error='チケットが見つかりません'), 404

    return render_template('ticket_detail.html', ticket=ticket, responses=responses)


# ----- API Routes -----

@app.route('/tickets', methods=['GET'])
def get_tickets():
    """GET /tickets チケット一覧を取得する。status, priority でフィルタ可能。"""
    db = get_db()
    conditions = []
    params = []

    status = request.args.get('status')
    if status:
        if status not in VALID_STATUSES:
            db.close()
            return jsonify({'error': f'status は {", ".join(VALID_STATUSES)} のいずれかを指定してください'}), 400
        conditions.append('status = ?')
        params.append(status)

    priority = request.args.get('priority')
    if priority:
        if priority not in VALID_PRIORITIES:
            db.close()
            return jsonify({'error': f'priority は {", ".join(VALID_PRIORITIES)} のいずれかを指定してください'}), 400
        conditions.append('priority = ?')
        params.append(priority)

    sql = 'SELECT * FROM tickets'
    if conditions:
        sql += ' WHERE ' + ' AND '.join(conditions)
    sql += ' ORDER BY created_at DESC'

    tickets = db.execute(sql, params).fetchall()
    db.close()
    return jsonify([dict(row) for row in tickets])


@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """GET /tickets/<id> 指定したチケットを取得する。"""
    db = get_db()
    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    db.close()
    if ticket is None:
        return jsonify({'error': 'チケットが見つかりません'}), 404
    return jsonify(dict(ticket))


@app.route('/tickets', methods=['POST'])
def create_ticket():
    """POST /tickets 新しいチケットを作成する。"""
    data = request.get_json()
    validated, error = validate_ticket_input(data, require_all=True)
    if error:
        return jsonify({'error': error}), 400

    customer_id = validated.get('customer_id', 1)
    db = get_db()

    customer = db.execute('SELECT id FROM customers WHERE id = ?', (customer_id,)).fetchone()
    if customer is None:
        db.close()
        return jsonify({'error': '指定された顧客が存在しません'}), 400

    cursor = db.execute(
        'INSERT INTO tickets (title, description, priority, customer_id) VALUES (?, ?, ?, ?)',
        (validated['title'], validated['description'], validated.get('priority', 'medium'), customer_id)
    )
    db.commit()
    ticket_id = cursor.lastrowid
    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    db.close()
    return jsonify(dict(ticket)), 201


@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """PUT /tickets/<id> チケットを更新する。"""
    data = request.get_json()
    validated, error = validate_ticket_input(data, require_all=False)
    if error:
        return jsonify({'error': error}), 400

    db = get_db()
    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    if ticket is None:
        db.close()
        return jsonify({'error': 'チケットが見つかりません'}), 404

    title = validated.get('title', ticket['title'])
    description = validated.get('description', ticket['description'])
    priority = validated.get('priority', ticket['priority'])
    assignee = validated.get('assignee', ticket['assignee'])

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
    """PATCH /tickets/<id>/status チケットのステータスを変更する。"""
    data = request.get_json()
    new_status = data.get('status', '')

    if new_status not in VALID_STATUSES:
        return jsonify({'error': f'status は {", ".join(VALID_STATUSES)} のいずれかを指定してください'}), 400

    db = get_db()
    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    if ticket is None:
        db.close()
        return jsonify({'error': 'チケットが見つかりません'}), 404

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
    """GET /tickets/search?q= チケットをキーワードで検索する。"""
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    q_sanitized = strip_html_tags(q)
    db = get_db()
    tickets = db.execute(
        'SELECT * FROM tickets WHERE title LIKE ? OR description LIKE ?',
        (f'%{q_sanitized}%', f'%{q_sanitized}%')
    ).fetchall()
    db.close()
    return jsonify([dict(row) for row in tickets])


# ----- Response (対応履歴) Routes -----

@app.route('/tickets/<int:ticket_id>/responses', methods=['GET'])
def get_responses(ticket_id):
    """GET /tickets/<id>/responses チケットの対応履歴を取得する。"""
    db = get_db()
    ticket = db.execute('SELECT id FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    if ticket is None:
        db.close()
        return jsonify({'error': 'チケットが見つかりません'}), 404

    responses = db.execute(
        'SELECT * FROM responses WHERE ticket_id = ? ORDER BY created_at ASC',
        (ticket_id,)
    ).fetchall()
    db.close()
    return jsonify([dict(r) for r in responses])


@app.route('/tickets/<int:ticket_id>/responses', methods=['POST'])
def create_response(ticket_id):
    """POST /tickets/<id>/responses チケットに対応履歴を追加する。"""
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'リクエストボディが必要です'}), 400

    responder = data.get('responder', '').strip()
    message = data.get('message', '').strip()
    is_internal = bool(data.get('is_internal', False))

    if not responder:
        return jsonify({'error': 'responder は必須です'}), 400
    if not message:
        return jsonify({'error': 'message は必須です'}), 400

    responder = strip_html_tags(responder)
    message = strip_html_tags(message)

    db = get_db()
    ticket = db.execute('SELECT id FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    if ticket is None:
        db.close()
        return jsonify({'error': 'チケットが見つかりません'}), 404

    cursor = db.execute(
        'INSERT INTO responses (ticket_id, responder, message, is_internal) VALUES (?, ?, ?, ?)',
        (ticket_id, responder, message, is_internal)
    )
    db.commit()
    response = db.execute('SELECT * FROM responses WHERE id = ?', (cursor.lastrowid,)).fetchone()
    db.close()
    return jsonify(dict(response)), 201


# ----- SLA Routes -----

@app.route('/tickets/<int:ticket_id>/sla-status', methods=['GET'])
def get_sla_status(ticket_id):
    """GET /tickets/<id>/sla-status チケットの SLA ステータスを取得する。"""
    db = get_db()
    ticket = db.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
    if ticket is None:
        db.close()
        return jsonify({'error': 'チケットが見つかりません'}), 404

    policy = db.execute(
        'SELECT * FROM sla_policies WHERE priority = ?',
        (ticket['priority'],)
    ).fetchone()

    first_response = db.execute(
        'SELECT created_at FROM responses WHERE ticket_id = ? ORDER BY created_at ASC LIMIT 1',
        (ticket_id,)
    ).fetchone()

    # 経過時間を計算（時間単位）
    elapsed = db.execute(
        "SELECT (julianday('now') - julianday(?)) * 24 as hours",
        (ticket['created_at'],)
    ).fetchone()

    db.close()

    elapsed_hours = elapsed['hours'] if elapsed else 0
    response_deadline = policy['response_deadline_hours'] if policy else 24
    resolution_deadline = policy['resolution_deadline_hours'] if policy else 72

    response_breached = first_response is None and elapsed_hours > response_deadline
    resolution_breached = ticket['status'] != 'closed' and elapsed_hours > resolution_deadline

    return jsonify({
        'ticket_id': ticket_id,
        'priority': ticket['priority'],
        'elapsed_hours': round(elapsed_hours, 1),
        'response_deadline_hours': response_deadline,
        'resolution_deadline_hours': resolution_deadline,
        'first_response_at': first_response['created_at'] if first_response else None,
        'response_breached': response_breached,
        'resolution_breached': resolution_breached,
    })


@app.route('/tickets/overdue', methods=['GET'])
def get_overdue_tickets():
    """GET /tickets/overdue SLA 違反のチケット一覧を取得する。"""
    db = get_db()
    tickets = db.execute(
        "SELECT * FROM tickets WHERE status != 'closed'"
    ).fetchall()

    overdue = []
    for ticket in tickets:
        policy = db.execute(
            'SELECT * FROM sla_policies WHERE priority = ?',
            (ticket['priority'],)
        ).fetchone()
        if policy is None:
            continue

        elapsed = db.execute(
            "SELECT (julianday('now') - julianday(?)) * 24 as hours",
            (ticket['created_at'],)
        ).fetchone()

        elapsed_hours = elapsed['hours'] if elapsed else 0
        if elapsed_hours > policy['resolution_deadline_hours']:
            overdue.append({
                **dict(ticket),
                'elapsed_hours': round(elapsed_hours, 1),
                'resolution_deadline_hours': policy['resolution_deadline_hours'],
            })

    db.close()
    return jsonify(overdue)


if __name__ == '__main__':
    init_db()
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)
