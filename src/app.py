import os

from flask import Flask, jsonify, render_template_string, request
from flask_wtf.csrf import CSRFProtect

from src.dictionary import Dictionary
from src.nth_letter import nth_letter
from src.shop import get_total

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
try:
    app.config.from_prefixed_env()
except AttributeError:
    pass
csrf = CSRFProtect(app)

# Preload sample dictionary entries for the demo page.
dictionary = Dictionary()
dictionary.newentry("apple", "A fruit that grows on trees")
dictionary.newentry("banana", "A long yellow fruit")
dictionary.newentry("python", "A programming language")
dictionary.newentry("flask", "A lightweight Python web framework")

price_catalog = {
    "socks": 5,
    "shoes": 60,
    "sweater": 30,
    "hat": 20,
    "shirt": 25,
    "jeans": 40,
    "jacket": 80,
    "cap": 10,
}

home_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>EPAM Python Task</title>
    <style>
      :root {
        color-scheme: dark;
        color: #1f2937;
        background: #f8fafc;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
          "Segoe UI", sans-serif;
        box-sizing: border-box;
      }
      *, *::before, *::after {
        box-sizing: inherit;
      }
      body {
        margin: 0;
        padding: 0;
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
      }
      .page {
        width: min(100%, 980px);
        padding: 32px;
      }
      header {
        margin-bottom: 24px;
      }
      h1 {
        margin: 0 0 12px;
        font-size: clamp(2rem, 2.5vw, 3rem);
        color: #111827;
      }
      p.lead {
        margin: 0;
        color: #475569;
      }
      .grid {
        display: grid;
        gap: 20px;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      }
      .card {
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 22px;
        background: #ffffff;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.06);
      }
      .card h2 {
        margin-top: 0;
        margin-bottom: 14px;
        font-size: 1.25rem;
        color: #111827;
      }
      .field {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-bottom: 12px;
      }
      input,
      button,
      textarea {
        width: 100%;
        max-width: 100%;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 12px 14px;
        font-size: 0.95rem;
      }
      button {
        width: 100%;
        margin-bottom: 12px;
        background: #2563eb;
        color: white;
        border: none;
        cursor: pointer;
        transition: transform 0.16s ease, background 0.16s ease;
      }
      button:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
      }
      pre {
        white-space: pre-wrap;
        word-break: break-word;
        background: #f1f5f9;
        padding: 14px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        min-height: 80px;
      }
      .notice {
        margin-top: 16px;
        color: #475569;
      }
    </style>
  </head>
  <body>
    <main class="page">
      <header>
        <h1>EPAM Python Task</h1>
      </header>

      <div class="grid">
        <section class="card" id="dictionary-card">
          <h2>Diccionario</h2>
          <div class="field">
            <label for="dictionary-word">Palabra</label>
            <input id="dictionary-word" type="text" placeholder="apple" value="" />
          </div>
          <div class="field">
            <label for="dictionary-definition">Definición</label>
            <input id="dictionary-definition" type="text" placeholder="Una fruta que crece en los árboles" />
          </div>
          <button id="dictionary-add" type="button">Agregar al diccionario</button>
          <div class="field">
            <label for="dictionary-search-word">Buscar palabra</label>
            <input id="dictionary-search-word" type="text" placeholder="apple" value="" />
          </div>
          <button id="dictionary-submit" type="button">Buscar definición</button>
          <pre id="dictionary-result">Introduce una palabra y presiona Buscar definición.</pre>
        </section>

        <section class="card" id="shop-card">
          <h2>Calculadora del carrito</h2>
          <div class="field">
            <label for="shop-new-item">Nuevo artículo</label>
            <input id="shop-new-item" type="text" placeholder="watch" />
          </div>
          <div class="field">
            <label for="shop-new-price">Precio</label>
            <input id="shop-new-price" type="text" placeholder="55" />
          </div>
          <button id="shop-add" type="button">Agregar artículo</button>
          <div class="field">
            <label for="shop-items">Artículos</label>
            <input id="shop-items" type="text" placeholder="socks,shoes" value="socks,shoes" />
          </div>
          <div class="field">
            <label for="shop-tax">Tax</label>
            <input id="shop-tax" type="text" placeholder="0.09" value="0.09" />
          </div>
          <button id="shop-submit" type="button">Calcular total</button>
          <pre id="shop-result">Introduce los artículos y el valor del tax.</pre>
        </section>

        <section class="card" id="nth-card">
          <h2>Nth Letter</h2>
          <div class="field">
            <label for="nth-words">Palabras separadas por coma</label>
            <input id="nth-words" type="text" placeholder="yoda,best,has" value="yoda,best,has" />
          </div>
          <button id="nth-submit" type="button">Concatenar letras</button>
          <pre id="nth-result">Introduce palabras y presiona Concatenar letras.</pre>
        </section>
      </div>

    </main>

    <script>
      async function getJson(url) {
        const response = await fetch(url);
        if (!response.ok) {
          const error = await response.json().catch(() => ({ error: response.statusText }));
          throw new Error(error.error || response.statusText);
        }
        return response.json();
      }

      function formatResult(result) {
        if (typeof result === 'string') {
          return result;
        }

        if (result.definition !== undefined) {
          return `${result.word}: ${result.definition}`;
        }

        if (result.message !== undefined) {
          const details = result.word && result.definition ? `\n${result.word}: ${result.definition}` : '';
          return `${result.message}${details}`;
        }

        if (result.total !== undefined) {
          const items = Array.isArray(result.items) ? result.items.join(', ') : result.items;
          return `Artículos: ${items}\nTax: ${result.tax}\nTotal: ${result.total}`;
        }

        if (result.result !== undefined) {
          const words = Array.isArray(result.words) ? result.words.join(', ') : result.words;
          return `Resultado: ${result.result}${words ? `\nPalabras: ${words}` : ''}`;
        }

        return JSON.stringify(result, null, 2);
      }

      async function updateResult(elementId, callback) {
        const element = document.getElementById(elementId);
        element.textContent = 'Cargando...';
        try {
          const result = await callback();
          element.textContent = formatResult(result);
        } catch (error) {
          element.textContent = String(error);
        }
      }

      document.getElementById('dictionary-add').addEventListener('click', async () => {
        const word = document.getElementById('dictionary-word').value.trim();
        const definition = document.getElementById('dictionary-definition').value.trim();
        const addButton = document.getElementById('dictionary-add');
        const searchButton = document.getElementById('dictionary-submit');

        if (!word || !definition) {
          document.getElementById('dictionary-result').textContent = 'Ingresa palabra y definición válidas.';
          return;
        }

        addButton.disabled = true;
        searchButton.disabled = true;
        try {
          await updateResult('dictionary-result', () => getJson(`/dictionary/add?word=${encodeURIComponent(word)}&definition=${encodeURIComponent(definition)}`));
          document.getElementById('dictionary-search-word').value = word;
        } finally {
          addButton.disabled = false;
          searchButton.disabled = false;
        }
      });

      document.getElementById('dictionary-submit').addEventListener('click', () => {
        const word = document.getElementById('dictionary-search-word').value.trim();
        if (!word) {
          document.getElementById('dictionary-result').textContent = 'Ingresa una palabra válida para buscar.';
          return;
        }
        updateResult('dictionary-result', () => getJson(`/dictionary/${encodeURIComponent(word)}`));
      });

      document.getElementById('shop-add').addEventListener('click', () => {
        const item = document.getElementById('shop-new-item').value.trim();
        const price = document.getElementById('shop-new-price').value.trim();
        if (!item || !price) {
          document.getElementById('shop-result').textContent = 'Ingresa nombre y precio del artículo.';
          return;
        }
        updateResult('shop-result', () => getJson(`/shop/add?item=${encodeURIComponent(item)}&price=${encodeURIComponent(price)}`));
      });

      document.getElementById('shop-submit').addEventListener('click', () => {
        const items = document.getElementById('shop-items').value.trim();
        const tax = document.getElementById('shop-tax').value.trim();
        updateResult('shop-result', () => getJson(`/shop/total?items=${encodeURIComponent(items)}&tax=${encodeURIComponent(tax)}`));
      });

      document.getElementById('nth-submit').addEventListener('click', () => {
        const words = document.getElementById('nth-words').value.trim();
        updateResult('nth-result', () => getJson(`/nth-letter?words=${encodeURIComponent(words)}`));
      });
    </script>
  </body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(home_template)


