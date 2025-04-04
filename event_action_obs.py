from common import select_and_load_json, COST_PER_CACHE_WRITE_TOKEN, COST_PER_CACHE_READ_TOKEN, COST_PER_COMPLETION_TOKEN
import webbrowser
import os
from datetime import datetime, timedelta

def visualize(data=None):
    # Prepare data for the table
    table_rows = []
    previous_event_with_llm_usage = None

    for event in data:
        cause_event_id = event.get("cause")
        special_note = ""  # Initialize special column
        if cause_event_id is not None or event.get("action") == "condensation":
            # Extract timestamp
            current_timestamp = event.get("timestamp", "")
            if current_timestamp:
                current_timestamp = datetime.fromisoformat(current_timestamp)

            # Check if the previous event with llm_usage exists and is within 5 minutes
            if previous_event_with_llm_usage:
                previous_timestamp = previous_event_with_llm_usage.get("timestamp", "")
                if previous_timestamp:
                    previous_timestamp = datetime.fromisoformat(previous_timestamp)
                    if current_timestamp - previous_timestamp > timedelta(minutes=5):
                        special_note = "cache miss: outdated"  # Set special note

            # Extract message and other details
            message = event.get("message", "")
            args = event.get("args", {})
            if "path" in args:
                message += f" (Path: {args['path']})"
            if "command" in args:
                message += f" (Command: {args['command']})"
            subt = event.get("observation", event.get("action", "UNKNOWN-TYPE"))

            # Extract LLM usage object
            llm_usage = (event
                .get("tool_call_metadata", {}).get("model_response", {}).get("usage",{}))
            if llm_usage == {}:
                llm_usage = event.get("llm_metrics", {}).get("accumulated_token_usage", {})
            cache_read_input_tokens = llm_usage.get("cache_read_input_tokens", 0)
            cache_creation_input_tokens = llm_usage.get("cache_creation_input_tokens", 0)
            completion_tokens = llm_usage.get("completion_tokens", 0)

            # If llm_usage exists, update the previous event with llm_usage
            if llm_usage:
                previous_event_with_llm_usage = event

            # Calculate costs
            cache_read_cost = cache_read_input_tokens * COST_PER_CACHE_READ_TOKEN
            cache_creation_cost = cache_creation_input_tokens * COST_PER_CACHE_WRITE_TOKEN
            completion_cost = completion_tokens * COST_PER_COMPLETION_TOKEN
            event_cost = cache_creation_cost + completion_cost  # Exclude cache-read
            total_cost = event_cost + cache_read_cost  # Include cache-read cost

            table_rows.append((
                event.get("id", ""),
                event.get("timestamp", ""),
                event.get("source", ""),
                message[:60],
                subt,
                cache_read_input_tokens,
                cache_creation_input_tokens,
                completion_tokens,
                f"${cache_read_cost:.2f}",  # Add cache read cost
                f"${cache_creation_cost:.2f}",
                f"${completion_cost:.2f}",
                f"${event_cost:.2f}",
                f"${total_cost:.2f}",  # Add total cost
                special_note
            ))

    # Generate HTML rows dynamically based on the length of each row
    html_rows = [
        f"""
        <tr>
            {''.join(f'<td>{cell}</td>' for cell in row)}
        </tr>
        """
        for row in table_rows
    ]

    # Generate HTML content
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
        <h1>Input Cost Visualizer</h1>
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
                    <th>Cache Read Cost</th> <!-- Add column header -->
                    <th>Cache Creation Cost</th>
                    <th>Completion Cost</th>
                    <th>Event Cost(excluding cache-read)</th>
                    <th>Total Cost</th> <!-- Add column header -->
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
