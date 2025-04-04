import numpy as np
import matplotlib.pyplot as plt
from common import select_and_load_json, COST_PER_COMPLETION_TOKEN, COST_PER_CACHE_WRITE_TOKEN, COST_PER_CACHE_READ_TOKEN
from by_type import create_summary_rows
from process_events import process_events

def visualize(data=None):
    
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
                "cache_read_tokens": usage.get("cache_read_tokens", 0),
            })

    # Sort events by ID for chronological order
    llm_events.sort(key=lambda x: x["id"])

    # Prepare data arrays for plotting
    ids = [str(evt["id"]) for evt in llm_events]
    completion_tokens = np.array([evt["completion_tokens"] for evt in llm_events], dtype=float)
    cache_write_tokens = np.array([evt["cache_write_tokens"] for evt in llm_events], dtype=float)
    cache_read_tokens = np.array([evt["cache_read_tokens"] for evt in llm_events], dtype=float)

    x = np.arange(len(ids))

    # Compute cost for each token type (in USD)
    completion_cost = completion_tokens * COST_PER_COMPLETION_TOKEN
    cache_write_cost = cache_write_tokens * COST_PER_CACHE_WRITE_TOKEN
    cache_read_cost = cache_read_tokens * COST_PER_CACHE_READ_TOKEN

    # Create two subplots: one for token counts and one for cost
    fig, (ax_top, ax_bottom) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8), sharex=True)

    # ----- Top subplot: Token Usage -----
    ax_top.bar(x, cache_read_tokens, color='skyblue', label='cache_read_tokens')
    ax_top.bar(x, cache_write_tokens, bottom=cache_read_tokens, color='orange', label='cache_write_tokens')
    ax_top.bar(x, completion_tokens, bottom=cache_read_tokens + cache_write_tokens, color='red', label='completion_tokens')

    ax_top.set_ylabel("Tokens")
    ax_top.set_title("LLM Token Usage (Top) vs Cost in USD (Bottom) by Event")
    ax_top.legend(loc='upper left')

    # ----- Bottom subplot: Cost -----
    ax_bottom.bar(x, cache_read_cost, color='skyblue', label='cache_read_cost')
    ax_bottom.bar(x, cache_write_cost, bottom=cache_read_cost, color='orange', label='cache_write_cost')
    ax_bottom.bar(x, completion_cost, bottom=cache_read_cost + cache_write_cost, color='red', label='completion_cost')

    ax_bottom.set_ylabel("Cost (USD)")
    ax_bottom.legend(loc='upper left')
    ax_bottom.set_xlabel("Event ID")
    ax_bottom.set_xticks(x)
    ax_bottom.set_xticklabels(ids, rotation=45)

    plt.tight_layout()
    plt.show()

    # Compute total tokens and costs
    total_completion_tokens = np.sum(completion_tokens)
    total_cache_write_tokens = np.sum(cache_write_tokens)
    total_cache_read_tokens = np.sum(cache_read_tokens)

    total_completion_cost = np.sum(completion_cost)
    total_cache_write_cost = np.sum(cache_write_cost)
    total_cache_read_cost = np.sum(cache_read_cost)

    # Create two additional pie charts
    fig, (ax_pie_tokens, ax_pie_costs) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # ----- Pie chart: Token Distribution -----
    token_labels = ['Completion Tokens', 'Cache Write Tokens', 'Cache Read Tokens']
    token_values = [total_completion_tokens, total_cache_write_tokens, total_cache_read_tokens]
    ax_pie_tokens.pie(token_values, labels=token_labels, autopct='%1.1f%%', startangle=90, colors=['red', 'orange', 'skyblue'])
    ax_pie_tokens.set_title("Token Distribution")

    # ----- Pie chart: Cost Distribution -----
    cost_labels = ['Completion Cost', 'Cache Write Cost', 'Cache Read Cost']
    cost_values = [total_completion_cost, total_cache_write_cost, total_cache_read_cost]
    ax_pie_costs.pie(cost_values, labels=cost_labels, autopct='%1.1f%%', startangle=90, colors=['red', 'orange', 'skyblue'])
    ax_pie_costs.set_title("Cost Distribution (USD)")

    plt.tight_layout()
    plt.show()

    # ----- Additional Pie Chart: Event Cost by Type -----
    # Create summary rows using the reusable function
    table_rows = process_events(data)
    summary_rows = create_summary_rows(table_rows)

    # Extract data for the pie chart
    event_types = [row["subt"] for row in summary_rows]
    event_costs = [row["sum_event_cost"] for row in summary_rows]

    # Create the pie chart
    fig, ax_event_cost = plt.subplots(figsize=(8, 6))
    ax_event_cost.pie(event_costs, labels=event_types, autopct='%1.1f%%', startangle=90)
    ax_event_cost.set_title("Event Cost Distribution by Type (USD). Excludes cache-read cost")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    visualize(data = select_and_load_json())
