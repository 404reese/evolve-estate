from flask import Flask, request, jsonify, render_template
import openai
from google.cloud import bigquery

app = Flask(__name__)

# Initialize OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key

# Initialize BigQuery client
bq_client = bigquery.Client()

# Define a function to generate BigQuery SQL query
def generate_bigquery_query(user_inputs):
    prompt = f"Generate a BigQuery SQL query based on the following inputs: {user_inputs}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    query = response['choices'][0]['message']['content']
    return query

# Define a function to execute the query
def execute_query(query):
    query_job = bq_client.query(query)
    results = query_job.result()  # Wait for the job to complete
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('input')
    # Here you would implement logic to ask a series of questions
    # For simplicity, let's assume we directly generate a query
    user_inputs = user_input  # Collect user inputs as needed
    query = generate_bigquery_query(user_inputs)
    
    # Execute the query and get results
    results = execute_query(query)
    
    # Convert results to a list of dictionaries
    results_list = [dict(row) for row in results]
    
    return jsonify({'query': query, 'results': results_list})

if __name__ == '__main__':
    app.run(debug=True)
