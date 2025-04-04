from datetime import datetime, timedelta
from common import COST_PER_CACHE_WRITE_TOKEN, COST_PER_CACHE_READ_TOKEN, COST_PER_COMPLETION_TOKEN

def process_events(data):
    """Process events and return a list of processed event objects."""
    table_rows = []
    previous_event_with_llm_usage = None

    for event in data:
        cause_event_id = event.get("cause")
        if cause_event_id is not None or event.get("action") == "condensation":
            # Extract timestamp
            current_timestamp = event.get("timestamp", "")
            if current_timestamp:
                current_timestamp = datetime.fromisoformat(current_timestamp)

            # Check if the previous event with llm_usage exists and is within 5 minutes
            special_note = ""  # Initialize special column
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
                .get("tool_call_metadata", {}).get("model_response", {}).get("usage", {}))
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

            table_rows.append({
                "id": event.get("id", ""),
                "timestamp": event.get("timestamp", ""),
                "source": event.get("source", ""),
                "message": message[:60],
                "subt": subt,
                "cache_read_tokens": cache_read_input_tokens,
                "cache_creation_tokens": cache_creation_input_tokens,
                "completion_tokens": completion_tokens,
                "cache_read_cost": f"${cache_read_cost:.2f}",
                "cache_creation_cost": f"${cache_creation_cost:.2f}",
                "completion_cost": f"${completion_cost:.2f}",
                "event_cost": f"${event_cost:.2f}",
                "total_cost": f"${total_cost:.2f}",
                "special": special_note
            })
    return table_rows
