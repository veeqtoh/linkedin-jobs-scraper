from flask import Flask
from scrape import links, create_job_csv

app = Flask(__name__)

@app.route('/')
def hello():
    for country in links:
        create_job_csv(links[country], country)

if __name__ == '__main__':
    app.run()
