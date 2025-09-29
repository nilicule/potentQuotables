import re
import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def fetch_signatures_content():
    """Fetch signatures content from remote URL."""
    signatures_url = os.getenv('SIGNATURES_URL')
    if not signatures_url:
        raise ValueError("SIGNATURES_URL environment variable is required")

    try:
        response = requests.get(signatures_url, timeout=30)
        response.raise_for_status()
        # Try to decode with different encodings
        try:
            content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            content = response.content.decode('iso-8859-1')
        return content
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch signatures from {signatures_url}: {e}")

def parse_signatures():
    """Parse signatures from remote URL, handling multi-line signatures."""
    content = fetch_signatures_content()

    # Split by lines starting with '%'
    sections = re.split(r'\n%\n', content)
    signatures = []

    for section in sections:
        section = section.strip()
        if not section or section == '%':
            continue

        # Handle signatures that may span multiple lines
        lines = section.split('\n')

        # Find attribution lines (starting with '--')
        attribution_lines = []
        quote_lines = []

        # Track if we found empty lines (intentional breaks)
        processed_lines = []
        current_quote_part = []

        for line in lines:
            stripped_line = line.strip()

            if stripped_line.startswith('-- '):
                # If we have accumulated quote parts, join them and add to processed
                if current_quote_part:
                    processed_lines.append(' '.join(current_quote_part))
                    current_quote_part = []
                attribution_lines.append(stripped_line)
            elif stripped_line == '':
                # Empty line - if we have quote parts, join them and start new part
                if current_quote_part:
                    processed_lines.append(' '.join(current_quote_part))
                    processed_lines.append('')  # Preserve the empty line
                    current_quote_part = []
            elif stripped_line:
                current_quote_part.append(stripped_line)
                quote_lines.append(stripped_line)

        # Handle any remaining quote parts
        if current_quote_part:
            processed_lines.append(' '.join(current_quote_part))

        # Join quote lines into a single line for display
        quote = ' '.join(quote_lines).strip()
        attribution = '\n'.join(attribution_lines) if attribution_lines else ""

        # Create full text preserving structure
        full_text_parts = []
        if processed_lines:
            full_text_parts.extend(processed_lines)
        if attribution_lines:
            full_text_parts.extend(attribution_lines)

        full_text = '\n'.join(full_text_parts)

        # Filter out the width indicator line
        if quote and not quote.startswith('<-') and '--->' not in quote:
            signatures.append({
                'quote': quote,
                'attribution': attribution,
                'full_text': full_text
            })

    return signatures

@app.route('/')
def index():
    signatures = parse_signatures()
    return render_template('index.html', signatures=signatures)

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    signatures = parse_signatures()

    if query:
        filtered_signatures = []
        for sig in signatures:
            if (query in sig['quote'].lower() or
                query in sig['attribution'].lower()):
                filtered_signatures.append(sig)
        signatures = filtered_signatures

    return jsonify(signatures)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    app.run(debug=debug, host=host, port=port)