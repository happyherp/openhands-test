from common import select_and_load_json, COST_PER_COMPLETION_TOKEN, save_and_open_html
import webbrowser
import os

def visualize(data=None):
    """Visualize completion cost data."""

    # Prepare data for the table
    table_rows = []
    for event in data:
        llm_metrics = event.get("llm_metrics", {}).get("accumulated_token_usage", {})
        if "completion_tokens" in llm_metrics:
            message = event.get("message", "")
            args = event.get("args", {})
            if "path" in args:
                message += f" (Path: {args['path']})"
            if "command" in args:
                message += f" (Command: {args['command']})"
            completion_tokens = llm_metrics.get("completion_tokens", 0)
            cost = completion_tokens * COST_PER_COMPLETION_TOKEN
            table_rows.append((
                event.get("id", ""),
                event.get("timestamp", ""),
                event.get("source", ""),
                event.get("action", ""),
                message[:60],
                completion_tokens,
                f"${cost:.6f}"
            ))

    # Sort rows by completion tokens in descending order
    table_rows.sort(key=lambda x: x[5], reverse=True)

    # Generate HTML rows
    html_rows = [
        f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
            <td>{row[5]}</td>
            <td>{row[6]}</td>
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
        <title>Completion Cost Visualizer</title>
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
        <h1>Completion Cost Visualizer</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Timestamp</th>
                    <th>Source</th>
                    <th>Action</th>
                    <th>Message</th>
                    <th>Completion Tokens</th>
                    <th>Cost</th>
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
    save_and_open_html(html_content, "completion_cost.html")

if __name__ == "__main__":
    # Load the selected JSON file
    data = select_and_load_json()
    visualize(data)
