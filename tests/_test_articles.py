import difflib
import http.client
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN", "")
assert ACCESS_TOKEN

PAGE = os.getenv("QIITA_PAGE", "1")
PAR_PAGE = os.getenv("QIITA_PER_PAGE", "100")

IGNORED_TITLES = []
ignored_titles_str = os.getenv("IGNORED_TITLES", "")
if ignored_titles_str:
    IGNORED_TITLES = [title.strip() for title in ignored_titles_str.split(",")]


def get_qiita_data():
    """Fetch articles from Qiita API"""
    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
    api = f"/api/v2/authenticated_user/items?page={PAGE}&per_page={PAR_PAGE}"
    conn = http.client.HTTPSConnection("qiita.com", 443)
    conn.request("GET", api, headers=headers)
    res = conn.getresponse()
    if res.reason != "OK":
        print(res.status, res.reason)
        conn.close()
        raise Exception("Failed to get data from Qiita")
    data = res.read().decode("utf-8")
    conn.close()
    return json.loads(data)


def check_article_consistency(readme_path, expected_content):
    if not os.path.exists(readme_path):
        return False, f"README.md not found in {readme_path}"

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            actual_content = f.read()

        if actual_content.strip() != expected_content.strip():
            expected_lines = expected_content.strip().splitlines()
            actual_lines = actual_content.strip().splitlines()
            diff = difflib.unified_diff(
                expected_lines,
                actual_lines,
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
            diff_output = "\n".join(diff)
            return (
                False,
                f"Content mismatch in {readme_path}" + "\n" + f"diff:{diff_output}",
            )
        return True, None
    except Exception as e:
        return False, f"Error reading {readme_path}: {str(e)}"


def run_consistency_check():
    """Run the consistency check for all articles"""
    dirname = Path(__file__).parent.parent
    json_data = get_qiita_data()

    inconsistent_articles = []

    for item in json_data:
        created_at = item["created_at"]
        title = item["title"]
        date = created_at[:10].replace("-", "")

        if any(ignored_title in title for ignored_title in IGNORED_TITLES):
            print(f"Skipping {title}")
            continue

        data_dirs = [
            d for d in dirname.iterdir() if d.is_dir() and d.name.startswith(f"{date}_")
        ]
        if len(data_dirs) != 1:
            raise Exception(
                f"Expected exactly one folder starting with '{date}_' for title '{title}'"
            )

        path = os.path.join(data_dirs[0], "README.md")

        is_consistent, error_msg = check_article_consistency(path, item["body"])
        if not is_consistent:
            inconsistent_articles.append(
                {"title": title, "path": path, "error": error_msg}
            )

    if inconsistent_articles:
        print("Inconsistency found in articles:")
        for article in inconsistent_articles:
            print(f"- {article['title']}: {article['error']}")
        return False
    else:
        print("All articles are consistent.")
        return True


def main():
    print("Running article consistency check...")
    try:
        success = run_consistency_check()
        if success:
            print("\n✅ All tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Consistency check failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
