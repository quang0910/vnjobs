from flask import Flask, Markup
import time
import markdown
import sqlite3
app = Flask(__name__)
conn = sqlite3.connect('jobs.db', check_same_thread=False)
c = conn.cursor()

@app.route('/')
def list_jobs():
    data = c.execute("SELECT * FROM jobs").fetchall()
    conn.commit()
    time.sleep(3)
    line = []
    result = "<ul>"
    order = 1
    for job_id, link, title, date, details in data:
        a = '''{0}.<a href='/jobs/{0}'>{2}</a><p><small>
        <em>Date create: {3}. Job id :{1}</em></small></p>'''.format(job_id, link, title, date)
        line.append(a)
        order += 1
    result = result + "<br>" + "<br>".join(line) + "</ul>"
    format_result = ''' <!DOCTYPE html>
                        <html>
                    <head>
                    <title>MY FIRST WEB</title>
                    </head>
                    <body>

                    <h1>lIST OPEN JOBS</h1>
                    Click each link below for more informations
                    {}

                    </body>
                    </html> '''.format(result)
    return format_result


@app.route("/jobs/<string:job_id_input>")
def job_detail(job_id_input):
    data = c.execute("SELECT * FROM jobs WHERE job_id=:job_id", {'job_id':job_id_input}).fetchall()
    conn.commit()
    try:
        job_id, link, title, date, details = data[-1]
        job_description = Markup(markdown.markdown(details))
        a = "<p>{}</p>".format(job_description)
        b = "<h2>{}</h2>".format(title)
        result = "<ul>" + "<br>" + b + "<br>" + a + "</ul>"
    except:
        result = "<p style='text-align:center;'>NO JOB INFORMATION</p>" 
    
    return result


if __name__ == "__main__":
    app.run(debug=True)
