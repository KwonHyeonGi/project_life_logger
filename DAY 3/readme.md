## DAY3 
## 전체 완성 시키기(全てを完成）

1. 데이터 입력 화면(FORM) 만들기（データ入力画面作る）
   teamplates폴더에 index.html이라는 파일을 생성 후 HTML 코드 작성. CSS사용하여 꾸미기.（TEAMPLATESというフォルダにINDEX.HTMLファイルを作成後、HTMLコード作成、CSSを利用する。）
<br>
   HTML 이라 모르는 문장이 너무 많아서 힘들었다.（HTMLは知らない文章が多くて大変でした。）



 2. app.py 파일의 index() 함수（APP.PYファイルのINDEX()）
       ```
            대부분이 cursor.execute 를 통해서 명령한다. fetchall()은 값이 있으면 가져오고, 없으면 아무것도 하지 말라는 뜻
          （大体がCURSOR.EXECUTEを通して命令する。FETCHALL()は値があったら持って、なかったら何もしいていう意味）
               cursor.execute("SELECT exercise_id, exercise_name FROM exercises;")
               exercises = cursor.fetchall()
            result 값은 execute에서 명령한 log_date(오늘 날짜)로 등록된 log_id가 daily_logs에 있는지 확인한 값을 나타남. 있으면 대답 / 없으면 안가져옴.
           （RESULT値はEXECUTEから命令したLOG_DATE（本日）に登録されたLOG_IDがDAILY_LOGSにあるかどうかを確認した値。あったら答え・なかったら何もしない）
               cursor.execute("SELECT log_id FROM daily_logs WHERE log_date = %s", (log_date,))
               result = cursor.fetchone()
               log_id = None
                  if result:
                     log_id = result[0]
                  else:
                     cursor.execute("INSERT INTO daily_logs (log_date) VALUES (%s)", (log_date,))
               log_id = cursor.lastrowid
            없으면 inesrt를 통해서 데이터 저장
          （なかったらINSERTでデータ保存）
              
             카테고리 이름으로 category_id를 찾아오거나 새로 생성
           （カテゴリー名でCATEGORY_IDを探し、新しく作成）
              cursor.execute("SELECT category_id FROM expense_categories WHERE category_name = %s", (category_name,))
              result = cursor.fetchone()
              category_id = None
              if result:
                  category_id = result[0]
              else:
           이미 존재하는 카테고리면 result[0], 처음 입력된 카테고리면 expense_categories 테이블에 새로 추가
          (もう、存在するカテゴリーならRESULT[0]を、初めて入力したカテゴリーならEXPENCESE_CATEGORIESテーブルに新しく追加）
                  cursor.execute("INSERT INTO expense_categories (category_name) VALUES (%s)", (category_name,))
                  category_id = cursor.lastrowid     
```


              오늘 수면기록을 저장해서 운동기록이 FLASE로 되어있을경우, 오늘 기록을 찾아서 [if result : ] did_workout 값만 TRUE로 바꾼다.
               (本日睡眠記録を保存して運動記録がFLASEになってる場合、今日の記録を探して [if result: ] did_workout 値をTRUEに変わる。）
              if result:
                  log_id = result[0]
                  cursor.execute("UPDATE daily_logs SET did_workout = TRUE WHERE log_id = %s", (log_id,))
              else:
                 오늘 기록 저장이 운동기록으로 처음일 경우 TRUE로 설정하고 기록을 생성한다. 
                  （本日の記録保存が運動記録で初めの場合はTRUEに設定してから記録を保存する）
                  cursor.execute("INSERT INTO daily_logs (log_date, did_workout) VALUES (%s, TRUE)", (log_date,))
                  log_id = cursor.lastrowid
```
