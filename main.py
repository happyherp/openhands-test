from common import select_and_load_json
from viz_charts import visualize as visualize_charts
from completion_cost import visualize as visualize_completion_cost

if __name__ == "__main__":
    # Load the selected JSON file
    data = select_and_load_json()

    # Run all visualizers
    visualize_charts(data)
    visualize_completion_cost(data)
