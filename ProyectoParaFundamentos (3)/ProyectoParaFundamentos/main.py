from flask import Flask, request, redirect, url_for, render_template, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = [
    {"username": "tester", "password": "1234"},
]
carrito = {}
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)

        if user:
            # Si el usuario es válido, almacenamos su nombre de usuario en la sesión
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Error: Nombre de usuario o contraseña incorrectos."

    return render_template("login.html", error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar si el usuario ya existe
        if any(user['username'] == username for user in users):
            return "Error: El nombre de usuario ya está registrado."

        # Agregar el nuevo usuario a la lista
        users.append({'username': username, 'password': password})
        return redirect('http://127.0.0.1:5000')
    return render_template("register_index.html")

@app.route('/index')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    return redirect(url_for('login'))

@app.route('/checkout')
def checkout():
    username = session['username']
    return render_template('checkout.html', username=username)

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('query').strip().lower() if request.args.get('query') else None

    if query:
        # Diccionario con términos de búsqueda y rutas
        bebidas = {
            "whisky": "whisky",
            "ron": "ron",
            "vino": "vino",
            "champagne": "champagne",
            "pisco": "pisco",
            "gin": "gin",
            "cerveza": "cerveza",
            "macerados": "macerados",
            "anisados": "anisados",
            "cocteles": "cocteles"
        }

        # Si encontramos la bebida, redirigimos a la ruta correspondiente
        if query in bebidas:
            return redirect(url_for(bebidas[query]))

        # Si no se encuentra, renderizamos la página con un mensaje de error
        error = f"No se encontraron resultados para: {query}"
        return render_template('index.html', error=error)

    return render_template('index.html', error=None)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Obtener el nombre del cliente desde la sesión
    nombre_cliente = session['username']
    producto = request.form.get('product')  # Usar .get() para evitar KeyError
    cantidad = request.form.get('quantity', type=int)  # Obtener la cantidad

    if producto and cantidad:
        # Si el cliente ya tiene un carrito, se añade el producto
        if nombre_cliente in carrito:
            if producto in carrito[nombre_cliente]:
                carrito[nombre_cliente][producto] += cantidad
            else:
                carrito[nombre_cliente][producto] = cantidad
        else:
            # Si no tiene un carrito, se crea uno nuevo para el cliente
            carrito[nombre_cliente] = {producto: cantidad}

        flash(f"Producto añadido al carrito: {cantidad} {producto}(s).")
        return redirect(url_for('index'))
    else:
        flash("Error al añadir el producto al carrito.")
        return redirect(url_for('index'))

@app.route('/ver_carrito')
def ver_carrito():
    if 'username' not in session:
        return "Debe iniciar sesión para ver su carrito."

    nombre_cliente = session['username']
    carrito_cliente = carrito.get(nombre_cliente, {})
    return render_template('ver_carrito.html', carrito=carrito_cliente)
####################################################
@app.route('/whisky')
def whisky():
    return render_template("whisky.html")
@app.route('/ron')
def ron():
    return render_template("ron.html")
@app.route('/vino')
def vino():
    return render_template('vino.html')
@app.route('/champagne')
def champagne():
    return render_template('champagne.html')
@app.route('/pisco')
def pisco():
    return render_template('pisco.html')
@app.route('/gin')
def gin():
    return render_template('gin.html')
@app.route('/cerveza')
def cerveza():
    return render_template('cerveza.html')
@app.route('/macerados')
def macerados():
    return render_template('macerados.html')
@app.route('/anisados')
def anisados():
    return render_template('anisados.html')
@app.route('/cocteles')
def cocteles():
    return render_template('cocteles.html')
@app.route('/cupo')
def cupo():
    return render_template("cupo.html")

if __name__ == '__main__':
    app.run(debug=True)