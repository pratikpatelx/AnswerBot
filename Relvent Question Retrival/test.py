from google.cloud import bigquery



def query_stackoverflow():
    client = bigquery.Client()
    query_job = client.query(
        """
        SELECT a.id, title, c files, answer_count answers, favorite_count favs,
        view_count views, score
        FROM `bigquery-public-data.stackoverflow.posts_questions` a
        JOIN (
        SELECT CAST(REGEXP_EXTRACT(content,
        r'stackoverflow.com/questions/([0-9]+)/') AS INT64) id, COUNT(*) c,
        MIN(sample_path) sample_path
        FROM `fh-bigquery.github_extracts.contents_js`
        WHERE content LIKE '%stackoverflow.com/questions/%'
        GROUP BY 1
        HAVING id>0
        ORDER BY 2 DESC
        LIMIT 10) 
        b ON a.id=b.id
        ORDER BY c DESC
        """
    )

    results = query_job.result()  # Waits for job to complete.

    for row in results:
        print("{} {} {} {} {} {} {}".format(row.id, row.title, row.files, row.answers, row.favs, row.views, row.score))


if __name__ == "__main__":
    query_stackoverflow()