from flask import Flask
import mysql.connector  # 1. 방금 설치한 통역사 import

app = Flask(__name__)

# 2. 데이터베이스 '창고'의 주소 정보
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Qhfkehfdl@12',  # 🚨 이 부분을 꼭 현기님의 비밀번호로 수정하세요!
    'database': 'life_logger_db'
}

@app.route("/")
def show_exercises():
    try:
        # 3. 창고에 연결해서 데이터 가져오기
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # "exercises 테이블에 있는 모든 운동 이름과 부위를 보여줘" 라는 SQL 명령
        cursor.execute("SELECT exercise_name, target_part FROM exercises;")
        exercises = cursor.fetchall()  # 모든 결과를 리스트로 가져오기

        cursor.close()
        conn.close()

        # 4. 가져온 데이터를 HTML로 만들어서 손님에게 보여주기
        html = "<h1>🏋️ 운동 목록 🏋️</h1><ul>"
        for exercise in exercises:
            # exercise[0]은 exercise_name, exercise[1]은 target_part
            html += f"<li>{exercise[0]} ({exercise[1]})</li>"
        html += "</ul>"

        return html

    except Exception as e:
        return f"데이터베이스 연결에 실패했습니다: {e}"

if __name__ == '__main__':
    app.run(debug=True)