import snowflake.connector
import pandas as pd
import json
import emoji

# Main function


def main():
    create_json()

# Function to create JSON file


def create_json():
    # Establish connection to Snowflake
    # Use AWS secrets manager in the future
    try:
        ctx = snowflake.connector.connect(
            user='user',
            password='pass',
            account='acc'
        )
        cursor = ctx.cursor()

        try:
            # Execute SQL query to fetch data from Snowflake
            cursor.execute(
                "SELECT ASIN, PRODUCT, RATING, REVIEW FROM DWH.PROD.FACT_AMAZON_REVIEWS WHERE REVIEW!='Rating only, no review provided' AND RATING IS NOT NULL"
            )

            # Fetch all the rows and column names
            data = cursor.fetchall()
            columns = [i[0] for i in cursor.description]

            results = {}
            # Iterate through each row of the data
            for row in data:
                asin = row[0]
                product = row[1]
                rating = row[2]
                review = row[3]
                if product not in results:
                    # Create a new entry for each product in the results dictionary
                    results[product] = {
                        "ASIN": asin, "PRODUCT": product, "RATING": [], "REVIEW": []}
                # Append the rating and review to the respective lists in the results dictionary
                results[product]["RATING"].append(rating)

                # Clean the review text by replacing certain Unicode characters and converting emojis to text
                half = review.replace("\u2019", "'")
                half = half.replace("\u2026", "...")
                half = half.replace("\u2014", "-")
                half = half.replace("\u201c", '"')
                half = half.replace("\u201d", '"')
                cleaned = emoji.demojize(half)
                results[product]["REVIEW"].append(cleaned)

            # Write the resulting dictionary as JSON to a file named 'output.json'
            with open('output.json', 'w') as json_file:
                json.dump(list(results.values()), json_file)

        finally:
            # Close the cursor and Snowflake connection
            cursor.close()
        ctx.close()

    except snowflake.connector.Error as e:
        print("Error connecting to Snowflake:", e)


# Entry point of the program
if __name__ == "__main__":
    main()
