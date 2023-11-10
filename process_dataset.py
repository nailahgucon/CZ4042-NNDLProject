import os
import csv

captures_directory = 'captures'
image_labels = []

# get the labels for each image in the directory
for f in os.listdir(captures_directory):
    # get suffix of filename
    indicated_key = f.rsplit('.', 1)[0].rsplit(" ", 1)[1]

    # if suffix of file name is "n"
    if indicated_key == "n":
        image_labels.append({'file_name': f, 'class': 0})
    # if suffix of file name is "space"
    elif indicated_key == "space":
        image_labels.append({'file_name': f, 'class': 1})
    # if suffix of file name is "down"
    elif indicated_key == "down":
        image_labels.append({'file_name': f, 'class': 2})

# define the field names for the CSV file
field_names = ['file_name', 'class']

# write the labels to a csv file
with open('labels.csv', 'w') as csvfile:
    # Create a CSV writer with the specified field names
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    # Write the header to the CSV file
    writer.writeheader()
    # Write the label data to the CSV file
    writer.writerows(image_labels)