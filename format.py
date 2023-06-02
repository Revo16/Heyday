import json

def format_reviews(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    formatted_reviews = []

    for i, item in enumerate(data[:100]):  # Iterate through the first 100 products
        reviews = item['REVIEW'][:10]  # Get the first ten reviews
        for review in reviews:
            formatted_review = {
                "prompt": review,
                "completion": "<ideal generated text>"
            }
            formatted_reviews.append(formatted_review)

    # Save formatted reviews as JSONL file
    with open('reviews.jsonl', 'w') as jsonl_file:
        for review in formatted_reviews:
            json.dump(review, jsonl_file)
            jsonl_file.write('\n')

# Example usage
json_file_path = 'out.json'
format_reviews(json_file_path)