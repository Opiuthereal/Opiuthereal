import requests
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = 'Opiuthereal'
API_URL = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'
README_FILE = "README.md"

# function to obtain total of commits
def get_github_commits():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        total_commits = 0
        
        # Get number of commit for each repo
        for repo in repos:
            commits_url = repo['commits_url'].replace('{/sha}', '')
            commits_response = requests.get(commits_url, headers=headers)
            if commits_response.status_code == 200:
                total_commits += len(commits_response.json())
            else:
                print(f"Erreur lors de la récupération des commits pour {repo['name']}")
        
        return total_commits, len(repos)
    else:
        print(f"Erreur lors de l'appel API: {response.status_code}")
        return 0, 0

# function tu update urls of badges inside README.md
def update_readme():
    total_commits, repo_count = get_github_commits()
    
    stats_url = f"https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}&theme=dark&hide_border=true&include_all_commits=true&count_private=true&cache_seconds=60"
    streak_url = f"https://nirzak-streak-stats.vercel.app/?user={GITHUB_USERNAME}&theme=dark&hide_border=false&cache_seconds=60"
    langs_url = f"https://github-readme-stats.vercel.app/api/top-langs/?username={GITHUB_USERNAME}&theme=dark&hide_border=false&langs_count=20&layout=compact&cache_seconds=60"

    with open(README_FILE, "r", encoding="utf-8") as file:
        readme_content = file.readlines()

    # update badges
    for i, line in enumerate(readme_content):
        if "github-readme-stats.vercel.app/api" in line:
            readme_content[i] = f"![Stats]({stats_url})\n"
        elif "nirzak-streak-stats.vercel.app" in line:
            readme_content[i] = f"![Streak]({streak_url})\n"
        elif "github-readme-stats.vercel.app/api/top-langs" in line:
            readme_content[i] = f"![Top Langs]({langs_url})\n"

    # update the README.md
    with open(README_FILE, "w", encoding="utf-8") as file:
        file.writelines(readme_content)

    #print("README.md updated with success !")

update_readme()
