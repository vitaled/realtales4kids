import wikipediaapi

def extract_wikipedia_text(page_title):
    # Initialize the Wikipedia API
    wiki_wiki = wikipediaapi.Wikipedia('Real Tales 4 Kids','it')



    # Get the page
    page = wiki_wiki.page("Luna")

    # Check if the page exists
    if not page.exists():
        return f"The page '{page_title}' does not exist."

    # Extract the text
    return page.text

# Example usage
if __name__ == "__main__":
    page_title = "Python (programming language)"
    text = extract_wikipedia_text(page_title)
    print(text)