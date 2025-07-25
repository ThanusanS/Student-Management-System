from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Thanu0403',
    'database': 'StudentDB'
}

def get_db_connection():
    try:
        db = mysql.connector.connect(**db_config)
        return db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Home Route
@app.route('/')
def index():
    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)  # Returns results as dictionaries
        cursor.execute("SELECT * FROM students")  # Changed to match your operations
        students = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('index.html', students=students)
    return "Database connection failed", 500

# Add Student
@app.route('/add', methods=['POST'])
def add_student():
    db = get_db_connection()
    if db:
        try:
            name = request.form['name']
            age = request.form['age']
            grade = request.form['grade']
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", 
                (name, age, grade)
            )
            db.commit()
            cursor.close()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            db.close()
    return redirect(url_for('index'))

# Delete Student
@app.route('/delete/<int:id>')
def delete_student(id):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (id,))
            db.commit()
            cursor.close()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)