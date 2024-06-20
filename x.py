from bs4 import BeautifulSoup


def render_html_or_none(input_string):
    try:
        # Attempt to parse the input string as HTML
        soup = BeautifulSoup(input_string, 'html.parser')
        
        if not soup.find():
            return False , None
        
        # Return the rendered text from the HTML
        str = soup.get_text()
        if len(str) == 0 :
            str = "None"
        return True , str
    except Exception as e:
        # If parsing fails, return "None"
        return "None"

# Example usage
input_string = f'<input type="checkbox" id="7a52f2b1-7e21-ee11-9967-000d3af46d37" name="cb_claim">'
result = render_html_or_none(input_string)
print((result))  # Output: This is a test string.

# input_string = "This is not HTML."
# result = render_html_or_none(input_string)
# print(result)  # Output: None
