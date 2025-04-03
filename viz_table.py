import json
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from common import select_and_load_json
import matplotlib.pyplot as plt

def visualize(data=None):
    """Visualize data in a table format."""    

    # Extract events that include LLM metrics (accumulated_token_usage)
    llm_events = []
    for event in data:
        llm_metrics = event.get("llm_metrics")
        if llm_metrics and "accumulated_token_usage" in llm_metrics:
            usage = llm_metrics["accumulated_token_usage"]
            llm_events.append({
                "id": event["id"],
                "completion_tokens": usage.get("completion_tokens", 0),
                "cache_write_tokens": usage.get("cache_write_tokens", 0),
            })

    # Define cost rates in USD per token (per million tokens)
    COST_PER_COMPLETION_TOKEN = 15.00 / 1000 / 1000
    COST_PER_CACHE_WRITE_TOKEN = 3.75 / 1000 / 1000

    # Compute total cost per event for cache-write and completion
    for event in llm_events:
        event["total_cost"] = (
            event["completion_tokens"] * COST_PER_COMPLETION_TOKEN +
            event["cache_write_tokens"] * COST_PER_CACHE_WRITE_TOKEN
        )

    # Sort events by total cost (descending) and select the top 10
    top_events = sorted(llm_events, key=lambda e: e["total_cost"], reverse=True)[:10]

    # Prepare data for the table
    table_data = [
        [
            evt["id"],
            f"${evt['total_cost']:.2f}",
            f"${evt['cache_write_tokens'] * COST_PER_CACHE_WRITE_TOKEN:.2f}",
            f"${evt['completion_tokens'] * COST_PER_COMPLETION_TOKEN:.2f}"
        ]
        for evt in top_events
    ]

    # Create a figure for the table
    fig, ax_table = plt.subplots(figsize=(12, 4))
    ax_table.axis('tight')
    ax_table.axis('off')

    # Add the table to the figure
    table = ax_table.table(
        cellText=table_data,
        colLabels=["ID", "Total Cost", "Cache Write Cost", "Completion Cost"],
        loc="center",
        cellLoc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(table_data[0]))))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize(data = select_and_load_json())
