from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)
DB_PATH = 'jobs.db'

VALID_STATUSES = ['pending', 'processing', 'completed', 'failed']
VALID_JOB_TYPES = ['backup', 'cleanup', 'report']


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'job-execution-api'
    })


@app.route('/jobs', methods=['GET'])
def get_jobs():
    status = request.args.get('status')
    conn = get_db_connection()

    if status:
        jobs = conn.execute(
            'SELECT * FROM jobs WHERE status = ? ORDER BY id ASC',
            (status,)
        ).fetchall()
    else:
        jobs = conn.execute(
            'SELECT * FROM jobs ORDER BY id ASC'
        ).fetchall()

    conn.close()
    return jsonify([dict(job) for job in jobs])


@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    conn = get_db_connection()
    job = conn.execute(
        'SELECT * FROM jobs WHERE id = ?',
        (job_id,)
    ).fetchone()
    conn.close()

    if job is None:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify(dict(job))


@app.route('/jobs/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    status = data.get('status')
    result = data.get('result')

    if status not in VALID_STATUSES:
        return jsonify({
            'error': 'Invalid status',
            'allowed_statuses': VALID_STATUSES
        }), 400

    conn = get_db_connection()

    existing_job = conn.execute(
        'SELECT * FROM jobs WHERE id = ?',
        (job_id,)
    ).fetchone()

    if existing_job is None:
        conn.close()
        return jsonify({'error': 'Job not found'}), 404

    conn.execute(
        '''
        UPDATE jobs
        SET status = ?, result = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''',
        (status, result, job_id)
    )
    conn.commit()

    updated_job = conn.execute(
        'SELECT * FROM jobs WHERE id = ?',
        (job_id,)
    ).fetchone()

    conn.close()
    return jsonify(dict(updated_job))


@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    job_type = data.get('job_type')
    payload = data.get('payload', '{}')

    if job_type not in VALID_JOB_TYPES:
        return jsonify({
            'error': 'Invalid job_type',
            'allowed_job_types': VALID_JOB_TYPES
        }), 400

    try:
        json.loads(payload)
    except json.JSONDecodeError:
        return jsonify({'error': 'payload must be a valid JSON string'}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        '''
        INSERT INTO jobs (job_type, payload, status)
        VALUES (?, ?, 'pending')
        ''',
        (job_type, payload)
    )
    conn.commit()

    job_id = cursor.lastrowid

    created_job = conn.execute(
        'SELECT * FROM jobs WHERE id = ?',
        (job_id,)
    ).fetchone()

    conn.close()
    return jsonify(dict(created_job)), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
