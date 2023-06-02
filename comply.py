import json
import openai

# OpenAI API configuration
openai.api_key = 'key'

# OpenAI API call to determine compliance


def check_compliance(review):
    response = openai.Completion.create(
        engine='ada:ft-personal-2023-06-02-00-12-51',
        prompt=review,
        stop=[" \n"]
    )

    return response.choices[0].text.strip()

# Function to process the reviews and create a new JSON file


def process_reviews(input_file_path, output_file_path):
    # Load the input JSON file
    with open(input_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Create a new list to store the processed data
    processed_data = []

    # Iterate through each item in the JSON data
    for count, item in enumerate(data):
        asin = item['ASIN']
        product = item['PRODUCT']
        rating = item['RATING']
        reviews = item['REVIEW']

        # Separate compliant and non-compliant reviews
        compliant_reviews = []
        non_compliant_reviews = []
        print("Sorting Product " + str(count + 1) + "'s Reviews...")

        for index, review in enumerate(reviews):
            # Check compliance only if rating is 3 stars or less
            compliance = check_compliance(review + " ->")
            print("Review:", review)
            print("Comply:", compliance)
            print()

            # Categorize the review based on compliance
            if "non-compliant" in compliance:
                non_compliant_reviews.append(review)
            else:
                compliant_reviews.append(review)

            # Break the loop after 10 reviews
            """
            if index == 9:
                break
            """

        # Create a new item dictionary with the desired fields
        new_item = {
            'asin': asin,
            'product': product,
            'rating': rating,
            'compliant_reviews': compliant_reviews,
            'non_compliant_reviews': non_compliant_reviews,
        }

        # Add the new item to the processed data list
        processed_data.append(new_item)
        print("Finished w/ Product", count + 1)
        break

    # Save the processed data to the output JSON file
    with open(output_file_path, 'w') as json_file:
        json.dump(processed_data, json_file)


# Example usage
input_file_path = 'output.json'  # Path to the input JSON file
output_file_path = 'complytwo.json'  # Path to the output JSON file

process_reviews(input_file_path, output_file_path)
