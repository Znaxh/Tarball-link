import re
import streamlit as st
import requests

st.set_page_config(
    page_title="PR Tarball Downloader",
    page_icon="📦",
    layout="centered",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark = st.toggle("🌙 Dark mode", value=st.session_state.dark_mode, key="dark_mode")

LIGHT_CSS = """
<style>
    .stApp {
        max-width: 720px;
        margin: 0 auto;
    }
</style>
"""

DARK_CSS = """
<style>
    .stApp {
        max-width: 720px;
        margin: 0 auto;
        background-color: #0d1117;
        color: #e6edf3;
    }
    header[data-testid="stHeader"] {
        background-color: #0d1117;
    }
    .stTextInput > div > div > input {
        background-color: #161b22;
        color: #e6edf3;
        border-color: #30363d;
    }
    .stMarkdown, .stCaption, p, span, label, .stAlert p {
        color: #e6edf3 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #e6edf3 !important;
    }
    .stCodeBlock {
        background-color: #161b22 !important;
    }
    code {
        color: #e6edf3 !important;
        background-color: #161b22 !important;
    }
    pre {
        background-color: #161b22 !important;
    }
    div[data-testid="stNotification"] {
        background-color: #161b22;
        border-color: #30363d;
    }
    .stButton > button {
        background-color: #238636;
        color: #ffffff;
        border-color: #238636;
    }
    .stButton > button:hover {
        background-color: #2ea043;
        border-color: #2ea043;
    }
    .stLinkButton > a {
        background-color: #238636 !important;
        color: #ffffff !important;
        border-color: #238636 !important;
    }
    .stLinkButton > a:hover {
        background-color: #2ea043 !important;
        border-color: #2ea043 !important;
    }
    div[data-testid="stForm"], div[data-testid="stVerticalBlock"] {
        background-color: transparent;
    }
    footer {
        color: #484f58 !important;
    }
    .stDeployButton {
        color: #e6edf3 !important;
    }
</style>
"""

st.markdown(DARK_CSS if dark else LIGHT_CSS, unsafe_allow_html=True)

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
            st.error(
                "Invalid GitHub PR URL. Expected format: "
                "`https://github.com/owner/repo/pull/123`"
            )
        else:
            owner, repo, pr_number = parsed
            with st.spinner("Fetching PR info from GitHub API..."):
                try:
                    sha = fetch_base_sha(owner, repo, pr_number)
                except requests.HTTPError as exc:
                    st.error(
                        f"GitHub API error: {exc.response.status_code} "
                        f"— {exc.response.reason}"
                    )
                    st.stop()
                except Exception as exc:
                    st.error(f"Something went wrong: {exc}")
                    st.stop()

            tarball_url = (
                f"https://github.com/{owner}/{repo}/archive/{sha}.tar.gz"
            )

            st.success("Tarball link ready!")

            st.code(tarball_url, language=None)

            st.link_button(
                "⬇️  Download Tarball",
                url=tarball_url,
                use_container_width=True,
            )
