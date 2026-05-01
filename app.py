from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder=".")

def solve_ap(data):
    mode = data.get('mode', 'basic')

    if mode == 'basic':
        a = float(data['a']) if data.get('a') else None
        d = float(data['d']) if data.get('d') else None
        n = int(data['n']) if data.get('n') else None
        an = float(data['an']) if data.get('an') else None
        sn = float(data['sn']) if data.get('sn') else None

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

    elif mode == 'two_terms':
        # --- ARCHETYPE 2: Systems of Equations ---
        try:
            n1 = int(data['n1'])
            v1 = float(data['v1'])
            n2 = int(data['n2'])
            v2 = float(data['v2'])
        except (ValueError, TypeError):
            return {"error": "Please fill out all 4 fields for the two terms."}

        if n1 == n2:
            return {"error": "Positions (n1 and n2) must be different."}

        # Simultaneous Equation Logic: d = (v1 - v2) / (n1 - n2)
        d = (v1 - v2) / (n1 - n2)
        
        # Substitute d back into the first equation to find 'a'
        # v1 = a + (n1 - 1)d  =>  a = v1 - (n1 - 1)d
        a = v1 - (n1 - 1) * d

        # Check if the user wants to find a specific target term/sum
        n = int(data['target_n']) if data.get('target_n') else 10 # Default to 10 for graphing
        an = a + (n - 1) * d
        sn = (n / 2) * (2 * a + (n - 1) * d)

    # Generate the progression for the graph
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
