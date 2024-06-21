from pathlib import Path

import google_auth_oauthlib.flow

CLIENT_SECRET_FILE = Path(__file__).resolve().parent / "client_secret.json"

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    CLIENT_SECRET_FILE,
    scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"],
)

flow.redirect_uri = "http://localhost:8000"

authorization_url, state = flow.authorization_url(
    access_type="offline",
    include_granted_scopes="true",
    prompt="consent",
)
