# project_life_logger
<br>
<br>

## 사용 언어 
  1. PYTHON
  2. SQL
  3. HTML,CSS
<br>
<br>

## 설명
  매일 자신의 정보를 기록 하는 프로그램. 수면시간, 일일 지출비용, 운동 상세내용 을 저장하여, 확인가능

## 데이터 구조 설명
<details>
<summary><strong>📦 daily_logs</strong></summary>

| Column Name      | Datatype     | Constraints                  | Description              |
| :--- | :--- | :--- | :--- |
| `log_id`         | `INT`        | `PK`, `AUTO_INCREMENT`       | 기록 고유 ID             |
| `log_date`       | `DATE`       | `NOT NULL`, `UNIQUE`         | 기록 날짜                |
| `sleep_start_time` | `DATETIME`   |                              | 취침 시작 시각           |
| `sleep_end_time`   | `DATETIME`   |                              | 기상 시각                |
| `did_workout`    | `BOOLEAN`    | `NOT NULL`, `DEFAULT FALSE`  | 운동 여부                |

</details>

<details>
<summary><strong>📦 exercises</strong></summary>

| Column Name | Datatype | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `exercise_id` | `INT` | `PK`, `AUTO_INCREMENT` | 운동 고유 ID |
| `exercise_name` | `VARCHAR(100)`| `NOT NULL`, `UNIQUE`| 운동 이름 |
| `target_part` | `VARCHAR(50)` | | 주 운동 부위 |

</details>

<details>
<summary><strong>📦 exercise_logs</strong></summary>

| Column Name | Datatype | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `set_id` | `INT` | `PK`, `AUTO_INCREMENT` | 운동 세트 고유 ID |
| `log_id` | `INT` | `FK`, `NOT NULL` | 어떤 날에? (`daily_logs` 참조) |
| `exercise_id` | `INT` | `FK`, `NOT NULL` | 무슨 운동을? (`exercises` 참조) |
| `set_number` | `INT` | `NOT NULL` | 몇 번째 세트? |
| `weight` | `DECIMAL(5,2)`| `NOT NULL` | 무게 (kg) |
| `reps` | `INT` | `NOT NULL` | 횟수 |

</details>

<details>
<summary><strong>📦 expense_categories</strong></summary>

| Column Name | Datatype | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `category_id` | `INT` | `PK`, `AUTO_INCREMENT` | 카테고리 고유 ID |
| `category_name` | `VARCHAR(50)` | `NOT NULL`, `UNIQUE`| 카테고리 이름 |

</details>

<details>
<summary><strong>📦 expense_records</strong></summary>

| Column Name | Datatype | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `expense_id` | `INT` | `PK`, `AUTO_INCREMENT` | 지출 기록 고유 ID |
| `log_id` | `INT` | `FK`, `NOT NULL`| 어떤 날에? (`daily_logs` 참조) |
| `category_id` | `INT` | `FK`, `NOT NULL`| 어떤 분야에? (`expense_categories` 참조) |
| `amount` | `INT` | `NOT NULL` | 지출 금액 |
| `description` | `VARCHAR(255)`| | 내용 (예: 점심 식사) |

</details>


### 구동 사진

수면시간 입력
<img width="1293" height="1253" alt="Image" src="https://github.com/user-attachments/assets/a86711fe-8aa1-4ac9-94f1-0c723c80279c" />
일일 지출 비용 입력
<img width="1293" height="1253" alt="Image" src="https://github.com/user-attachments/assets/fb508dd5-70c5-45ff-b394-b702a8875231" />
일일 운동 내용 입력
<img width="1293" height="1253" alt="Image" src="https://github.com/user-attachments/assets/4dd8ac80-c7fc-4d73-9f32-97f82ef7b7f2" />
기록 정보 확인
<img width="1293" height="1253" alt="Image" src="https://github.com/user-attachments/assets/59789fac-68b2-412d-a3cb-6a49db213556" />
