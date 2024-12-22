from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la base de datos MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambia esta contraseña si tienes una configurada
    'database': 'movie_rental'
}

# Conexión global
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    """Página principal: lista de películas."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    """Agregar una nueva película."""
    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']
        genre = request.form['genre']
        description = request.form['description']
        price = request.form['price']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO movies (title, release_date, genre, description, price)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, release_date, genre, description, price))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Película agregada exitosamente.')
        return redirect(url_for('index'))

    return render_template('add_movie.html')

@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    """Editar los detalles de una película."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']
        genre = request.form['genre']
        description = request.form['description']
        price = request.form['price']

        cursor = conn.cursor()
        cursor.execute("""
            UPDATE movies
            SET title = %s, release_date = %s, genre = %s, description = %s, price = %s
            WHERE id = %s
        """, (title, release_date, genre, description, price, movie_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Película actualizada exitosamente.')
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_movie.html', movie=movie)

@app.route('/rent_movie/<int:movie_id>', methods=['GET', 'POST'])
def rent_movie(movie_id):
    """Registrar un alquiler."""
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rentals (movie_id, customer_name)
            VALUES (%s, %s)
        """, (movie_id, customer_name))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Película alquilada exitosamente.')
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    return render_template('rent_movie.html', movie=movie)

@app.route('/rentals')
def rentals():
    """Historial de alquileres."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT rentals.id, movies.title, rentals.customer_name, rentals.rental_date
        FROM rentals
        JOIN movies ON rentals.movie_id = movies.id
    """)
    rentals = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('rentals.html', rentals=rentals)

@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    """Eliminar una película."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Película eliminada exitosamente.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
