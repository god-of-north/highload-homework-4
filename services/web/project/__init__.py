import os
import  json
import psycopg2

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")


@app.route("/")
def index():
    return "Hello"


@app.route("/hard_query")
def hard_query():
    q = """select t.category, t.city from 
        (select c3."name" as category, c2.city, sum(r.return_date - r.rental_date) as rent_time, rank() over (partition by c2.city order by sum(r.return_date - r.rental_date) desc) as rnk from rental r 
        join customer c on c.customer_id = r.customer_id 
        join address a on a.address_id = c.customer_id 
        join city c2 on c2.city_id = a.city_id 
        join inventory i on i.inventory_id = r.inventory_id 
        join film_category fc on fc.film_id = i.film_id 
        join category c3 on c3.category_id = fc.category_id 
        where r.return_date is not null and r.rental_date is not NULL
        group  by c2.city, category) t
    where t.rnk = 1 and (lower(t.city) like 'a%' or t.city like '%-%');"""
    
    ret = "error"

    conn = psycopg2.connect(database="pagila", user="hello_flask", password="hello_flask", host="localhost", port=5432)
    try:
        with conn.cursor() as cur:
            cur.execute(q)
            all = cur.fetchall()
            ret = dict.fromkeys(range(len(all)), all)
    finally:
        conn.close()

    return ret


@app.route("/add_film", methods=["POST"])
def add_film():
    if request.method == "POST":
        if request.form:
            data = json.loads(list(request.form)[0])

            conn = psycopg2.connect(database="pagila", user="hello_flask", password="hello_flask", host="localhost", port=5432)
            try:
                with conn.cursor() as cur:
                    cur.execute(f"INSERT INTO film(title, description, release_year, rating, language_id) VALUES('{data['title']}', '{data['description']}', {data['release_year']}, '{data['rating']}', 1);")
            finally:
                conn.close()


        return jsonify(status="added")
    return jsonify(status="fail")

@app.route("/cache_test")
def cache_test():
    pass

