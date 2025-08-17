## DAY3 
## 전체 완성 시키기

1. 데이터 입력 화면(FORM) 만들기
        <!DOCTYPE html>
      <html lang="ko">
      <head>
          <meta charset="UTF-8">
          <title>Life Logger</title>
          <style>
              /* CSS style */
              body { font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; background-color: #f9f9f9; }
              h1, h2 { text-align: center; }
              .form-section { background-color: white; border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
              .form-section h2 { margin-top: 0; }
              label { display: block; margin-bottom: 5px; font-weight: bold; }
              input, select { width: 98%; padding: 8px; margin-bottom: 10px; border-radius: 4px; border: 1px solid #ccc; }
              button { width: 100%; padding: 10px 15px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
              button:hover { background-color: #0056b3; }
              
              .log-section { margin-top: 40px; }
              .log-item { background-color: white; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
              .log-item h3 { margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px; }
              .log-item ul { padding-left: 20px; list-style: none; }
              .log-item li { margin-bottom: 10px; }
          </style>
      </head>
      <body>
          <h1>📝 Life Logger</h1>
      
          <div class="form-section">
              <h2>🌙 수면 시간 기록</h2>
              <form action="/add_sleep" method="post">
                  <label for="date">날짜:</label>
                  <input type="date" id="date" name="log_date" required>
                  <label for="sleep_start">취침 시각:</label>
                  <input type="datetime-local" id="sleep_start" name="sleep_start_time" required>
                  <label for="sleep_end">기상 시각:</label>
                  <input type="datetime-local" id="sleep_end" name="sleep_end_time" required>
                  <button type="submit">수면 기록 저장</button>
              </form>
          </div>
      
          <div class="form-section">
              <h2>💸 지출 기록</h2>
              <form action="/add_expense" method="post">
                  <label for="expense_date">날짜:</label>
                  <input type="date" id="expense_date" name="log_date" required>
                  <label for="category">분야:</label>
                  <input type="text" id="category" name="category_name" placeholder="예: 식비, 교통" required>
                  <label for="amount">금액:</label>
                  <input type="number" id="amount" name="amount" placeholder="예: 8000" required>
                  <label for="description">내용:</label>
                  <input type="text" id="description" name="description" placeholder="예: 점심 식사">
                  <button type="submit">지출 기록 저장</button>
              </form>
          </div>
      
          <div class="form-section">
              <h2>🏋️ 운동 기록</h2>
              <form action="/add_exercise" method="post">
                  <label for="exercise_date">날짜:</label>
                  <input type="date" id="exercise_date" name="log_date" required>
                  <label for="exercise">운동 종류:</label>
                  <select id="exercise" name="exercise_id" required>
                      {% for exercise in exercises %}
                          <option value="{{ exercise.exercise_id }}">{{ exercise.exercise_name }}</option>
                      {% endfor %}
                  </select>
                  <label for="sets">세트 수:</label>
                  <input type="number" id="sets" name="set_number" placeholder="예: 3" required>
                  <label for="weight">무게(kg):</label>
                  <input type="number" step="0.1" id="weight" name="weight" placeholder="예: 60.5" required>
                  <label for="reps">횟수:</label>
                  <input type="number" id="reps" name="reps" placeholder="예: 10" required>
                  <button type="submit">운동 기록 추가</button>
              </form>
          </div>
          
          <div class="log-section">
              <h2>📊 나의 기록</h2>
              {% for log in logs %}
              /*app.py에서 보내준 logs라는 리스트를 log라는 변수에 하나씩 담아서 반복하는 for문*/
                  <div class="log-item">
                      <h3>{{ log.log_date.strftime('%Y년 %m월 %d일') }}</h3>
                      /*  {{}} <- 변수안의 값을 화면에 출력하라 라는 뜻. */
                      <ul>
                          <li>
                              <strong>🌙 수면:</strong> 
                              {% if log.sleep_start_time and log.sleep_end_time %}
                                  {{ log.sleep_start_time.strftime('%H:%M') }} ~ {{ log.sleep_end_time.strftime('%H:%M') }}
                              {% else %}
                                  기록 없음
                              {% endif %}
                          </li>
                          <li>
                              <strong>🏋️ 운동:</strong> 
                              {% if log.did_workout %}
                                  <ul>
                                    {% for ex in log.exercise_details %}
                                        <li>{{ ex.exercise_name }}: {{ ex.weight }}kg, {{ ex.reps }}회 ({{ ex.set_number }}세트)</li>
                                    {% endfor %}
                                  </ul>
                              {% else %}
                                  ❌ 휴식
                              {% endif %}
                          </li>
                          <li>
                              <strong>💸 지출:</strong>
                              {% if log.expense_details %}
                                  <ul>
                                  {% for exp in log.expense_details %}
                                      <li>{{ exp.category_name }}: {{ exp.amount }}원 ({{ exp.description }})</li>
                                  {% endfor %}
                                  </ul>
                              {% else %}
                                  기록 없음
                              {% endif %}
                          </li>
                      </ul>
                  </div>
              {% endfor %}
          </div>
      
      </body>
      </html>

2. app.py 수면시간 / 운동 / 지출을 입력 및 저장 되게 파이썬 코드 작성
      from flask import Flask, render_template, request, redirect, url_for
      import mysql.connector
      
      app = Flask(__name__)
      
      # 데이터베이스 연결 설정
      db_config = {
          'host': 'localhost',
          'user': 'root',
          'password': '-', #
          'database': 'life_logger_db'
      }
      
      # 메인 페이지를 보여주는 함수 
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
              return f"데이터를 불러오는 중 오류 발생: {e}"
              
      # 수면 기록을 저장하는 함수
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

      # 지출기록 저장하는 함수 
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
              # result 값은 execute에서 명령한 log_date(오늘 날짜)로 등록된 log_id가 daily_logs에 있는지 확인한 값을 나타남. 있으면 대답 / 없으면 안가져옴.
              log_id = None
              if result:
                  log_id = result[0]
              else:
              # 없으면 inesrt를 통해서 데이터 저장 
                  cursor.execute("INSERT INTO daily_logs (log_date) VALUES (%s)", (log_date,))
                  log_id = cursor.lastrowid
      
              
              # 카테고리 이름으로 category_id를 찾아오거나 새로 생성
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
      
              # expense_records 테이블에 최종 데이터 INSERT
              sql = "INSERT INTO expense_records (log_id, category_id, amount, description) VALUES (%s, %s, %s, %s)"
              val = (log_id, category_id, amount, description)
              cursor.execute(sql, val)
      
              conn.commit()
              cursor.close()
              conn.close()
      
          except Exception as e:
              return f"지출 기록 저장 중 오류 발생: {e}"
      
          return redirect(url_for('index'))
      	
      #  운동 기록 저장 함수 
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
                # 오늘 수면기록을 저장해서 운동기록이 FLASE로 되어있을경우, 오늘 기록을 찾아서 [if result : ] did_workout 값만 TRUE로 바꾼다.
              if result:
                  log_id = result[0]
                  cursor.execute("UPDATE daily_logs SET did_workout = TRUE WHERE log_id = %s", (log_id,))
              else:
                # 오늘 기록 저장이 운동기록으로 처음일 경우 TRUE로 설정하고 기록을 생성한다. 
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
