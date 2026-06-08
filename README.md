# Norway Job Market

This is an interactive data dashboard built with Python and Streamlit that takes the live job listing from NAV.no and visualizes market trends, such as top cities, employers, job categories, and posting frequency.

My name is [Bita Panahi](https://linkedin.com/in/bita-panahi-1994-) and I am a PhD researcher in Computer Science, NTNU, Norway.


## What the dashboard shows
- Top 15 cities by number of active job listings.
- Job category breakdown to make the job search easier.
- Top 15 hiring employers in Norway.
- Daily posting trend over the last 30 days.
- Table for searching and filtering all active listings with city and category filters.


## What I used
- `Python` -- core programming language
- `requests` -- obtain live data from NAV API
- `pandas` -- data cleaning and transformation
- `Plotly` -- interactive charts
- `Streamlit` -- web dashboard


## Project structure
```
norway_job_market/
|-- app.py                      # Streamlit dashboard app
|-- Norway_Job.ipynb            # Main script
|-- requirements.txt            # Dependencies
|-- README.md              
|-- norway_jobs_summary.csv     # One example of the results

```


## Run locally

### Clone the repository
```bash
git clone https://github.com/Bita-Panahi/Norway_Job_Market.git
cd Norway_Job_Market
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Get fresh data
Open `Norway_Job.ipynb` in VS Code (or Jupyter) and run all cells.
This calls the NAV API and saves `norway_jobs_summary.csv`.

### Launch the dashboard
```bash
streamlit run app.py
```
> **Windows tip:** If `streamlit` is not recognised as a command, use:
> ```bash
> python -m streamlit run app.py
> ```


## Data source
Live data from **NAV Arbeidsplassen** via the [pam-stilling-feed API](https://navikt.github.io/pam-stilling-feed/).
Free to use, no API key or registration required.


## Skills I learned from this project
- REST API integration with `requests`
- Data cleaning and transformation with `pandas`
- Interactive data visualization with `Plotly`
- Dashboard with `Streamlit`
- Data analysis in Jupyter Notebook
- End-to-end data pipeline: API-- transform-- visualize
