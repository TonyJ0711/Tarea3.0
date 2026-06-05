from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

estudiantes = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Estudiantes</title>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0d0f14; --surface: #161a23; --border: #252a38;
            --accent: #4fffb0; --accent2: #ff6b6b; --accent3: #ffd166;
            --text: #e8eaf0; --muted: #6b7280; --radius: 10px;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: var(--bg); color: var(--text);
            font-family: 'Syne', sans-serif;
            min-height: 100vh; padding: 40px 20px;
        }
        body::before {
            content: ''; position: fixed; inset: 0;
            background-image:
                linear-gradient(rgba(79,255,176,.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(79,255,176,.04) 1px, transparent 1px);
            background-size: 40px 40px; pointer-events: none; z-index: 0;
        }
        .wrapper { position: relative; z-index: 1; max-width: 1000px; margin: 0 auto; }
        header {
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 36px; padding-bottom: 20px; border-bottom: 1px solid var(--border);
        }
        .logo { display: flex; align-items: center; gap: 12px; }
        .logo-icon {
            width: 42px; height: 42px; background: var(--accent); border-radius: 8px;
            display: flex; align-items: center; justify-content: center; font-size: 20px;
        }
        h1 { font-size: 1.6rem; font-weight: 800; letter-spacing: -.5px; }
        h1 span { color: var(--accent); }
        .stat-badge {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 20px; padding: 6px 16px;
            font-family: 'DM Mono', monospace; font-size: .82rem; color: var(--accent);
        }
        .layout { display: grid; grid-template-columns: 320px 1fr; gap: 24px; }
        @media (max-width: 700px) { .layout { grid-template-columns: 1fr; } }
        .card {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 24px;
        }
        .card-title {
            font-size: .75rem; font-weight: 700; letter-spacing: 2px;
            text-transform: uppercase; color: var(--muted); margin-bottom: 20px;
        }
        label { display: block; font-size: .8rem; color: var(--muted); margin-bottom: 6px; margin-top: 14px; }
        label:first-of-type { margin-top: 0; }
        input {
            width: 100%; background: var(--bg); border: 1px solid var(--border);
            border-radius: 6px; padding: 10px 12px; color: var(--text);
            font-family: 'DM Mono', monospace; font-size: .88rem; transition: border-color .2s;
        }
        input:focus { outline: none; border-color: var(--accent); }
        .btn {
            display: inline-flex; align-items: center; justify-content: center; gap: 6px;
            margin-top: 18px; width: 100%; padding: 11px; border: none; border-radius: 6px;
            font-family: 'Syne', sans-serif; font-size: .9rem; font-weight: 700;
            cursor: pointer; transition: opacity .15s, transform .1s;
        }
        .btn:active { transform: scale(.98); }
        .btn-primary { background: var(--accent); color: #0d0f14; }
        .btn-primary:hover { opacity: .88; }
        .btn-danger {
            background: transparent; border: 1px solid var(--accent2); color: var(--accent2);
            padding: 5px 10px; width: auto; margin-top: 0; font-size: .75rem; border-radius: 5px;
        }
        .btn-danger:hover { background: var(--accent2); color: #fff; }
        .btn-edit {
            background: transparent; border: 1px solid var(--accent3); color: var(--accent3);
            padding: 5px 10px; width: auto; margin-top: 0; font-size: .75rem; border-radius: 5px;
        }
        .btn-edit:hover { background: var(--accent3); color: #0d0f14; }
        table { width: 100%; border-collapse: collapse; font-size: .88rem; }
        thead tr { border-bottom: 1px solid var(--border); }
        th {
            text-align: left; padding: 8px 10px; font-size: .7rem;
            letter-spacing: 1.5px; text-transform: uppercase; color: var(--muted); font-weight: 700;
        }
        td { padding: 12px 10px; border-bottom: 1px solid rgba(37,42,56,.7); vertical-align: middle; }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: rgba(79,255,176,.03); }
        .grade {
            display: inline-block; padding: 3px 10px; border-radius: 20px;
            font-family: 'DM Mono', monospace; font-size: .82rem; font-weight: 500;
        }
        .grade-a { background: rgba(79,255,176,.15); color: var(--accent); }
        .grade-b { background: rgba(255,209,102,.15); color: var(--accent3); }
        .grade-c { background: rgba(255,107,107,.15); color: var(--accent2); }
        .empty { text-align: center; padding: 48px 20px; color: var(--muted); }
        .empty-icon { font-size: 2.5rem; margin-bottom: 12px; }
        .flash {
            background: rgba(79,255,176,.1); border: 1px solid var(--accent);
            border-radius: 6px; padding: 10px 16px; margin-bottom: 20px;
            font-size: .88rem; color: var(--accent);
        }
        .avatar {
            width: 32px; height: 32px; border-radius: 50%;
            display: inline-flex; align-items: center; justify-content: center;
            font-size: .8rem; font-weight: 800; flex-shrink: 0; margin-right: 8px;
        }
        .name-cell { display: flex; align-items: center; }
        .actions { display: flex; gap: 6px; }
        .edit-card {
            background: var(--surface); border: 1px solid var(--accent3);
            border-radius: var(--radius); padding: 24px; margin-bottom: 24px;
        }
        .edit-card .card-title { color: var(--accent3); }
    </style>
</head>
<body>
<div class="wrapper">
    <header>
        <div class="logo">
            <div class="logo-icon">🎓</div>
            <h1>Gestión de <span>Estudiantes</span></h1>
        </div>
        <div class="stat-badge">{{ estudiantes|length }} registrado{{ 's' if estudiantes|length != 1 else '' }}</div>
    </header>

    {% if mensaje %}
    <div class="flash">✓ {{ mensaje }}</div>
    {% endif %}

    <div class="layout">
        <div>
            {% if editar %}
            <div class="edit-card">
                <div class="card-title">✏ Editar Estudiante</div>
                <form method="POST" action="/editar/{{ editar.id }}">
                    <label>Nombre</label>
                    <input type="text" name="nombre" value="{{ editar.nombre }}" required>
                    <label>Código</label>
                    <input type="text" name="codigo" value="{{ editar.codigo }}" required>
                    <label>Carrera</label>
                    <input type="text" name="carrera" value="{{ editar.carrera }}" required>
                    <label>Nota (0–10)</label>
                    <input type="number" name="nota" min="0" max="10" step="0.1" value="{{ editar.nota }}" required>
                    <button class="btn btn-primary" type="submit">💾 Guardar Cambios</button>
                </form>
                <a href="/" style="display:block;margin-top:10px;text-align:center;font-size:.8rem;color:var(--muted);">Cancelar</a>
            </div>
            {% endif %}

            <div class="card">
                <div class="card-title">＋ Nuevo Estudiante</div>
                <form method="POST" action="/agregar">
                    <label>Nombre completo</label>
                    <input type="text" name="nombre" placeholder="Ej. Ana García" required>
                    <label>Código estudiantil</label>
                    <input type="text" name="codigo" placeholder="Ej. EST-2024-001" required>
                    <label>Carrera</label>
                    <input type="text" name="carrera" placeholder="Ej. Ingeniería de Software" required>
                    <label>Nota (0–10)</label>
                    <input type="number" name="nota" min="0" max="10" step="0.1" placeholder="Ej. 8.5" required>
                    <button class="btn btn-primary" type="submit">＋ Agregar Estudiante</button>
                </form>
            </div>
        </div>

        <div class="card">
            <div class="card-title">📋 Listado</div>
            {% if estudiantes %}
            <table>
                <thead>
                    <tr>
                        <th>Estudiante</th><th>Código</th><th>Carrera</th><th>Nota</th><th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                {% for est in estudiantes %}
                {% set colors = ['#4fffb0','#ffd166','#ff6b6b','#a78bfa','#38bdf8'] %}
                {% set color = colors[loop.index0 % 5] %}
                <tr>
                    <td>
                        <div class="name-cell">
                            <div class="avatar" style="background:{{ color }}22; color:{{ color }}">
                                {{ est.nombre[0].upper() }}
                            </div>
                            {{ est.nombre }}
                        </div>
                    </td>
                    <td style="font-family:'DM Mono',monospace;font-size:.8rem;color:var(--muted)">{{ est.codigo }}</td>
                    <td style="font-size:.85rem">{{ est.carrera }}</td>
                    <td>
                        {% if est.nota >= 8 %}
                            <span class="grade grade-a">{{ "%.1f"|format(est.nota) }}</span>
                        {% elif est.nota >= 6 %}
                            <span class="grade grade-b">{{ "%.1f"|format(est.nota) }}</span>
                        {% else %}
                            <span class="grade grade-c">{{ "%.1f"|format(est.nota) }}</span>
                        {% endif %}
                    </td>
                    <td>
                        <div class="actions">
                            <a href="/editar_form/{{ est.id }}"><button class="btn btn-edit">Editar</button></a>
                            <form method="POST" action="/eliminar/{{ est.id }}" style="display:inline"
                                  onsubmit="return confirm('¿Eliminar a {{ est.nombre }}?')">
                                <button class="btn btn-danger" type="submit">Eliminar</button>
                            </form>
                        </div>
                    </td>
                </tr>
                {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty">
                <div class="empty-icon">📭</div>
                <p>Sin estudiantes registrados.</p>
                <p style="font-size:.8rem;margin-top:6px;">Usa el formulario para agregar el primero.</p>
            </div>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    mensaje = request.args.get("msg", "")
    return render_template_string(HTML, estudiantes=estudiantes, mensaje=mensaje, editar=None)

@app.route("/agregar", methods=["POST"])
def agregar():
    global next_id
    nombre  = request.form.get("nombre", "").strip()
    codigo  = request.form.get("codigo", "").strip()
    carrera = request.form.get("carrera", "").strip()
    nota    = float(request.form.get("nota", 0))
    if nombre and codigo and carrera:
        estudiantes.append({"id": next_id, "nombre": nombre, "codigo": codigo, "carrera": carrera, "nota": nota})
        next_id += 1
    return redirect(url_for("index", msg=f"Estudiante '{nombre}' agregado correctamente."))

@app.route("/editar_form/<int:est_id>")
def editar_form(est_id):
    editar = next((e for e in estudiantes if e["id"] == est_id), None)
    return render_template_string(HTML, estudiantes=estudiantes, mensaje="", editar=editar)

@app.route("/editar/<int:est_id>", methods=["POST"])
def editar(est_id):
    est = next((e for e in estudiantes if e["id"] == est_id), None)
    if est:
        est["nombre"]  = request.form.get("nombre", est["nombre"]).strip()
        est["codigo"]  = request.form.get("codigo", est["codigo"]).strip()
        est["carrera"] = request.form.get("carrera", est["carrera"]).strip()
        est["nota"]    = float(request.form.get("nota", est["nota"]))
    return redirect(url_for("index", msg="Estudiante actualizado correctamente."))

@app.route("/eliminar/<int:est_id>", methods=["POST"])
def eliminar(est_id):
    global estudiantes
    est = next((e for e in estudiantes if e["id"] == est_id), None)
    nombre = est["nombre"] if est else "Desconocido"
    estudiantes = [e for e in estudiantes if e["id"] != est_id]
    return redirect(url_for("index", msg=f"Estudiante '{nombre}' eliminado."))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)