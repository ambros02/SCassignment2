import csv
from prettytable import PrettyTable
from datetime import datetime

def aggregate_trace(trace_file):
    function_calls = {}

    with open(trace_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header

        for row in csv_reader:
            unique_id, function_name, event, timestamp = row
            unique_id = int(unique_id)

            if event == 'start':
                if function_name in function_calls:
                    function_calls[function_name]['num_calls'] += 1
                    function_calls[function_name]['start_time'] = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
                else:
                    function_calls[function_name] = {'num_calls': 1, 'start_time': datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f"), 'total_time': 0}

            elif event == 'stop':
                if function_name in function_calls:
                    start_time = function_calls[function_name]['start_time']
                    execution_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") - start_time
                    function_calls[function_name]['total_time'] += execution_time.total_seconds()

    return function_calls

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python reporting.py trace_file.log")
        sys.exit(1)

    trace_file = sys.argv[1]

    function_calls = aggregate_trace(trace_file)

    # Create a PrettyTable
    table = PrettyTable()
    table.field_names = ["Function Name", "Num. of calls", "Total Time (ms)", "Average Time (ms)"]

    for function_name, data in function_calls.items():
        num_calls = data['num_calls']
        total_time = data['total_time']
        average_time = total_time / num_calls if num_calls > 0 else 0

        # Format the times to milliseconds
        total_time_ms = total_time * 1000
        average_time_ms = average_time * 1000

        # Add data to the table
        table.add_row([function_name, num_calls, f"{total_time_ms:.3f}", f"{average_time_ms:.3f}"])

    # Set the alignment to right for numeric columns
    table.align["Num. of calls"] = "r"
    table.align["Total Time (ms)"] = "r"
    table.align["Average Time (ms)"] = "r"

    # Print the table
    print(table)
