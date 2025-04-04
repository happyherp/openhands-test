from common import select_and_load_json, COST_PER_CACHE_WRITE_TOKEN, save_and_open_html
import webbrowser
import os

def visualize(data=None):
    """Visualize input cost data."""

    # Prepare data for the table
    table_rows = []
    for event in data:
        obs = event.get("observation", None)
        new_input_tokens = event.get("tool_call_metadata", {})\
            .get("model_response", {})\
            .get("usage", {}).get("cache_creation_input_tokens")
        if obs is not None and new_input_tokens is not None:  # Include cache creation tokens
            message = event.get("message", "")
            args = event.get("args", {})
            if "path" in args:
                message += f" (Path: {args['path']})"
            if "command" in args:
                message += f" (Command: {args['command']})"
            cache_creation_cost = new_input_tokens * COST_PER_CACHE_WRITE_TOKEN
            table_rows.append((
                event.get("id", ""),
                event.get("timestamp", ""),
                event.get("source", ""),
                obs,
                message[:60],
                new_input_tokens,
                f"${cache_creation_cost:.6f}"
            ))

    # Sort rows by input tokens in descending order
    table_rows.sort(key=lambda x: x[5], reverse=True)

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
        <title>Input Cost Visualizer</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
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
                    <th>Observation</th>
                    <th>Message</th>
                    <th>Cache Creation Tokens</th>
                    <th>Cache Creation Cost</th>
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
    save_and_open_html(html_content, "input_cost.html")

if __name__ == "__main__":
    # Load the selected JSON file
    data = select_and_load_json()
    visualize(data)
