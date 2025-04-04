from common import select_and_load_json
from viz_charts import visualize as visualize_charts
from completion_cost import visualize as visualize_completion_cost
from by_type import visualize as visualize_by_type
from input_cost import visualize as visualize_input_cost
from event_action_obs import visualize as visualize_event_action_obs
from all_events import visualize as visualize_all_events

if __name__ == "__main__":
    # Load the selected JSON file
    data = select_and_load_json()

    # Run all visualizers
    visualize_charts(data)
    visualize_completion_cost(data)
    visualize_by_type(data)
    visualize_input_cost(data)
    visualize_event_action_obs(data)
    visualize_all_events(data)
