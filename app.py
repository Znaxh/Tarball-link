import re
import streamlit as st
import requests

st.set_page_config(
    page_title="PR Tarball Downloader",
    page_icon="📦",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        max-width: 720px;
        margin: 0 auto;
    }
    .tar-url-box {
        background: #f0f2f6;
        border: 1px solid #d0d3da;
        border-radius: 8px;
        padding: 14px 18px;
        font-family: monospace;
        font-size: 14px;
        word-break: break-all;
        margin: 12px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PR_URL_PATTERN = re.compile(
    r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)"
)


def parse_pr_url(url: str):
    m = PR_URL_PATTERN.match(url.strip())
    if not m:
        return None
    return m.group("owner"), m.group("repo"), m.group("number")


def fetch_base_sha(owner: str, repo: str, pr_number: str) -> str:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    resp = requests.get(api_url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data["base"]["sha"]


st.title("📦 PR Tarball Downloader")
st.caption("Paste a GitHub pull request URL and get the base-branch tarball link.")

pr_url = st.text_input(
    "GitHub PR URL",
    placeholder="https://github.com/owner/repo/pull/123",
)

if st.button("Get Tarball", type="primary", use_container_width=True):
    if not pr_url:
        st.warning("Please enter a PR URL first.")
    else:
        parsed = parse_pr_url(pr_url)
        if parsed is None:
            st.error("Invalid GitHub PR URL. Expected format: `https://github.com/owner/repo/pull/123`")
        else:
            owner, repo, pr_number = parsed
            with st.spinner("Fetching PR info from GitHub API..."):
                try:
                    sha = fetch_base_sha(owner, repo, pr_number)
                except requests.HTTPError as exc:
                    st.error(f"GitHub API error: {exc.response.status_code} — {exc.response.reason}")
                    st.stop()
                except Exception as exc:
                    st.error(f"Something went wrong: {exc}")
                    st.stop()

            tarball_url = f"https://github.com/{owner}/{repo}/archive/{sha}.tar.gz"

            st.success("Tarball link ready!")

            st.code(tarball_url, language=None)

            st.link_button(
                "⬇️  Download Tarball",
                url=tarball_url,
                use_container_width=True,
            )