@app.route("/dictionary/<word>", methods=["GET"])
def lookup(word):
    result = dictionary.look(word)
    if result.startswith("Can't find"):
        return jsonify({"word": word, "error": result}), 404
    return jsonify({"word": word, "definition": result})


@app.route("/dictionary/add", methods=["GET"])
def dictionary_add():
    word = request.args.get("word", "").strip()
    definition = request.args.get("definition", "").strip()

    if not word or not definition:
        return jsonify({"error": "Both word and definition are required."}), 400

    dictionary.newentry(word, definition)
    return jsonify({"word": word, "definition": definition, "message": "Palabra agregada al diccionario."})


@app.route("/shop/catalog", methods=["GET"])
def shop_catalog():
    return jsonify({"catalog": price_catalog})


@app.route("/shop/add", methods=["GET"])
def shop_add():
    item = request.args.get("item", "").strip()
    price = request.args.get("price", "").strip()

    if not item or not price:
        return jsonify({"error": "Item name and price are required."}), 400

    try:
        price_value = float(price)
    except ValueError:
        return jsonify({"error": "Price must be a number."}), 400

    if price_value < 0:
        return jsonify({"error": "Price must be greater than or equal to zero."}), 400

    price_catalog[item] = price_value
    return jsonify({"item": item, "price": price_value, "catalog": price_catalog, "message": "Artículo agregado al catálogo."})


@app.route("/shop/total", methods=["GET"])
def shop_total():
    items = request.args.get("items", "")
    tax = request.args.get("tax", "0")

    try:
        tax_value = float(tax)
    except ValueError:
        return jsonify({"error": "Invalid tax value. Use a decimal like 0.09."}), 400

    item_list = [item.strip() for item in items.split(",") if item.strip()]
    if not item_list:
        return jsonify({"error": "Use ?items=item1,item2&tax=0.09"}), 400

    total = get_total(price_catalog, item_list, tax_value)
    return jsonify({"items": item_list, "tax": tax_value, "total": total})


@app.route("/nth-letter", methods=["GET"])
def nth_letter_route():
    words = request.args.get("words", "")
    if not words:
        return jsonify({"error": "Query parameter 'words' is required."}), 400

    words_list = [word.strip() for word in words.split(",") if word.strip()]
    if not words_list:
        return jsonify({"error": "Provide words separated by commas."}), 400

    result = nth_letter(words_list)
    return jsonify({"words": words_list, "result": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="127.0.0.1", port=port)
