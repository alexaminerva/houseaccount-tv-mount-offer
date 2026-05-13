// ── HouseAccount — Google Apps Script ──
// Routes form submissions to the correct Google Sheet based on the `sheet` param.
// Default (no sheet param) → TV Mount sheet
// sheet=leadingre → LeadingRE sheet
//
// TV Mount Sheet ID:   10OolxGTAwX9p91fC4fGtpo98sK3JPIE7AuAVgYbcCM8
// LeadingRE Sheet ID:  1fm1OlrT9ZY23w-oM05ZtX-0kD6ojpr0OUy6ofStyp1o

var SHEETS = {
  'default':   '10OolxGTAwX9p91fC4fGtpo98sK3JPIE7AuAVgYbcCM8',
  'leadingre': '1fm1OlrT9ZY23w-oM05ZtX-0kD6ojpr0OUy6ofStyp1o'
};

function doGet(e) {
  var p = e.parameter;
  var sheetId = SHEETS[p.sheet] || SHEETS['default'];

  if (p.type === 'broker_signup') {
    writeBrokerSignup(p, sheetId);
  } else {
    writeHomeownerSignup(p, sheetId);
  }

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ── Homeowner sign-ups ──────────────────────────────────────────────────────
function writeHomeownerSignup(p, sheetId) {
  var sheet = getOrCreateSheet(sheetId, 'Homeowner Signups', [
    'Timestamp', 'First Name', 'Last Name', 'Email', 'Phone',
    'Move Date', 'Street', 'City', 'State', 'Zip', 'Source'
  ]);
  sheet.appendRow([
    new Date(),
    p['first-name'] || '', p['last-name'] || '', p['email'] || '',
    p['phone'] || '', p['move-date'] || '', p['to-street'] || '',
    p['to-city'] || '', p['to-state'] || '', p['to-zip'] || '',
    p['source'] || ''
  ]);
}

// ── Broker / Agent popup sign-ups ───────────────────────────────────────────
function writeBrokerSignup(p, sheetId) {
  // LeadingRE sheet uses "Agent Signups"; TV Mount sheet uses "Broker Signups"
  var tabName = (sheetId === SHEETS['leadingre']) ? 'Agent Signups' : 'Broker Signups';
  var sheet = getOrCreateSheet(sheetId, tabName, [
    'Timestamp', 'Name', 'Email', 'Brokerage', 'Phone', 'Source'
  ]);
  sheet.appendRow([
    new Date(),
    p['name'] || '', p['email'] || '', p['brokerage'] || '',
    p['phone'] || '', p['source'] || ''
  ]);
}

// ── Helper: get tab by name, or create it with a header row ────────────────
function getOrCreateSheet(sheetId, name, headers) {
  var ss = SpreadsheetApp.openById(sheetId);
  var sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
  }
  return sheet;
}
