from common import select_and_load_json, COST_PER_CACHE_WRITE_TOKEN, COST_PER_CACHE_READ_TOKEN, COST_PER_COMPLETION_TOKEN, save_and_open_html
import webbrowser
import os

def visualize(data=None):
    # Prepare data for the table
    table_rows = []
    for event in data:
        message = event.get("message", "")
        args = event.get("args", {})
        if "path" in args:
            message += f" (Path: {args['path']})"
        if "command" in args:
            message += f" (Command: {args['command']})"
        event_type = "observation" if "observation" in event else "action"
        subt = event.get("observation", event.get("action", ""))

        # Extract LLM usage object
        llm_usage = event.get("tool_call_metadata", {}).get("model_response", {}).get("usage", {})
        cache_read_input_tokens = llm_usage.get("cache_read_input_tokens", 0)
        cache_creation_input_tokens = llm_usage.get("cache_creation_input_tokens", 0)
        completion_tokens = llm_usage.get("completion_tokens", 0)

        # Calculate costs
        cache_read_cost = cache_read_input_tokens * COST_PER_CACHE_READ_TOKEN
        cache_creation_cost = cache_creation_input_tokens * COST_PER_CACHE_WRITE_TOKEN
        completion_cost = completion_tokens * COST_PER_COMPLETION_TOKEN
        total_cost = cache_read_cost + cache_creation_cost + completion_cost

        table_rows.append((
            event.get("id", ""),
            event.get("timestamp", ""),
            event.get("source", ""),
            message[:60],
            event_type,
            subt,
            cache_read_input_tokens,
            cache_creation_input_tokens,
            completion_tokens,
            f"${cache_read_cost:.2f}",
            f"${cache_creation_cost:.2f}",
            f"${completion_cost:.2f}",
            f"${total_cost:.2f}"
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
        <title>All Events</title>
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
        <h1>All Events</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Timestamp</th>
                    <th>Source</th>
                    <th>Message</th>
                    <th>Type</th>
                    <th>Subt</th>
                    <th>Cache Read Tokens</th>
                    <th>Cache Creation Tokens</th>
                    <th>Completion Tokens</th>
                    <th>Cache Read Cost</th>
                    <th>Cache Creation Cost</th>
                    <th>Completion Cost</th>
                    <th>Total Cost</th>
                </tr>
            </thead>
            <tbody>
                {''.join(html_rows)}
            </tbody>
        </table>
    </body>
    </html>
    """

    # Save and open the HTML file
    save_and_open_html(html_content, "events.html")

if __name__ == "__main__":
    # Load the selected JSON file
    data = select_and_load_json()
    visualize(data)
