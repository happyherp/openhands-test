from common import select_and_load_json, COST_PER_CACHE_WRITE_TOKEN, COST_PER_CACHE_READ_TOKEN, COST_PER_COMPLETION_TOKEN
from process_events import process_events  # Import the function
import webbrowser
import os
from datetime import datetime, timedelta
from collections import defaultdict

def generate_html(table_rows):
    """Generate HTML content from processed event objects."""
    html_rows = [
        f"""
        <tr>
            {''.join(f'<td>{row[key]}</td>' for key in row)}
        </tr>
        """
        for row in table_rows
    ]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Event Action+Obs combined Visualizer</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                table-layout: auto; /* Change from fixed to auto */
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
                width: auto; /* Allow columns to autofit content */
            }}
            th {{
                background-color: #f2f2f2;
                position: sticky;
                top: 0;
                z-index: 1;
            }}
            tbody {{
                overflow-y: auto;
                max-height: 500px;
            }}
            thead, tbody tr {{
                /* Remove display: block to ensure proper alignment */
            }}
        </style>
    </head>
    <body>
        <h1>Action/Observation Visualizer</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Timestamp</th>
                    <th>Source</th>
                    <th>Message</th>
                    <th>Subt</th>
                    <th>Cache Read Tokens</th>
                    <th>Cache Creation Tokens</th>
                    <th>Completion Tokens</th>
                    <th>Cache Read Cost</th>
                    <th>Cache Creation Cost</th>
                    <th>Completion Cost</th>
                    <th>Event Cost(excluding cache-read)</th>
                    <th>Total Cost</th>
                    <th>Special</th>
                </tr>
            </thead>
            <tbody>
                {''.join(html_rows)}
            </tbody>
        </table>
    </body>
    </html>
    """
    return html_content

def visualize(data=None):
    # Process events into a list of objects
    table_rows = process_events(data)

    # Sort table_rows by event_cost in descending order
    table_rows.sort(key=lambda row: float(row["event_cost"].strip("$")), reverse=True)

    # Generate HTML content for the main table
    html_content = generate_html(table_rows)

    # Save the HTML to a file in the output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "event_action_obs.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Open the HTML file in the default web browser
    webbrowser.open(output_file)

if __name__ == "__main__":
    # Load the selected JSON file
    data = select_and_load_json()
    visualize(data)
