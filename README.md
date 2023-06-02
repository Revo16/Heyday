# Compliance
This project involves scraping data from a Snowflake database to retrieve ASINs, reviews, ratings, and product names. The retrieved data is then processed and used to generate a JSONL file in the format: {"prompt": "", "completion": ""}. The format.py script is responsible for creating this file. The purpose of the JSONL file is to provide training data for fine-tuning an OpenAI model using the OpenAI API. Once we have the fine-tuned model, we can use it to classify all reviews for each product on whether the review is complaint or non-compliant.

Prerequisites

Before running the project, ensure that you have the following prerequisites:

Python 3.x installed on your system. Dependencies: snowflake-connector, pandas, json, emoji, openai. You can install the dependencies using pip: pip install snowflake-connector pandas openai

Usage

Follow the steps below to run the project:

Step 1: Scrape the Amazon reviews and create a JSON file. Open the scrape.py file. Update the Snowflake connection details (user, password, account) in the create_json() function. Run the scrape.py file to fetch the reviews and generate an output.json file. Step 2: Format the reviews and create a JSONL file for fine-tuning. Open the format.py file. Set the json_file_path variable to the path of the output.json file generated in Step 1. Customize the "" section in the formatted_review dictionary to represent the desired answer for each review. Run the format.py file to format the reviews and generate a reviews.jsonl file. Note: In addition to the reviews.jsonl file, you can also include AI-generated lines in the file for training purposes. You can manually modify the "completion" values in the reviews.jsonl file or add AI-generated lines directly to the file. Make sure the AI-generated lines are formatted correctly as per the JSONL format. After modifying the reviews.jsonl file and preparing it for training, you can save the final prepared JSONL file as mod.jsonl. This file should include both the original reviews and the AI-generated lines. Step 3: Fine-tune the OpenAI model using the prepared data. Open your command-line interface (CLI). Set the OpenAI API key you want to use by running the command: export OPENAI_API_KEY="<OPENAI_API_KEY>" Prepare the JSONL file, mod.jsonl, for better model understanding by running the command: openai tools fine_tunes.prepare_data -f mod.jsonl Train the model with the prepared data and desired base model by running the command: openai api fine_tunes.create -t <TRAIN_FILE_ID_OR_PATH> -m <BASE_MODEL> This command will return the name of the fine-tuned model. Step 4: Update compliance check in compliance.py and run the script. Open the compliance.py file. Set the engine variable in the check_compliance() function to the name of the fine-tuned model obtained in Step 3. Run the compliance.py file. This will create a new JSON file named complytwo.json which contains the original JSON data from scrape.py but with the non-compliant and compliant reviews separated for each product.

Note: You may need to adjust the file paths or modify the code to suit your specific requirements.

Additional Information

The Snowflake database connection details should be provided in the scrape.py file's create_json() function. The OpenAI API key should be set as an environment variable or directly in the CLI using the export command. The generated reviews.jsonl file contains prompts and ideal completions for the reviews, including "NA," "Compliant," and "Non-Compliant" answers. The compliance.py script should be updated with the name of the fine-tuned model obtained from Step 3 by setting the engine variable. Running the compliance.py script will create the complytwo.json file, which contains the original JSON data from scrape.py but with the reviews categorized as compliant or non-compliant for each product. Please feel free to customize the code and adapt it to your specific use case.

License

This project is licensed under the MIT License.

Acknowledgments

OpenAI for providing the powerful text processing capabilities. Snowflake for the Snowflake connector used to establish a connection to the database.
