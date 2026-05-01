from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder=".")

def solve_ap(data):
    # Extract basic variables
    a = float(data['a']) if data.get('a') else None
    d = float(data['d']) if data.get('d') else None
    n = int(data['n']) if data.get('n') else None
    an = float(data['an']) if data.get('an') else None
    sn = float(data['sn']) if data.get('sn') else None

    # ARCHETYPE 1, 2, 3 Logic
    if a is not None and d is not None and n is not None:
        an = a + (n - 1) * d
        sn = (n / 2) * (2 * a + (n - 1) * d)
    elif a is not None and d is not None and an is not None:
        n_calc = ((an - a) / d) + 1
        if n_calc <= 0 or not n_calc.is_integer():
            return {"error": "These values do not form a valid AP."}
        n = int(n_calc)
        sn = (n / 2) * (a + an)
    elif a is not None and n is not None and sn is not None:
        d = (sn - (n * a)) * 2 / (n * (n - 1))
        an = a + (n - 1) * d
    else:
        return {"error": "Please provide at least 3 values (e.g., a, d, n)."}

    # Generate progression array for the frontend graph
    progression = [a + i * d for i in range(n)]
    labels = [f"Term {i+1}" for i in range(n)]

    return {
        "a": round(a, 4), "d": round(d, 4), "n": n, "an": round(an, 4), "sn": round(sn, 4),
        "labels": labels,
        "progression": progression
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    result = solve_ap(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
