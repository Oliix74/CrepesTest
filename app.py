from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)

# Configuration de la base de données SQLite
DATABASE = os.path.join(os.getcwd(), 'database.db')

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.route('/', methods=['GET', 'POST'])
def command_page():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        classe = request.form['classe']
        crepe_type = request.form['crepe_type']
        
        # Enregistrez les données dans la base de données SQLite
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO commandes (nom, prenom, classe, crepe_type) VALUES (?, ?, ?, ?)", (nom, prenom, classe, crepe_type))
        db.commit()
        db.close()

        flash('Commande enregistrée avec succès!', 'success')
        
        return redirect(url_for('command_page'))
    
    return render_template('index.html')

@app.route('/orders')
def orders_page():
    # Récupérez les commandes en attente depuis la base de données
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM commandes WHERE etat = 'en_attente' ORDER BY timestamp")
    orders = cursor.fetchall()
    db.close()
    
    return render_template('orders.html', orders=orders)

@app.route('/mark_done/<int:order_id>', methods=['POST'])
def mark_done(order_id):
    # Marquez une commande comme "faite"
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE commandes SET etat = 'faite' WHERE id = ?", (order_id,))
    db.commit()
    db.close()
    
    flash('Commande marquée comme "faite".', 'success') 
    
    return redirect(url_for('orders_page'))

@app.route('/delete/<int:order_id>', methods=['POST'])
def delete(order_id):
    # Supprimez une commande
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM commandes WHERE id = ?", (order_id,))
    db.commit()
    db.close()
    
    flash('Commande supprimée.', 'danger') 
    
    return redirect(url_for('orders_page'))

if __name__ == '__main__':
    app.secret_key = "b'\x92\x8a\xee\xd8\xd5\xf7:\xc4\x13\x10\xfeW<\x93\xea\xef\xcbCEB\x08C\xf0`'"  
    app.run(debug=True)

