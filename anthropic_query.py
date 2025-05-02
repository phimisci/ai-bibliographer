SYSTEM_PROMPT = """You are tasked with converting a bibliographical reference 
                  into a BibTeX entry. BibTeX is a reference management software 
                  for formatting lists of references, commonly used with LaTeX 
                  documents. Your goal is to accurately transform the given 
                  reference into a properly formatted BibTeX entry.\n\nTo 
                  complete this task, follow these steps:\n\n1. Identify the key 
                  components in the reference. These typically include:\n   
                  - Authors\n   
                  - Title\n   
                  - Publication year\n   
                  - Journal or book title (if applicable)\n   
                  - Editors (for chapters in edited volumes)\n   
                  - Volume and issue numbers (for journal articles)\n   
                  - Page numbers\n   
                  - Publisher (for books)\n   
                  - DOI or URL (if available)\n\n2. 
                  Determine the appropriate BibTeX entry type. Common types 
                  include:\n   
                  - @article: For journal articles\n   
                  - @book: For books\n   
                  - @incollection: For chapters in edited volumes\n   
                  - @techreport: For technical reports\n   
                  - @phdthesis: For PhD theses\n\n3. 
                  Create the BibTeX entry using the following format:\n   
                  @entrytype{citekey,\n     
                  field1 = {value1},\n     
                  field2 = {value2},\n     
                  ...\n   
                  }\n\n   
                  Where:\n   
                  - entrytype is one of the types mentioned above\n   
                  - citekey is a unique identifier for the reference 
                  (typically the first author's last name and the year)\n   
                  - field1, field2, etc. are BibTeX fields like author, title, 
                  year, journal, etc.\n   
                  - value1, value2, etc. are the corresponding values for each 
                  field\n\n4. 
                  Format the entry correctly:\n   
                  - Enclose all field values in curly braces {}\n   
                  - Use extra curly braces {} for acronyms and proper names in
                    titles to preserve capitalization\n   
                  - Separate multiple authors with \" and \"\n\n5. 
                  Include all relevant information from the original reference 
                  in appropriate BibTeX fields.\n\nHere's an example of a 
                  properly formatted BibTeX entry for a journal article:\n\n
                  @article{smith2020example,\n  
                  author = {Smith, John and Doe, Jane},\n  
                  title = {An Example of a {BibTeX} Entry},\n  
                  journal = {Journal of Examples},\n  
                  year = {2020},\n  
                  volume = {5},\n  
                  number = {2},\n  
                  pages = {123--145},\n  
                  doi = {10.1234/example.doi}\n}\n\n
                  Now, convert the given references into BibTeX entries. 
                  Provide only the converted items as response."""

def return_claude_response(*, client, references, model, 
                           system_promt = SYSTEM_PROMPT):
    message_content = f"""Here is the bibliographical reference you need to 
                          convert:\n\n<reference>\n{references}\n</reference>"""

    return client.messages.create(
        model=model,
        max_tokens=20000,
        temperature=1,
        system=system_promt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message_content
                    }
                ]
            }
        ]
    )


def check_claude_response(response):
    if response.stop_reason == "end_turn":
        return True
    if response.stop_reason == "max_tokens":
        raise Exception("Too many tokens.")