# Potent Quotables

A web interface for browsing and searching memorable quotes and signatures.

## Features

- Browse all signatures from `signatures.txt`
- Real-time search functionality
- Copy quotes to clipboard with a single click
- Responsive design for mobile and desktop
- Clean, modern interface

## Configuration

The application uses environment variables for configuration. Create a `.env` file (copy from `.env.example`) to customize settings:

```bash
PORT=5001                                    # Port to run the application on
HOST=0.0.0.0                               # Host to bind to (0.0.0.0 for all interfaces)
DEBUG=true                                 # Enable debug mode (true/false)
SIGNATURES_URL=https://example.com/signatures.txt  # URL to fetch signatures from (REQUIRED)
```

**Important**: The `SIGNATURES_URL` environment variable is required. The application fetches signatures from this remote URL instead of using a local file.

## Running Locally

### With UV (recommended for development)

```bash
# Install dependencies
uv sync

# Run the application
uv run python app.py
```

### With pip

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5001` (or the port specified in .env)

## Running with Docker

### Build the image

```bash
docker build -t potent-quotables .
```

### Run the container

```bash
docker run -p 5001:5001 potent-quotables
```

The application will be available at `http://localhost:5001`

## Signatures File Format

The application fetches signatures from a remote URL. The file should be in the following format:

- Signatures are separated by lines starting with `%`
- Multi-line signatures are supported
- Attribution lines start with `-- ` and appear on separate lines
- All text is preserved as-is for copying
- File encoding: UTF-8 or ISO-8859-1

## Development

This project uses:
- Python 3.13+
- Flask for the web framework
- Requests for HTTP fetching
- UV for package management
- Docker for containerization

## Remote URL Setup

To use this application, you need to:

1. Host your signatures file at a publicly accessible URL
2. Set the `SIGNATURES_URL` environment variable to point to that URL
3. The application will fetch and parse the signatures from the remote location

Example URLs:
- GitHub raw file: `https://raw.githubusercontent.com/user/repo/main/signatures.txt`
- Any web server: `https://yourdomain.com/path/to/signatures.txt`