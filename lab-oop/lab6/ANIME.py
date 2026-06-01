import requests
from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    try:
        # Використовуємо пряме посилання на API v4
        url = "https://api.jikan.moe/v4/anime/54595/episodes"
        response = requests.get(url)

        # Перевіряємо, чи успішний запит (статус 200)
        if response.status_code == 200:
            data = response.json()
            episodes_list = data['data']

            html = "<h1>Список епізодів (Прямий запит v4)</h1>"
            for ep in episodes_list:
                title = ep.get('title', 'Без назви')
                score = ep.get('score') or "немає"
                html += (
                    f"<p>Епізод {ep['mal_id']}: <b>{title}</b> — "
                    f"Оцінка: {score}</p>"
                )
            return html
        else:
            return f"Помилка сервера Jikan: {response.status_code}"

    except Exception as e:
        return f"Помилка виконання: {e}"


@app.route('/season')
def season():
    try:
        # Прямий запит на поточний сезон
        url = "https://api.jikan.moe/v4/seasons/now"
        response = requests.get(url)
        data = response.json()

        html = "<h1>Аніме поточного сезону</h1><ul>"
        for anime in data['data'][:15]:  # беремо перші 15
            title = anime['title']
            score = anime['score'] or "очікується"
            html += f"<li>{title} (Оцінка: {score})</li>"
        html += "</ul><br><a href='/'>Назад</a>"
        return html
    except Exception as e:
        return f"Помилка: {e}"


if __name__ == '__main__':
    app.run(debug=True)