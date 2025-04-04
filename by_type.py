from common import select_and_load_json
from process_events import process_events
import webbrowser
import os
from collections import defaultdict

def create_summary_rows(table_rows):
    """Create summary rows grouped by 'subt'."""
    # Filter out rows with 'special' set
    filtered_rows = [row for row in table_rows if not row["special"]]

    # Group rows by 'subt' and calculate aggregates
    grouped_data = defaultdict(lambda: {
        "count": 0,
        "sum_cache_creation_tokens": 0,
        "sum_completion_tokens": 0,
        "sum_cache_creation_cost": 0.0,
        "sum_completion_cost": 0.0,
        "sum_event_cost": 0.0
    })

    for row in filtered_rows:
        subt = row["subt"]
        grouped_data[subt]["count"] += 1
        grouped_data[subt]["sum_cache_creation_tokens"] += row["cache_creation_tokens"]
        grouped_data[subt]["sum_completion_tokens"] += row["completion_tokens"]
        grouped_data[subt]["sum_cache_creation_cost"] += float(row["cache_creation_cost"].strip("$"))
        grouped_data[subt]["sum_completion_cost"] += float(row["completion_cost"].strip("$"))
        grouped_data[subt]["sum_event_cost"] += float(row["event_cost"].strip("$"))

    # Prepare rows for the summary table
    summary_rows = []
    for subt, data in grouped_data.items():
        count = data["count"]
        summary_rows.append({
            "subt": subt,
            "count": count,
            "avg_cache_creation_tokens": data["sum_cache_creation_tokens"] / count,
            "avg_completion_tokens": data["sum_completion_tokens"] / count,
            "avg_cache_creation_cost": data["sum_cache_creation_cost"] / count,
            "avg_completion_cost": data["sum_completion_cost"] / count,
            "avg_event_cost": data["sum_event_cost"] / count,
            "sum_cache_creation_tokens": data["sum_cache_creation_tokens"],
            "sum_completion_tokens": data["sum_completion_tokens"],
            "sum_cache_creation_cost": data["sum_cache_creation_cost"],
            "sum_completion_cost": data["sum_completion_cost"],
            "sum_event_cost": data["sum_event_cost"]
        })

    # Filter out summary rows where 'subt' is "null" or 'sum_event_cost' is 0
    summary_rows = [
        row for row in summary_rows
        if row["subt"] != "null" and row["sum_event_cost"] != 0
    ]


    return summary_rows

def generate_html_summary(table_rows):
    """Generate a summary HTML table grouped by 'subt'."""
    # Use the reusable function to create summary rows
    summary_rows = create_summary_rows(table_rows)

    # Generate HTML rows for the summary table
    html_rows = [
        f"""
        <tr>
            <td>{row['subt']}</td>
            <td>{row['count']}</td>
            <td>{row['sum_cache_creation_tokens']}</td>
            <td>{row['avg_cache_creation_tokens']:.2f}</td>
            <td>{row['sum_completion_tokens']}</td>
            <td>{row['avg_completion_tokens']:.2f}</td>
            <td>${row['sum_cache_creation_cost']:.2f}</td>
            <td>${row['avg_cache_creation_cost']:.2f}</td>
            <td>${row['sum_completion_cost']:.2f}</td>
            <td>${row['avg_completion_cost']:.2f}</td>
            <td>${row['sum_event_cost']:.2f}</td>
            <td>${row['avg_event_cost']:.2f}</td>
        </tr>
        """
        for row in summary_rows
    ]

    # Generate HTML content for the summary table
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Summary by Type</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                table-layout: auto;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                position: sticky;
                top: 0;
                z-index: 1;
            }}
        </style>
    </head>
    <body>
        <h1>Summary by Type</h1>
        <table>
            <thead>
                <tr>
                    <th>Subt</th>
                    <th>Count</th>
                    <th>Sum Cache Creation Tokens</th>
                    <th>Avg Cache Creation Tokens</th>
                    <th>Sum Completion Tokens</th>
                    <th>Avg Completion Tokens</th>
                    <th>Sum Cache Creation Cost</th>
                    <th>Avg Cache Creation Cost</th>
                    <th>Sum Completion Cost</th>
                    <th>Avg Completion Cost</th>
                    <th>Sum Event Cost</th>
                    <th>Avg Event Cost</th>
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

    # Generate HTML content for the summary table
    html_content = generate_html_summary(table_rows)

    # Save the HTML to a file in the output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "by_type.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Open the HTML file in the default web browser
    webbrowser.open(output_file)

if __name__ == "__main__":
    # Load the selected JSON file
    data = select_and_load_json()
    visualize(data)
