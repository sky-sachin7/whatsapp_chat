import pandas as pd
import re
from datetime import datetime

def process_chat_file(chat_data):
    """
    Process the WhatsApp chat data and return a DataFrame.

    Parameters:
    chat_data (list of str): List of chat lines.

    Returns:
    pd.DataFrame: DataFrame containing the processed chat data.
    """
    # Regular expression to match the date and time format in WhatsApp exports (24-hour format)
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} - )(.+?): (.*)'

    # Prepare lists to hold the data
    date_time = []
    users = []
    messages = []

    for line in chat_data:
        match = re.match(pattern, line)
        if match:
            # Convert date and time to the desired format
            dt_str = match.group(1).strip()
            dt = datetime.strptime(dt_str[:-3], '%d/%m/%Y, %H:%M')  # Remove the trailing ' -'
            formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
            date_time.append(formatted_dt)  # Formatted date and time

            user = match.group(2).strip()  # Extract user name
            message = match.group(3).strip()  # Extract message
            users.append(user)  # Append user
            messages.append(message)  # Append message
        else:
            # Handle cases where the message might be a media omitted or a continuation
            if "Media omitted" in line:
                if messages:  # Check if there is a previous message
                    date_time.append(date_time[-1])  # Use the last date_time
                    users.append("Media omitted")
                    messages.append("Media omitted")
            elif line.strip():  # If the line is not empty
                # This handles cases where the message might be a continuation of the previous message
                if messages:  # Check if there is a previous message
                    messages[-1] += f"\n{line.strip()}"

    # Create a DataFrame with user and message
    df = pd.DataFrame({
        'date': date_time,
        'user': users,
        'message': messages
    })

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Extract the year, month, day, hour, and minute from the 'date' column
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['date_only'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period
    # Optionally, you can sort the DataFrame by date
    df.sort_values(by='date', inplace=True)

    return df