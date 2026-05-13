#!/usr/bin/env python3
"""
submit_server.py — Accepts form POSTs from tv-mount-offer.html and
appends each submission as a new row in the TV Mount Leads Google Sheet.

Run with:
    python3 submit_server.py

Keep this running while the landing page is in use.
"""

import json
import warnings
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

warnings.filterwarnings("ignore")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH   = "/Users/alexawagman/houseaccount/token.json"
SPREADSHEET_ID = "10OolxGTAwX9p91fC4fGtpo98sK3JPIE7AuAVgYbcCM8"
SHEET_RANGE  = "Sheet1!A:G"
PORT         = 5050


def get_sheets_service():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("sheets", "v4", credentials=creds)


def append_row(data: dict):
    service = get_sheets_service()
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("firstName", ""),
        data.get("lastName", ""),
        data.get("moveDate", ""),
        data.get("street", ""),
        data.get("city", ""),
        data.get("state", ""),
    ]
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]},
    ).execute()
    print(f"[{row[0]}] New lead: {row[1]} {row[2]} — {row[5]}, {row[6]}")


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self._cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length)
        try:
            data = json.loads(body)
            append_row(data)
            self._cors()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        except Exception as e:
            print(f"Error: {e}")
            self._cors()
            self.send_response(500)
            self.end_headers()

    def _cors(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, *args):
        pass  # suppress default access logs


if __name__ == "__main__":
    print(f"Submit server running on http://localhost:{PORT}")
    print(f"Writing to: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
    print("Press Ctrl+C to stop.\n")
    HTTPServer(("", PORT), Handler).serve_forever()
