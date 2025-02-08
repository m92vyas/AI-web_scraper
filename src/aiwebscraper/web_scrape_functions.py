from url_to_llm_text.get_html_text import get_page_source
from url_to_llm_text.get_llm_input_text import get_processed_text
from litellm import acompletion, token_counter
import asyncio, json, os
from aiwebscraper.web_search_functions import get_search_query, default_search_and_get_urls


def filter_till_token_limit(model, messages, input_tokens_allowed):
  input_tokens = token_counter(model=model, messages=messages)
  if input_tokens>input_tokens_allowed:
    prompt = messages[0].get('content','')
    len_prompt = len(prompt)
    for i in range(5,95,5):
      input_tokens = token_counter(model=model, messages=[{'content':prompt[:int(len_prompt*(100-i)/100)]}])
      if input_tokens<input_tokens_allowed:
        messages[0]['content'] = prompt[:int(len_prompt*(100-i)/100)]
        return messages
      else:
        continue
  else:
    return messages
  

async def default_get_page_source(url, wait=5):
  page_source = await get_page_source(url, wait=wait)
  return page_source


html_to_markdown_params={}
async def default_get_llm_text(page_source, url, **html_to_markdown_params):
  llm_text = await get_processed_text(page_source, url)
  return llm_text


async def extract_data_using_llm(what_to_extract, llm_ready_text, model=model, input_tokens_allowed=100000, verbose=True):

  prompt_text = """Below I have given you one webpage. Your work is to extract data from the webpage as per the user query.
  If the user has not mentioned any output format then extract the data in an appropriate readable and clear format.
  
  User Query:
  {what_to_extract}
  
  Webpage:
  {llm_ready_text}
  """ 
  messages = [{"role": "user", "content": [{"type": "text", "text": prompt_text.format(what_to_extract=what_to_extract, llm_ready_text=llm_ready_text)}]}]
  messages = filter_till_token_limit(model, messages, input_tokens_allowed)

  try:
    response = await acompletion(model=model, messages=messages, temperature=0, top_p=0.001)
    usage = response.usage
    print('$$$ Tokens Usage for extracting data using llm: ',usage) if verbose else None
    llm_extraction = response.choices[0].message.content
    return llm_extraction
  except Exception as e:
    return {'Error':e}
  

async def scrape_single_url(url, what_to_extract, page_source_func='default_get_page_source', llm_text_func='default_get_llm_text', model=model, input_tokens_allowed=100000, html_to_markdown_params={}, verbose=True):

  page_source = await globals()[page_source_func](url)
  if page_source == '':
    print(f"***Not able to fetch {url}: either you got blocked or some internal error.***") if verbose else None
    return ''
  else:
    llm_text = await globals()[llm_text_func](page_source, url, **html_to_markdown_params)
  
  if llm_text == '' or len(llm_text)<100:
    print(f"***Not able to extract from {url}: Some internal error.***") if verbose else None
    return ''
  else:
    scraped_data = await extract_data_using_llm(what_to_extract, llm_text, model=model, input_tokens_allowed=input_tokens_allowed)
    if type(scraped_data)==dict and scraped_data.get('Error','') != '':
      print(f"***Not able to extract from {url}: Error while using LLM. Error Message: scraped_data.get('Error','') ***") if verbose else None
      return ''
    else:
      print(f"---Data extracted from url: {url} --") if verbose else None
      scraped_data = json.dumps({"url": url, "extraction":scraped_data})
      return scraped_data
    
async def extract_from_url(urls, what_to_extract, page_source_func='default_get_page_source', llm_text_func='default_get_llm_text', model=model, input_tokens_allowed=100000, verbose=True):
  
  if type(urls) == str:
    urls = [urls]
  
  try:
    tasks = []
    for url in urls:
      tasks.append(asyncio.create_task(scrape_single_url(url, what_to_extract, page_source_func=page_source_func, llm_text_func=llm_text_func, model=model, input_tokens_allowed=input_tokens_allowed, verbose=True)))
    responses = await asyncio.gather(*tasks)
    return responses
  except Exception as e:
    print('***Error while extracting data from urls: ',e)
    return []
  
web_search_params={}
html_to_markdown_params={}

async def scrape_data_from_web(what_to_extract, top_n_urls, model=model, web_search_function_name='default_search_and_get_urls',
                               page_source_func='default_get_page_source', llm_text_func='default_get_llm_text',
                               input_tokens_allowed=100000, web_search_params={}, html_to_markdown_params={}, 
                               verbose=True):

  query = await get_search_query(what_to_extract, model)
  if type(query)==dict and query.get('Error','') != '':
    query = what_to_extract
  urls = await globals()[web_search_function_name](query, top_n_urls, web_search_params)

  if urls == []:
    return {"Error":"Web search failed to fetch urls."}

  responses = await extract_from_url(urls, what_to_extract, page_source_func=page_source_func, llm_text_func=llm_text_func, model=model, input_tokens_allowed=input_tokens_allowed, verbose=verbose)
  return responses