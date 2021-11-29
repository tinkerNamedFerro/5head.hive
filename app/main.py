from flask import Flask
from .worker import celery

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config.Config")

@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

with app.app_context():
    from . import routes
    from .dash import demo, iris_kmeans, crossfilter_example
    from .dash.biz_insights import bizCoinMentions

    app = demo.init_dash(app)
    app = bizCoinMentions.init_dash(app)
    app = iris_kmeans.init_dash(app)
    app = crossfilter_example.init_dash(app)

if __name__ == "__main__":
    # Only for debugging while developing
    task = celery.send_task('tasks.add', args=[4, 3], kwargs={})
    app.run(host="0.0.0.0", debug=True, port=8080)
