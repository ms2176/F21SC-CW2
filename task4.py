from collections import defaultdict
from load import load_data

# Runs Task 4: Top N readers by total reading time
def run_task_4(file_path, top_n=10):
    user_readtime = defaultdict(int) # Dictionary to accumulate read times per user

    for r in load_data(file_path): # Iterate through all records
        user = r.get("visitor_uuid") # Get visitor UUID
        readtime = r.get("event_readtime") # Get reading time

        if user and readtime: # Ensure both user and readtime are valid
            user_readtime[user] += readtime # Accumulate reading time

    top_readers = sorted(user_readtime.items(), key=lambda x: x[1], reverse=True)[:top_n] # Sort through users by total read time, then sort by the second item in the tuple (total read time), reverse for descending order and get top N

    lines = [] # Prepare output lines
    lines.append(f"Top {top_n} readers by total reading time") # Header line
    lines.append("{:<40} {:>15}".format("Visitor UUID", "Total Read Time (s)")) # Column headers

    for user, total_time in top_readers: # Format each top reader's info
        lines.append("{:<40} {:>15}".format(user, total_time)) # Format each line with user and total read time
        print(f"User: {user}, Total Read Time: {total_time}") # Debug print statement
        
    return "\n".join(lines) # Return the formatted output as a single string

