'''
This is the main file for the application. It orchestrates the execution of the other functions.
'''
import os
import time
import toml
import requests
import csv
import pandas as pd
from datetime import datetime, timedelta
from collections import deque
def parse_toml_file(file_path):
    '''
    This function parses the input toml file and returns the list of repository URLs.
    It also handles the FileNotFoundError exception and provides a meaningful error message to the user.
    '''
    if os.path.exists(file_path):
        try:
            with open(file_path) as file:
                data = toml.load(file)
                repo_urls = [repo['url'] for repo in data['repo']]
                return repo_urls
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file '{file_path}' not found.")
    else:
        raise FileNotFoundError(f"Input file '{file_path}' not found.")
def get_commit_history(repo_url, headers):
    '''
    This function uses the GitHub API to fetch the commit history of a repository.
    It also handles the rate limit of the GitHub API by waiting until the rate limit resets.
    It uses pagination to fetch the commit history in smaller chunks.
    '''
    api_url = repo_url.replace('github.com', 'api.github.com/repos') + '/commits'
    commits = []
    while api_url:
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if response.status_code == 403 and 'X-RateLimit-Reset' in response.headers:
                reset_time = int(response.headers['X-RateLimit-Reset'])
                sleep_time = reset_time - int(time.time())
                if sleep_time > 0:
                    time.sleep(sleep_time)
                continue
            print(f'An error occurred while making a request to the GitHub API: {e}')
            return []
        commits.extend(response.json())
        if 'next' in response.links:
            api_url = response.links['next']['url']
        else:
            break
    return commits
def calculate_active_developers(repo_urls, headers):
    '''
    This function calculates the number of unique active developers for each day.
    '''
    active_developers = {}
    for repo_url in repo_urls:
        commits = get_commit_history(repo_url, headers)
        for commit in commits:
            date = commit['commit']['author']['date'][:10]
            author = commit['commit']['author']['name']
            if date not in active_developers:
                active_developers[date] = set()
            active_developers[date].add(author)
    return {date: len(authors) for date, authors in active_developers.items()}
def write_to_csv(active_developers, file_path):
    '''
    This function writes the output to a csv file.
    '''
    df = pd.DataFrame([{'date': k, 'active developers': v} for k, v in active_developers.items()])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    df.to_csv(file_path)
def main():
    '''
    The main function of the application.
    '''
    headers = {'Authorization': 'token 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'}
    repo_urls = parse_toml_file('input.toml')  # Update the file path if necessary
    active_developers = calculate_active_developers(repo_urls, headers)
    write_to_csv(active_developers, 'output.csv')
if __name__ == "__main__":
    main()