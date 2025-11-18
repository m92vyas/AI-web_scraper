# AI Web Scraper
Detailed Readme coming soon.

This repo aims to provide functions for AI web scraping which can be easily used to make Web Search + Extraction/Scraping Agents or Workflow.

Advantage over other available AI scraping library is that it is very good with extracting urls which is critical for many scraping operation, the functions are easy to use and can be easily added to any codebase, it uses the open source webpage to llm ready text convertor [llm-reader](https://github.com/m92vyas/llm-reader) an alternative to firecrawl and jina reader api so reducing costs.
As the code is open source you can use the [llm-reader](https://github.com/m92vyas/llm-reader) to create any web related AI features similar to this repo.

### Install:
```python
pip install git+https://github.com/m92vyas/llm-reader.git git+https://github.com/m92vyas/AI-web_scraper.git
playwright install
playwright install-deps
```

### Import:
```python
from aiwebscraper.web_scrape_functions import extract_from_url, scrape_data_from_web
```

### Select LLM Model:
I have used LiteLLM library to provide support for various API based and local models. So select model name as per their documentation. (I will soon add those details here)
```python
import os
os.environ["OPENAI_API_KEY"] = <open_ai_key>
# os.environ["GEMINI_API_KEY"] = <gemini_key>
model= "openai/gpt-4o-mini"    # "gemini/gemini-1.5-flash"
```
### Note:
No anti-blocking mechanism is available so you may get blocked by some websites. Solution for this will be added.

### Quick Web Data Extraction:
Just give your query and get scraped data from the web. You can also mention any output format in your query. e.g.
```python
what_to_extract="what is the scenario in the coming decade for solar energy investment in india?"
extracted_data = await scrape_data_from_web(what_to_extract , top_n_urls=5, model=model)
print(extracted_data)
```

### Quick Scraping from a Single URL:
Just mention what you want to scrape from the given url with the desired format(optional but better if it is mentioned).
You can pass a single url or a list of urls e.g.
```python
urls="https://www.ikea.com/in/en/cat/corner-sofas-10671/"
what_to_extract = """extract the product name, product link, image link and price for all the products given in the webpage. The format should be:
{
  "1": {
        "Product Name": ,
        "Product Link": ,
        "Image Link": ,
        "Price":
        },
  "2": {
        "Product Name": ,
        ...
        },
}"""
extracted_data = await extract_from_url(urls=urls, what_to_extract=what_to_extract, model=model)
print(extracted_data)
```
