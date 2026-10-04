from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "77e6e14a65a54a65953fe70c75f54c93"  # Necessário para usar sessões

@app.before_request
def require_login():
    """Exibe o formulário de login se o usuário não estiver autenticado."""
    if not session.get("username") and request.endpoint not in ["login", "static"]:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Armazena o nome de usuário na sessão
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]  # Apenas para exemplo, não recomendado
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/")
def index():
    return render_template("index.html", username=session["username"])

@app.route("/fortinet", methods=['GET', 'POST'])
def fortinet():
    message = None
    if request.method == 'POST':
        # Lógica para processar o formulário e gerar a mensagem
        if request.form.get('nome_vpn'):
            print(f"VPN Verificada com sucesso! {request.form.get('nome_vpn')}")
        elif request.form.get('nome_nat'):
            print("NAT Verificado com sucesso!")
        elif request.form.get('origem'):
            print("arriba")
        elif request.form.get('ip_rota'):
            print("bala no alvo")

    return render_template('fortinet.html', username=session["username"])

@app.route("/logout")
def logout():
    """Limpa a sessão e redireciona para o login."""
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
