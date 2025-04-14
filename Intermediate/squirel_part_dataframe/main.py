import pandas

with open('2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv', 'r') as file:
    # Read the CSV file into a DataFrame
    df = pandas.read_csv(file)

# Count the number of squirrels by fur color
squirrel_count = df['Primary Fur Color'].value_counts()
# Create a new DataFrame with the counts
squirrel_count_df = pandas.DataFrame({
    'Fur Color': squirrel_count.index,
    'Count': squirrel_count.values
})
# Save the new DataFrame to a CSV file
squirrel_count_df.to_csv('squirrel_count.csv', index=False)
# Print the DataFrame
print(squirrel_count_df)
