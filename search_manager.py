from search import WebSearcher
from termcolor import colored
class SearchManager:
    def __init__(self, model_qa):
        self.model_qa = model_qa

    def fetch_code_reference(self, query):
        search = WebSearcher(self.model_qa)
        search_results = search.fetch_search_results(query)
        
        if not search_results:
            print(colored("No search results found; skipping reference fetching.", 'red'))
            return {}
        
        best_page = search.get_search_page(search_results, query)
        
        if not best_page:
            print(colored("No valid search page found; skipping reference fetching.", 'red'))
            return {}

        results_dict = search.scrape_website_content(best_page)

        if self.verbose:
            print(colored(f"SEARCH RESULTS {search_results}", 'yellow'))
            print(colored(f"RESULTS DICT {results_dict}", 'yellow'))

        return results_dict

