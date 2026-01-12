from flask import Flask, render_template, request, redirect, url_for
from app.archivo_caja import (
    registrar_pago_web,
    resumen_completo_web,
    resumen_id_web,
    obtener_ultimo_pago_web,
    actualizar_pago_web
)

app = Flask(__name__)

# =========================
# MENU INICIAL
# =========================
@app.route("/")
def menu():
    return render_template("menu.html")


# =========================
# CAJA - LISTA GENERAL (clickeable)
# =========================
@app.route("/caja")
def caja():
    clientes = resumen_completo_web()
    return render_template("caja.html", clientes=clientes)

# =========================
# REGISTRAR PAGO (por ID)
# =========================
@app.route("/registrar_pago/<int:cliente_id>", methods=["GET", "POST"])
def registrar(cliente_id):
    cliente = resumen_id_web(cliente_id)

    mensaje = ""
    if request.method == "POST":
        monto = float(request.form["monto"])
        ok, mensaje = registrar_pago_web(cliente_id, monto)
        cliente = resumen_id_web(cliente_id)

    return render_template(
        "registrar_pago.html",
        cliente=cliente,
        mensaje=mensaje
    )
    

# =========================
# EDITAR ÚLTIMO PAGO
# =========================
@app.route("/editar_pago/<int:cliente_id>", methods=["GET", "POST"])
def editar_pago(cliente_id):
    ultimo_pago = obtener_ultimo_pago_web(cliente_id)

    if not ultimo_pago:
        return "Este cliente no tiene pagos registrados"

    pago_id, monto_actual = ultimo_pago
    mensaje = ""

    if request.method == "POST":
        nuevo_monto = float(request.form["monto"])
        ok, mensaje = actualizar_pago_web(pago_id, nuevo_monto)

        if ok:
            return redirect(url_for("registrar", cliente_id=cliente_id))

    return render_template(
        "editar_pago.html",
        monto=monto_actual,
        mensaje=mensaje
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)