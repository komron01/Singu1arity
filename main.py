from flask import *
import psycopg2
import settings

#Подключение к Базе данных
try: 
    conn = psycopg2.connect(**settings.DATABASE_CONFIG)
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM example")
    data = cursor.fetchall()
    # Отключение
    cursor.close()
    conn.close()
except Exception as e:
    print('Произошла ошибка:', e)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template( 'index.html',data=data)
if __name__ == '__main__':
    app.run(debug=True)