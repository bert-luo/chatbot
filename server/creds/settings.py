import git
import os

def get_git_root():
    git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root

ROOT = get_git_root()

ASTRA_DB_SECURE_BUNDLE_PATH = ROOT + "/server/creds/secure-connect-web-vectors.zip" 
ASTRA_DB_TOKEN_JSON_PATH = ROOT + "chatbot/server/creds/astra-token.json" 
ASTRA_DB_KEYSPACE = "search" 

METAPHOR_API_KEY = "7d3b0f92-903b-412c-905d-30c347c9b03f"

OPENAI_API_KEY = "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" # TODO: Change
