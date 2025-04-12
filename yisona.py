import json
import sqlite3

class Yisona:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{json_file_path}' not found.")
            self.data = {}
        except json.JSONDecodeError:
            print(f"Error: File '{json_file_path}' contains invalid JSON.")
            self.data = {}

    def get_json(self, key):
        keys = str(key).split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(str(k))
            else:
                return None
        return value

    def write_json(self, key, value):
        keys = str(key).split('.')
        current = self.data
        
        # Navigate through nested structure
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value at the final key
        current[keys[-1]] = value
        
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            print(f"Successfully updated key '{key}'.")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def get_json_as_number(self, key):
        value = self.get_json(key)
        if isinstance(value, (int, float)):
            return value
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def create_json(self, key, value):
        if not isinstance(self.data, dict):
            print("Error: JSON data is not in the expected dictionary format.")
            return
        if str(key) in self.data:
            print(f"Warning: Key '{key}' already exists and will be overwritten.")
        self.data[str(key)] = value  # Ensure key is treated as a string
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            print(f"Successfully created JSON entry with key '{key}'.")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def get_sqlite(self, db_path, query):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            connection.close()
            return results
        except sqlite3.Error as e:
            print(f"SQLite query error: {e}")
            return []

    def cc(self, key, default_value):
        keys = str(key).split('.')
        current = self.data
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        if keys[-1] in current:
            return True
        current[keys[-1]] = default_value
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error writing to file: {e}")
        return False

# Usage example
if __name__ == "__main__":
    yisona = Yisona("test.json")
    value = yisona.get_json(123)  # Example with integer key
    print(f"Retrieved value is: {value}")
    yisona.write_json(456, "new value")  # Example with integer key
    key_exists = yisona.cc(789, "default_value")  # Example with integer key
    print(f"Key existed: {key_exists}")
