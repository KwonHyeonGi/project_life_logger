from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 데이터베이스 연결 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Qhfkehfdl@12', # 🚨 비밀번호 확인!
    'database': 'life_logger_db'
}

# --- 1. 메인 페이지를 보여주는 함수 (이게 있어야 합니다!) ---
# app.py 파일의 index() 함수

@app.route("/")
def index():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 운동 목록 가져오기 (HTML Form을 위해 필요)
        cursor.execute("SELECT exercise_id, exercise_name FROM exercises;")
        exercises = cursor.fetchall()

        # 저장된 모든 일일 기록(daily_logs)을 최신순으로 가져오기
        cursor.execute("SELECT * FROM daily_logs ORDER BY log_date DESC;")
        logs = cursor.fetchall()

        # 각 로그에 해당하는 상세 기록들을 추가해주는 로직
        for log in logs:
            # 운동 기록 가져오기
            sql = """
                SELECT e.exercise_name, el.set_number, el.weight, el.reps 
                FROM exercise_logs el
                JOIN exercises e ON el.exercise_id = e.exercise_id
                WHERE el.log_id = %s
                ORDER BY el.set_id;
            """
            cursor.execute(sql, (log['log_id'],))
            log['exercise_details'] = cursor.fetchall()

            # 지출 기록 가져오기
            sql = """
                SELECT ec.category_name, er.amount, er.description
                FROM expense_records er
                JOIN expense_categories ec ON er.category_id = ec.category_id
                WHERE er.log_id = %s
                ORDER BY er.expense_id;
            """
            cursor.execute(sql, (log['log_id'],))
            log['expense_details'] = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('index.html', exercises=exercises, logs=logs)
    
    except Exception as e:
        return f"데이터를 불러오는 중 오류 발생: {e}"# --- 2. 수면 기록을 저장하는 함수 ---
@app.route("/add_sleep", methods=['POST'])
def add_sleep():
    log_date = request.form['log_date']
    sleep_start = request.form['sleep_start_time']
    sleep_end = request.form['sleep_end_time']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO daily_logs (log_date, sleep_start_time, sleep_end_time, did_workout) VALUES (%s, %s, %s, %s)"
        val = (log_date, sleep_start, sleep_end, False)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return f"데이터 저장 중 오류 발생: {e}"
    return redirect(url_for('index'))

@app.route("/add_expense", methods=['POST'])
def add_expense():
    log_date = request.form['log_date']
    category_name = request.form['category_name'] 
    amount = request.form['amount']
    description = request.form['description']

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT log_id FROM daily_logs WHERE log_date = %s", (log_date,))
        result = cursor.fetchone()
        log_id = None
        if result:
            log_id = result[0]
        else:
            cursor.execute("INSERT INTO daily_logs (log_date) VALUES (%s)", (log_date,))
            log_id = cursor.lastrowid

        # 3. (핵심!) 카테고리 이름으로 category_id를 찾아오거나 새로 생성
        cursor.execute("SELECT category_id FROM expense_categories WHERE category_name = %s", (category_name,))
        result = cursor.fetchone()
        category_id = None
        if result:
            # 이미 존재하는 카테고리면
            category_id = result[0]
        else:
            # 처음 입력된 카테고리면 expense_categories 테이블에 새로 추가
            cursor.execute("INSERT INTO expense_categories (category_name) VALUES (%s)", (category_name,))
            category_id = cursor.lastrowid

        # 4. expense_records 테이블에 최종 데이터 INSERT
        sql = "INSERT INTO expense_records (log_id, category_id, amount, description) VALUES (%s, %s, %s, %s)"
        val = (log_id, category_id, amount, description)
        cursor.execute(sql, val)

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        return f"지출 기록 저장 중 오류 발생: {e}"

    return redirect(url_for('index'))
	
# --- 3. 현기님이 방금 추가하신 운동 기록 저장 함수 ---
@app.route("/add_exercise", methods=['POST'])
def add_exercise():
    log_date = request.form['log_date']
    exercise_id = request.form['exercise_id']
    set_number = request.form['set_number']
    weight = request.form['weight']
    reps = request.form['reps']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT log_id FROM daily_logs WHERE log_date = %s", (log_date,))
        result = cursor.fetchone()
        log_id = None
        if result:
            log_id = result[0]
            cursor.execute("UPDATE daily_logs SET did_workout = TRUE WHERE log_id = %s", (log_id,))
        else:
            cursor.execute("INSERT INTO daily_logs (log_date, did_workout) VALUES (%s, TRUE)", (log_date,))
            log_id = cursor.lastrowid
        sql = "INSERT INTO exercise_logs (log_id, exercise_id, set_number, weight, reps) VALUES (%s, %s, %s, %s, %s)"
        val = (log_id, exercise_id, set_number, weight, reps)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return f"운동 기록 저장 중 오류 발생: {e}"
    return redirect(url_for('index'))

# --- 4. 서버를 실행하는 부분 ---
if __name__ == '__main__':
    app.run(debug=True)