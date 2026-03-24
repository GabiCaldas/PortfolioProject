# Portfolio Project

A collection of data analysis, data engineering, and automation projects demonstrating skills in SQL, Python, ETL pipelines, and web scraping.

## Projects

### Covid 19 Data Exploration
SQL-based exploration of Covid-19 datasets, covering infection rates, death rates, and vaccination trends across countries and continents.

**Tech Stack:** SQL (MS SQL Server / SSMS)

### Nashville Housing Data Cleaning
SQL scripts to clean and standardize raw Nashville housing data — handling nulls, duplicate records, and inconsistent formatting.

**Tech Stack:** SQL (MS SQL Server / SSMS)

### Movie Correlation Project
Jupyter Notebook analyzing correlations between movie attributes (budget, gross revenue, ratings, etc.) using Python data science libraries.

**Tech Stack:** Python, Pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebook

### Application Data Cleaning Script
Python script that reads member application data from Excel, applies cleaning transformations, and exports organized output to a dated folder structure.

**Tech Stack:** Python, Pandas, NumPy, openpyxl

### Health Provider Data Scraper & ETL
Headless browser scraper that collects provider listings from a public health directory and loads them into a SQL database.

**Tech Stack:** Python, Selenium, Pandas, SQLAlchemy

### Movie Reviews ETL (NYT API)
Apache Airflow DAG that extracts movie review data from the New York Times Article Search API, transforms it, and loads it to AWS S3.

**Tech Stack:** Python, Apache Airflow, Pandas, NYT API, AWS S3 (s3fs)

## Running Locally

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/GabiCaldas/PortfolioProject.git
   cd PortfolioProject
   ```

2. Install Python dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn sqlalchemy selenium openpyxl xlsxwriter requests s3fs apache-airflow
   ```

3. For the **NYT Movie Reviews ETL**, create a `config.json` file inside `movie_reviews_etl/` (the script reads it from the working directory):
   ```json
   {
     "NYT_API_KEY": "your_api_key_here"
   }
   ```

4. For the **Health Provider Scraper**, ensure Google Chrome and a matching [ChromeDriver](https://chromedriver.chromium.org/downloads) are installed and available on your PATH.

### Running Individual Projects

- **SQL projects** — open the `.sql` files in your preferred SQL client (e.g., SSMS, DBeaver) and execute against your database.
- **Movie Correlation Project** — launch Jupyter and open `Movie Correlation Project.ipynb`.
- **Application Data Cleaning Script** — update the file path in the script and run `python "Application Data Cleaning Script.py"`.
- **Health Provider Scraper** — run `python "Health Provider Data Scraper & ETL"`.
- **NYT Movie Reviews ETL** — deploy `movie_reviews_etl/` to an Airflow environment and trigger the `nytimes_dag` DAG.
