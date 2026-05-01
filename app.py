from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__, template_folder=".")

def solve_ap(data):
    mode = data.get('mode', 'basic')

    if mode == 'basic':
        # [Keep your existing 'basic' logic here...]
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
        # [Keep your existing 'two_terms' logic here...]
        n1, v1 = int(data['n1']), float(data['v1'])
        n2, v2 = int(data['n2']), float(data['v2'])
        d = (v1 - v2) / (n1 - n2)
        a = v1 - (n1 - 1) * d
        n = int(data['target_n']) if data.get('target_n') else 10
        an = a + (n - 1) * d
        sn = (n / 2) * (2 * a + (n - 1) * d)

    elif mode == 'three_terms':
        # --- ARCHETYPE 5: Symmetric Selection (Sum & Product of 3 terms) ---
        try:
            sum_3 = float(data['sum_3'])
            prod_3 = float(data['prod_3'])
        except (ValueError, TypeError):
            return {"error": "Please provide both the sum and product of the 3 terms."}

        # Symmetric assumption: terms are (x-d), x, (x+d)
        # 1. Solve for x (the middle term)
        x = sum_3 / 3.0
        
        # 2. Solve for d^2 using Product = x(x^2 - d^2)
        # x^2 - d^2 = prod / x  =>  d^2 = x^2 - (prod / x)
        d_sq = (x ** 2) - (prod_3 / x)
        
        if d_sq < 0:
            return {"error": "No real AP exists for these values (d would be imaginary)."}
            
        d = math.sqrt(d_sq) # Note: Taking positive root yields one of the valid APs
        a = x - d # The actual first term
        
        n = int(data['target_n']) if data.get('target_n') else 3
        an = a + (n - 1) * d
        sn = (n / 2) * (2 * a + (n - 1) * d)
    
    elif mode == 'divisibility':
        # --- ARCHETYPE 6: Divisibility Ranges & Constraints ---
        try:
            r_start = int(data['r_start'])
            r_end = int(data['r_end'])
            divisor = int(data['divisor'])
            remainder = int(data['remainder']) if data.get('remainder') else 0
        except (ValueError, TypeError):
            return {"error": "Please provide the start range, end range, and divisor."}

        if divisor == 0:
            return {"error": "Divisor cannot be zero."}
            
        d = divisor
        
        # 1. Find the first valid number (a) >= r_start
        offset_start = (r_start - remainder) % d
        a = r_start if offset_start == 0 else r_start + (d - offset_start)
        
        # 2. Find the last valid number (an) <= r_end
        offset_end = (r_end - remainder) % d
        an = r_end - offset_end
        
        if a > r_end or an < r_start or a > an:
            return {"error": "No numbers in this range match the criteria."}
            
        # 3. Calculate the number of terms (n)
        n = int(((an - a) / d) + 1)
        
        # 4. Calculate the sum (Sn)
        sn = (n / 2) * (a + an)

    # Generate the progression for the graph
    # Generate the progression for the graph (Cap at 50 terms to prevent browser freezing)
    graph_n = min(n, 50)
    progression = [a + i * d for i in range(graph_n)]
    labels = [f"Term {i+1}" for i in range(graph_n)]

    return {
        "a": round(a, 4), "d": round(d, 4), "n": n, "an": round(an, 4), "sn": round(sn, 4),
        "labels": labels,
        "progression": [round(p, 4) for p in progression]
    }

# [Keep your index and calculate routes here]
@app.route("/")
def index():
    return render_template("index4.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    result = solve_ap(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
