from setuptools import setup,find_packages

setup(
    name               = 'AI-web_scraper'
    , version          = '1'
    , license          = 'MIT License'
    , author           = "Maharishi Vyas"
    , author_email     = 'maharishi92vyas@gmail.com'
    , packages         = find_packages('src')
    , package_dir      = {'': 'src'}
    , url              = 'https://github.com/m92vyas/AI-web_scraper.git'
    , keywords         = 'AI Web Scraping'
    , install_requires = [
                            'google',
                            'litellm',
                            # 'git+https://github.com/m92vyas/llm-reader.git',
                         ]
    , include_package_data=True
)