#!/usr/bin/env python3
"""Create HouseAccount TV Mount Campaign Summary Google Doc."""

import warnings
warnings.filterwarnings("ignore")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = "/Users/alexawagman/houseaccount/token.json"

def get_creds():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

def create_doc():
    creds = get_creds()
    service = build("docs", "v1", credentials=creds)

    doc = service.documents().create(body={"title": "HouseAccount TV Mount Campaign — Summary"}).execute()
    doc_id = doc["documentId"]

    # Build content as a list of (text, style) tuples
    # style: 'h1', 'h2', 'h3', 'normal', 'bold_normal'
    sections = [
        ("HouseAccount TV Mount Campaign — Summary\n", "h1"),
        ("\n", "normal"),

        ("What Was Built\n", "h2"),
        ("Two landing pages hosted on Netlify at https://houseaccount-freetvmount.netlify.app/\n", "normal"),
        ("\n", "normal"),

        ("1. Homeowner Sign-Up Page\n", "h3"),
        ("URL: https://houseaccount-freetvmount.netlify.app/\n\n", "normal"),
        ("The page a real estate agent shares with their new homeowner client after closing. It explains the free TV mount offer and collects their information.\n\n", "normal"),
        ("Sections:\n", "bold"),
        ("Hero with offer card (Buy 1 TV Mount, Get 1 Free)\nWhat is HouseAccount (2-column explainer)\nTrust strip (brokerage logos)\nHow It Works (3 steps)\nServices tiles: TV Mounting, Pool Maintenance, Move-In Clean, Lock Change, Fixture Installation, Mirror & Art Hanging\nHouseAccount Protected section\nSign-up form\nFooter\n\n", "normal"),
        ("Form fields collected:\n", "bold"),
        ("First name, Last name, Email, Phone (all required)\nEstimated move date (optional)\nStreet, City, State, Zip (all required)\n\n", "normal"),

        ("2. Agent Share Page\n", "h3"),
        ("URL: https://houseaccount-freetvmount.netlify.app/agent-share\n\n", "normal"),
        ("The page for real estate agents. Explains the offer, gives them a copy link and QR code to share with clients, and shows how-to-share steps.\n\n", "normal"),
        ("Features:\n", "bold"),
        ("Offer summary tiles (4 across)\nCopy link button (copies homeowner URL to clipboard)\nQR code (links to homeowner page)\nHow-to-share steps\nTrusted by brokerage logos: Compass, Keller Williams, Side, Corcoran, Sotheby's\n\n", "normal"),

        ("How Form Submissions Work\n", "h2"),
        ("1. Homeowner fills out the form and clicks Unlock My Free TV Mount\n2. The page sends the data to a Google Apps Script web app\n3. Apps Script appends a new row to the Google Sheet instantly\n4. The homeowner sees a success confirmation on the page\n\n", "normal"),
        ("Google Sheet: ", "bold"),
        ("https://docs.google.com/spreadsheets/d/10OolxGTAwX9p91fC4fGtpo98sK3JPIE7AuAVgYbcCM8\n\n", "normal"),
        ("Columns in the sheet:\n", "bold"),
        ("Timestamp | First Name | Last Name | Email | Phone | Move Date | Street | City | State | Zip\n\n", "normal"),

        ("LinkedIn Outreach Campaign (Expandi.io)\n", "h2"),
        ("Target: Real estate brokers and agents in Texas\n\n", "normal"),

        ("Campaign Flow\n", "h3"),
        ("Start → Visit Profile (immediately)\n↓\nAlready connected?\n\nYES path:\n  → Message 1 (wait 3 days)\n  → Message 2 (wait 10 days)\n  → End\n\nNO path:\n  → Send Connection Request (wait 1 day)\n  → Did they connect?\n      YES → Message 1 (wait 5 days) → Message 2 (wait 4 days) → Message 3 (wait 10 days)\n      NO  → End\n\n", "normal"),

        ("Messages\n", "h3"),

        ("Connection Request (under 300 characters)\n", "bold"),
        ("Hi {{firstName}} — I work with agents in Texas on closing gifts for new homeowners. Think you'd find this useful. Would love to connect.\n\n", "normal"),

        ("Already Connected — Message 1 (3 days after visit)\n", "bold"),
        ("Hey {{firstName}} — wanted to share something we're doing for agents in Texas right now.\n\nHouseAccount is giving new homeowners a free professional TV mount installation as a closing gift — no cost to you, just a link you send them after closing.\n\nHere's the agent page: https://houseaccount-freetvmount.netlify.app/agent-share\n\nHappy to answer any questions if you want to know more.\n\n", "normal"),

        ("Already Connected — Message 2 (10 days later)\n", "bold"),
        ("Just wanted to bump this up in case it got buried {{firstName}}. A few agents in your market have already started sharing it with clients — takes about 30 seconds to set up. Link is here if you want to take a look: https://houseaccount-freetvmount.netlify.app/agent-share\n\n", "normal"),

        ("Post-Connect Message 1 (5 days after connecting)\n", "bold"),
        ("Hey {{firstName}} — glad to be connected. Wanted to share something we're doing for agents right now.\n\nHouseAccount is offering new homeowners a free TV mount installation as a closing gift from their agent. No cost to you — you just send them a link after closing.\n\nAgent page is here: https://houseaccount-freetvmount.netlify.app/agent-share\n\nLet me know if you have questions!\n\n", "normal"),

        ("Post-Connect Message 2 (4 days later)\n", "bold"),
        ("Did you get a chance to look at the TV mount offer {{firstName}}? A lot of agents love it because it's a tangible gift their clients actually use — and it opens the door to HouseAccount's full home services platform for things like pool maintenance, lock changes, and move-in cleaning. Just a nice way to stay top of mind post-close.\n\n", "normal"),

        ("Post-Connect Message 3 (10 days later)\n", "bold"),
        ("Last follow up on this {{firstName}} — if the timing isn't right or it's not a fit, totally understand. But if you ever work with buyers moving into a new home in Texas and want a simple closing gift to send, the link is here: https://houseaccount-freetvmount.netlify.app/agent-share. No strings attached.\n\n", "normal"),

        ("Where to Find Results\n", "h2"),
        ("Homeowner sign-ups: https://docs.google.com/spreadsheets/d/10OolxGTAwX9p91fC4fGtpo98sK3JPIE7AuAVgYbcCM8\n", "normal"),
        ("Agent share page: https://houseaccount-freetvmount.netlify.app/agent-share\n", "normal"),
        ("Homeowner page: https://houseaccount-freetvmount.netlify.app/\n", "normal"),
        ("LinkedIn campaign: Expandi.io dashboard\n", "normal"),
        ("Site management: Netlify — houseaccount-freetvmount\n", "normal"),
    ]

    # Insert all text first (in reverse so indices stay valid, or just build one big insert)
    full_text = "".join(t for t, _ in sections)

    insert_requests = [{"insertText": {"location": {"index": 1}, "text": full_text}}]
    service.documents().batchUpdate(documentId=doc_id, body={"requests": insert_requests}).execute()

    # Now apply formatting — walk through sections tracking index
    format_requests = []
    index = 1  # Docs start at index 1

    HEADING_STYLES = {"h1": "HEADING_1", "h2": "HEADING_2", "h3": "HEADING_3"}

    for text, style in sections:
        length = len(text)
        end = index + length

        if style in HEADING_STYLES:
            format_requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": index, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": HEADING_STYLES[style]},
                    "fields": "namedStyleType"
                }
            })
        elif style == "bold":
            format_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": index, "endIndex": end},
                    "textStyle": {"bold": True},
                    "fields": "bold"
                }
            })

        index = end

    if format_requests:
        service.documents().batchUpdate(documentId=doc_id, body={"requests": format_requests}).execute()

    return f"https://docs.google.com/document/d/{doc_id}"

if __name__ == "__main__":
    url = create_doc()
    print(url)
