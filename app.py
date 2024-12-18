from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secret_key'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'event_manager'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events")
    events = cur.fetchall()
    cur.close()
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events (name, date, description) VALUES (%s, %s, %s)", (name, date, description))
        mysql.connection.commit()
        cur.close()
        flash('Evento agregado exitosamente', 'success')
        return redirect(url_for('index'))

    return render_template('add_event.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE id = %s", (id,))
    event = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE events 
            SET name = %s, date = %s, description = %s 
            WHERE id = %s
        """, (name, date, description, id))
        mysql.connection.commit()
        cur.close()
        flash('Evento actualizado exitosamente', 'success')
        return redirect(url_for('index'))

    return render_template('edit_event.html', event=event)

@app.route('/delete/<int:id>')
def delete_event(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM events WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Evento eliminado exitosamente', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
