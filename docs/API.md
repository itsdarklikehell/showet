# Showet API Documentation

## Overview

The showet HTTP API provides programmatic access to demo functionality. It can be started via:

```bash
showet-api         # Starts API server on port 8765
showet-webui       # Starts API + opens browser
```

## Endpoints

### GET /api/platforms

Returns a list of all supported platform slugs.

**Response:**
```json
{
  "success": true,
  "platforms": ["commodore64", "amigaocsecs", "playstation", ...]
}
```

### GET /api/search?q={query}

Search pouet.net productions by name or keyword.

**Parameters:**
- `q` (required): Search query string

**Response:**
```json
{
  "success": true,
  "results": {
    "12345": {
      "id": "12345",
      "name": "Demo Name",
      "type": "demo",
      "releaseDate": "2024-01-01",
      "voteup": "42"
    }
  }
}
```

### POST /api/run/{pouet_id}

Launch a demo by its pouet.net ID.

**Response:**
```json
{
  "success": true,
  "message": "Demo launched"
}
```

### GET /*

Serves static UI files from `showet-ui/` directory.

## Error Handling

All endpoints return JSON responses with an error structure:

```json
{
  "success": false,
  "error": "Error message description"
}
```

HTTP status codes:
- `200`: Success
- `400`: Bad request (missing parameters, invalid ID)
- `404`: Resource not found
- `500`: Server error

## Integration Examples

### Python
```python
import urllib.request
import json

# List platforms
with urllib.request.urlopen("http://localhost:8765/api/platforms") as r:
    data = json.loads(r.read().decode())
    print(data["platforms"])

# Search demos
with urllib.request.urlopen("http://localhost:8765/api/search?q=c64") as r:
    results = json.loads(r.read().decode())["results"]
```

### JavaScript (Browser)
```javascript
// Search and display results
async function searchDemos(query) {
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    if (data.success) {
        displayResults(data.results);
    }
}
```

### curl
```bash
# List platforms
curl http://localhost:8765/api/platforms | jq .

# Search demos
curl "http://localhost:8765/api/search?q=commodore" | jq .

# Run a demo
curl -X POST http://localhost:8765/api/run/12345
```