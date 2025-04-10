# pi-digits-search-api
Total hexadecimal digits in the file: 1,000,000,001
## Overview
The `pi-digits-search-api` is a Python-based API that allows users to search for words within the digits of pi. The API accepts string inputs, converts them to their Base32 equivalents, and searches for full words, partial matches, and character-wise matches in a SQLite database containing words derived from pi.

## Project Structure
```
pi-digits-search-api
├── src
│   ├── app.py                # Entry point of the API application
│   ├── search_service.py      # Logic for processing input strings and searching
│   ├── database
│   │   └── db_manager.py      # Manages database connections and queries
│   ├── utils
│   │   ├── base32_converter.py # Converts ASCII strings to Base32
│   │   └── pi_searcher.py      # Performs searches in the pi_words.db
│   └── models
│       └── search_result.py     # Defines data models for search results
├── tests
│   ├── test_app.py            # Unit tests for app.py
│   ├── test_search_service.py  # Unit tests for search_service.py
│   └── test_base32_converter.py # Unit tests for base32_converter.py
├── static
│   └── pi_base32_1b.txt       # Digits of pi in Base32 format
├── database
│   └── pi_words.db            # SQLite database containing searchable words
├── requirements.txt            # Lists project dependencies
├── .gitignore                  # Specifies files to ignore in version control
└── README.md                   # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd pi-digits-search-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the API:
   ```
   python src/app.py
   ```

2. Send a POST request to the API with a string input to search for:
   ```
   POST /search
   {
       "input_string": "your_string_here"
   }
   ```

3. The API will return the indexes of found words in the pi digits.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.