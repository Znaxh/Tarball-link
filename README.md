# 📦 PR Tarball Downloader

A simple Streamlit app that converts a **GitHub Pull Request URL** into a downloadable **tarball (.tar.gz) link** for the PR's base branch at that point in time.

## How It Works

1. You paste a GitHub PR link, e.g. `https://github.com/elastic/elasticsearch/pull/139693`
2. The app calls the GitHub API to fetch PR metadata
3. It extracts the `base.sha` (the commit SHA the PR targets)
4. It builds the tarball URL: `https://github.com/{owner}/{repo}/archive/{sha}.tar.gz`

You can then **copy** the link or **download** the tarball directly.

## Features

- Parses any public GitHub PR URL
- One-click copy via the built-in code block copy button
- Direct download button for the `.tar.gz` file
- Dark mode toggle

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open at [http://localhost:8501](http://localhost:8501).

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New app**, select the repo, and set the main file to `app.py`
4. Hit **Deploy**

## Project Structure

```
.
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── README.md
└── .streamlit/
    └── config.toml         # Streamlit server config
```

## Limitations

- Only works with **public** GitHub repositories (the GitHub API is called without authentication)
- Subject to GitHub's unauthenticated API rate limit (~60 requests/hour per IP)

## License

MIT
