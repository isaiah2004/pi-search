import unittest
import os
import sqlite3
from unittest.mock import patch, MagicMock
from src.search_service import search_words_in_db, process_search_request
from src.utils.base32_converter import ascii_to_base32

class TestSearchService(unittest.TestCase):

    def setUp(self):
        # Setup test database
        self.test_db_path = 'test_pi_words.db'
        
        # Create a test database
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Create a table for testing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY,
                word TEXT
            )
        ''')
        
        # Insert some test data
        test_data = [
            (1, 'RQPC47'), # "example" in base32
            (2, 'RQP'),    # "ex" in base32
            (3, 'C47'),    # "ple" in base32
            (4, 'UNRELATED')
        ]
        cursor.executemany('INSERT OR IGNORE INTO words (id, word) VALUES (?, ?)', test_data)
        conn.commit()
        conn.close()
        
        # Test string
        self.test_string = "example"
        self.base32_string = ascii_to_base32(self.test_string)

    def tearDown(self):
        # Clean up test database
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_ascii_to_base32(self):
        # Test the conversion of a string to Base32
        expected_base32 = "RQPC47"  # "example" in base32
        self.assertEqual(self.base32_string, expected_base32)

    def test_search_words_in_db(self):
        # Test searching in the database with all match types
        results = search_words_in_db(self.test_string, self.test_db_path)
        
        # Check structure of results
        self.assertIn('full_matches', results)
        self.assertIn('partial_matches', results)
        self.assertIn('character_matches', results)
        
        # Verify full matches (exact match)
        self.assertEqual(results['full_matches'], [1])
        
        # Verify partial matches (contains the string)
        self.assertIn(1, results['partial_matches'])
        self.assertIn(2, results['partial_matches'])
        self.assertIn(3, results['partial_matches'])
        
        # Verify character matches
        self.assertTrue(len(results['character_matches']) > 0)

    def test_search_words_with_no_matches(self):
        # Test searching for a string that doesn't exist
        results = search_words_in_db("nonexistent", self.test_db_path)
        
        # Check that all result lists are empty
        self.assertEqual(results['full_matches'], [])
        self.assertEqual(results['partial_matches'], [])
        self.assertEqual(results['character_matches'], [])

    @patch('src.search_service.search_words_in_db')
    def test_process_search_request(self, mock_search):
        # Setup mock
        mock_search.return_value = {
            'full_matches': [1],
            'partial_matches': [1, 2],
            'character_matches': [1, 2, 3]
        }
        
        # Test valid input
        result = process_search_request("example")
        mock_search.assert_called_once_with("example")
        self.assertEqual(result, {
            'full_matches': [1],
            'partial_matches': [1, 2],
            'character_matches': [1, 2, 3]
        })
    
    def test_process_search_request_empty_input(self):
        # Test empty input
        result = process_search_request("")
        self.assertEqual(result, {"error": "Input string cannot be empty."})

    def test_process_search_request_none_input(self):
        # Test None input
        result = process_search_request(None)
        self.assertEqual(result, {"error": "Input string cannot be empty."})
    
    @patch('sqlite3.connect')
    def test_database_connection_error(self, mock_connect):
        # Simulate a database connection error
        mock_connect.side_effect = sqlite3.Error("Database connection error")
        
        with self.assertRaises(sqlite3.Error):
            search_words_in_db("example", "nonexistent_path.db")
            
    def test_search_with_special_characters(self):
        # Test searching with special characters
        special_string = "example!@#"
        results = search_words_in_db(special_string, self.test_db_path)
        # Special characters should be handled by ascii_to_base32
        self.assertIsInstance(results, dict)
        
    def test_search_case_sensitivity(self):
        # Test that the search is case insensitive
        uppercase_string = "EXAMPLE"
        results = search_words_in_db(uppercase_string, self.test_db_path)
        # The base32 conversion should handle case properly
        self.assertEqual(results['full_matches'], [1])
        
    def test_search_with_numeric_input(self):
        # Test searching with numeric input
        # Add numeric test data to the database
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO words (id, word) VALUES (5, ?)', (ascii_to_base32("123"),))
        conn.commit()
        conn.close()
        
        results = search_words_in_db("123", self.test_db_path)
        self.assertEqual(results['full_matches'], [5])
        
    @patch('os.path.exists')
    def test_nonexistent_database_path(self, mock_exists):
        # Test behavior when database path doesn't exist
        mock_exists.return_value = False
        
        with self.assertRaises(Exception):
            results = search_words_in_db("example", "nonexistent_db.db")

if __name__ == "__main__":
    unittest.main()

    def test_search_partial_matches(self):
        # Test searching for partial matches in the database
        results = search_words_in_db(self.base32_string, match_type='partial')
        self.assertIsInstance(results, list)
        # Add assertions to check the contents of results

    def test_search_character_wise_matches(self):
        # Test searching for character-wise matches in the database
        results = search_words_in_db(self.base32_string, match_type='character-wise')
        self.assertIsInstance(results, list)
        # Add assertions to check the contents of results
        class TestSearchService(unittest.TestCase):

            def setUp(self):
                # Setup test database
                self.test_db_path = 'test_pi_words.db'
                
                # Create a test database
                conn = sqlite3.connect(self.test_db_path)
                cursor = conn.cursor()
                
                # Create a table for testing
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS words (
                        id INTEGER PRIMARY KEY,
                        word TEXT
                    )
                ''')
                
                # Insert some test data
                test_data = [
                    (1, 'RQPC47'), # "example" in base32
                    (2, 'RQP'),    # "ex" in base32
                    (3, 'C47'),    # "ple" in base32
                    (4, 'UNRELATED')
                ]
                cursor.executemany('INSERT OR IGNORE INTO words (id, word) VALUES (?, ?)', test_data)
                conn.commit()
                conn.close()
                
                # Test string
                self.test_string = "example"
                self.base32_string = ascii_to_base32(self.test_string)

            def tearDown(self):
                # Clean up test database
                if os.path.exists(self.test_db_path):
                    os.remove(self.test_db_path)

            def test_ascii_to_base32(self):
                # Test the conversion of a string to Base32
                expected_base32 = "RQPC47"  # "example" in base32
                self.assertEqual(self.base32_string, expected_base32)

            def test_search_words_in_db(self):
                # Test searching in the database with all match types
                results = search_words_in_db(self.test_string, self.test_db_path)
                
                # Check structure of results
                self.assertIn('full_matches', results)
                self.assertIn('partial_matches', results)
                self.assertIn('character_matches', results)
                
                # Verify full matches (exact match)
                self.assertEqual(results['full_matches'], [1])
                
                # Verify partial matches (contains the string)
                self.assertIn(1, results['partial_matches'])
                self.assertIn(2, results['partial_matches'])
                self.assertIn(3, results['partial_matches'])
                
                # Verify character matches
                self.assertTrue(len(results['character_matches']) > 0)

            def test_search_words_with_no_matches(self):
                # Test searching for a string that doesn't exist
                results = search_words_in_db("nonexistent", self.test_db_path)
                
                # Check that all result lists are empty
                self.assertEqual(results['full_matches'], [])
                self.assertEqual(results['partial_matches'], [])
                self.assertEqual(results['character_matches'], [])

            @patch('src.search_service.search_words_in_db')
            def test_process_search_request(self, mock_search):
                # Setup mock
                mock_search.return_value = {
                    'full_matches': [1],
                    'partial_matches': [1, 2],
                    'character_matches': [1, 2, 3]
                }
                
                # Test valid input
                result = process_search_request("example")
                mock_search.assert_called_once_with("example")
                self.assertEqual(result, {
                    'full_matches': [1],
                    'partial_matches': [1, 2],
                    'character_matches': [1, 2, 3]
                })
            
            def test_process_search_request_empty_input(self):
                # Test empty input
                result = process_search_request("")
                self.assertEqual(result, {"error": "Input string cannot be empty."})

            def test_process_search_request_none_input(self):
                # Test None input
                result = process_search_request(None)
                self.assertEqual(result, {"error": "Input string cannot be empty."})
            
            @patch('sqlite3.connect')
            def test_database_connection_error(self, mock_connect):
                # Simulate a database connection error
                mock_connect.side_effect = sqlite3.Error("Database connection error")
                
                with self.assertRaises(sqlite3.Error):
                    search_words_in_db("example", "nonexistent_path.db")
if __name__ == "__main__":
    unittest.main()