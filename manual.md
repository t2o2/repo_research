manual.md

```
# Active Developers Tracker

This software is designed to track the number of unique active developers within a group of repositories over time. An active developer is defined as a developer who has committed a change to any of the repositories within a rolling 30-day window throughout the commit history.

## Quick Install

Before running the software, you need to install the necessary Python packages. You can do this by running the following command in your terminal:

`pip install -r requirements.txt`

## What does this software do?

The software takes a TOML file as input, which contains the URLs of the repositories you want to track. It then uses the GitHub API to fetch the commit history of each repository and calculates the number of unique active developers for each day. The results are written to a CSV file.

## How to use it?

1. **Prepare your TOML file**: The TOML file should contain the URLs of the repositories you want to track. Here is an example:

```
# Ecosystem Level Information
title = "Magi"

sub_ecosystems = []

github_organizations = ["https://github.com/magi-project"]

# Repositories
[[repo]]
url = "https://github.com/m-pays/m-cpuminer-qt"

[[repo]]
url = "https://github.com/m-pays/m-cpuminer-v2"

[[repo]]
url = "https://github.com/m-pays/magi"

[[repo]]
url = "https://github.com/m-pays/magi-api-cpp"
```

2. **Run the software**: You can run the software by executing the main.py file in your terminal. Make sure to replace 'YOUR_TOKEN' in the headers dictionary with your GitHub API token. Also, update the file paths in the `parse_toml_file` and `write_to_csv` function calls if necessary.

```
python main.py
```

3. **Check the results**: The software will create a CSV file named 'output.csv' (or whatever name you specified in the `write_to_csv` function call). The CSV file will contain the date and the number of active developers for each day, like this:

```
date       | active developers
-----------+------------------
2021-01-10 | 10
2021-01-11 | 2
2021-01-12 | 23
2021-01-13 | 9
```

## Documentation

For more detailed information about the functions used in the software, please refer to the comments in the main.py file.
```