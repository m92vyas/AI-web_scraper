from litellm import acompletion, token_counter
import json, os
from googlesearch import search

async def get_search_query(what_to_extract, model=model, verbose=True):

  prompt_text = f"""Below i have given you one user requirement for web scraping. You have to provide a google search query for the given user requirement so that we can get relevant urls.
  Make sure the web search query has all the relevant keywords, mention of place/country(if any given) so that we are able to get right webpages from the query.
  Give output as a one line sentence only.

  User Requirement:
  {what_to_extract}
  """

  messages = [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]

  try:
    response = await acompletion(model=model, messages=messages, temperature=0, top_p=0.001)
    usage = response.usage
    print('$$$ Tokens Usage for getting web search query: ',usage) if verbose else None
    search_query = response.choices[0].message.content # response.json()['choices'][0]['message']['content']
    return search_query
  except Exception as e:
    return {'Error':e}
  

web_search_params = {}
async def default_search_and_get_urls(query, top_n_urls= 5, web_search_params={}, verbose=True):
  try:
    print("---started web search (google search)---") if verbose else None
    search_params_default = {'pause':3, 'ignore_url': ['.pdf']}
    search_params_updated = search_params_default | web_search_params
    ignore_url = search_params_updated.get('ignore_url',[])
    search_params_updated.pop('ignore_url',None)
    urls = search(query, stop = top_n_urls+10, **search_params_updated)
    url_list = []
    for url in urls:
      if any(ignore in url for ignore in ignore_url):
        continue
      else:
        url_list.append(url)
    return url_list[:top_n_urls]
  except Exception as e:
    print('Error while fetching urls: ',e)
    return []