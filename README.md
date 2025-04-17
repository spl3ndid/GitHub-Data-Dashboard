# GitHub Data Dashboard

A data visualization dashboard for analyzing GitHub repositories. This tool provides insights into repository metrics, contributor trends, commit activity, programming language usage, and more.

🚀 **Live Demo**: [GitHub Data Dashboard](https://web-production-e2a2f.up.railway.app/)

---

## Features

- **Repository Metrics**: View stars, forks, and open issues.
- **Contributor Analysis**: Identify top contributors and their activity.
- **Commit Frequency**: Visualize commit trends over time.
- **Programming Language Distribution**: Analyze the languages used in the repository.
- **Issue Analysis**: Track issue status, closing times, and trends.
- **Pull Request Metrics**: Understand pull request activity and contributors.
- **Comparative Analysis**: Compare issues and pull requests over time.
- **Date Range Filtering**: Filter data by custom date ranges.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/github-data-dashboard.git
cd github-data-dashboard
```

### 2. Install Dependencies
Ensure you have Python installed. Then, install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the Streamlit app:
```bash
streamlit run app.py
```

Access the dashboard in your browser at [http://localhost:8501](http://localhost:8501).

---

## GitHub API Authentication

To avoid hitting GitHub's API rate limits, you can use a personal access token:

1. Go to **GitHub → Settings → Developer settings → Personal access tokens**.
2. Generate a new token with the `repo` scope.
3. Copy the token and paste it into the dashboard's sidebar under "GitHub Personal Access Token".

- Without a token: **60 requests/hour**
- With a token: **5,000 requests/hour**

---

## Technologies Used

- **Python**: Core programming language.
- **Streamlit**: Interactive web application framework.
- **Plotly**: Data visualization library for charts and graphs.
- **Pandas**: Data manipulation and analysis.
- **GitHub API**: Fetch repository data.

---

## Project Structure

```
GitHub-Data-Dashboard/
├── app.py                     # Main application file
├── components/                # UI components for different analyses
│   ├── __init__.py
│   ├── commits.py             # Commit analysis
│   ├── contributors.py        # Contributor analysis
│   ├── issues.py              # Issue analysis
│   ├── languages.py           # Language distribution
│   ├── pulls.py               # Pull request analysis
│   ├── repository_info.py     # Repository metrics
│   ├── sidebar.py             # Sidebar UI
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── data_processing.py     # Data filtering and transformation
│   ├── github_api.py          # GitHub API interaction
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── LICENSE                    # License information
└── .gitignore                 # Git ignore rules
```

---

## Example Usage

1. **Select a Repository**: Enter a GitHub username/organization or repository URL in the sidebar.
2. **Filter by Date**: Choose a start and end date for the analysis.
3. **Explore Metrics**: View visualizations for contributors, commits, issues, pull requests, and more.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

**GitHub Data Dashboard** | Built with ❤️ using Streamlit