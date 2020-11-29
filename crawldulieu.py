import requests
import sqlite3
import time

link_url = 'https://api.github.com/repos/awesome-jobs/vietnam/issues'
database = 'jobs.db'
conn = sqlite3.connect(database)
c = conn.cursor()
c.execute('''CREATE TABLE jobs (job_id integer,
            link_job text, title text, postdate text, contents text)''')
conn.commit()


def crawl_jobs():
    ses = requests.Session()
    page = 1
    while True:
        params = {'page':page}
        reps = ses.get(link_url, params=params)
        data = reps.json()
        if not data:
            break
        for jobs in data:
            c.execute('''INSERT INTO jobs VALUES (?, ?, ?, ?, ?)''',
                (jobs['id'], jobs['html_url'], jobs['title'],
                    jobs['created_at'][:10], jobs['body']))
        conn.commit()
        page +=1
        time.sleep(5)
    conn.close()
    return


def main():
    crawl_jobs()

 
if __name__ == "__main__":
     main()