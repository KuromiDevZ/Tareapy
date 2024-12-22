-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS movie_rental;

-- Usar la base de datos
USE movie_rental;

-- Crear la tabla de películas
CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    genre VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Crear la tabla de alquileres
CREATE TABLE rentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);

-- Insertar datos de ejemplo
INSERT INTO movies (title, release_date, genre, description, price)
VALUES
    ('The Shawshank Redemption', '1994-09-23', 'Drama', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 4.99),
    ('Inception', '2010-07-16', 'Sci-Fi', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 5.99),
    ('The Godfather', '1972-03-24', 'Crime', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 6.99),
    ('The Dark Knight', '2008-07-18', 'Action', 'When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.', 5.49),
    ('Pulp Fiction', '1994-10-14', 'Crime', 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.', 4.79);
