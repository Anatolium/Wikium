import re
from collections import defaultdict

# Dictionary for team name transformations
TEAM_NAMES = {
    '«Спартак» (Москва)': 'Спартак М',
    '«Динамо» (Москва)': 'Динамо М',
    'ЦСКА(Москва)': 'ЦСКА',
    'ЦСКА': 'ЦСКА',
    '«Локомотив» (Москва)': 'Локомотив',
    '«Крылья Советов» (Москва)': 'Крылья Советов',
    '«Торпедо» (Горький)': 'Торпедо',
    '«Химик» (Воскресенск)': 'Химик',
    '«Трактор» (Челябинск)': 'Трактор',
    'СКА (Ленинград)': 'СКА Л',
    'СКА (Калинин)': 'СКА Кл',
    '«Молот» (Пермь)': 'Молот',
    '«Динамо» (Новосибирск)': 'Динамо Нс',
    '«Металлург» (Новокузнецк)': 'Металлург Нк',
    '«Электросталь» (Электросталь)': 'Электросталь',
    '«Даугава» (Рига)': 'Даугава',
    '«Спартак» (Свердловск)': 'Спартак Св',
    'СКА (Куйбышев)': 'СКА Кб',
    '«Спартак» (Омск)': 'Спартак Ом',
    '«Кировец» (Ленинград)': 'Кировец',
    'ЛИИЖТ (Ленинград)': 'ЛИИЖТ',
    '«Динамо» (Киев)': 'Динамо К',
    '«Сибирь» (Новосибирск)': 'Сибирь',
    '«Торпедо» (Минск)': 'Торпедо Мн'
}

def parse_match(line, match_counter=None):
    # Regular expression for standard matches with "Матч №"
    standard_pattern_with_num = r'Матч\s*№\s*(\d+)\.\s*([^–—-]+?)\s*[–—-]\s*([^–—-]+?)\s*[–—-]\s*(\d+)\s*:\s*(\d+)(?:\s*\(.*?\))?(?:\s*.*)?'
    # Regular expression for technical defeats with "Матч №"
    technical_pattern_with_num = r'Матч\s*№\s*(\d+)\.\s*([^–—-]+?)\s*[–—-]\s*([^–—-]+?)\s*-\s*:\s*\+(?:\s*.*)?'
    # Regular expression for standard matches without "Матч №"
    standard_pattern_no_num = r'([^–—-]+?)\s*[–—-]\s*([^–—-]+?)\s*[–—-]\s*(\d+)\s*:\s*(\d+)(?:\s*\(.*?\))?(?:\s*.*)?'
    # Regular expression for technical defeats without "Матч №"
    technical_pattern_no_num = r'([^–—-]+?)\s*[–—-]\s*([^–—-]+?)\s*-\s*:\s*\+(?:\s*.*)?'

    # Try standard match with "Матч №"
    match = re.match(standard_pattern_with_num, line.strip())
    if match:
        match_num, team1, team2, goals1, goals2 = match.groups()
        team1 = team1.strip()
        team2 = team2.strip()
        return (int(match_num), TEAM_NAMES.get(team1, team1), TEAM_NAMES.get(team2, team2),
                int(goals1), int(goals2), False)

    # Try technical defeat with "Матч №"
    match = re.match(technical_pattern_with_num, line.strip())
    if match:
        match_num, team1, team2 = match.groups()
        team1 = team1.strip()
        team2 = team2.strip()
        return (int(match_num), TEAM_NAMES.get(team1, team1), TEAM_NAMES.get(team2, team2),
                '-', '+', True)

    # Try standard match without "Матч №"
    match = re.match(standard_pattern_no_num, line.strip())
    if match:
        team1, team2, goals1, goals2 = match.groups()
        team1 = team1.strip()
        team2 = team2.strip()
        return (match_counter, TEAM_NAMES.get(team1, team1), TEAM_NAMES.get(team2, team2),
                int(goals1), int(goals2), False)

    # Try technical defeat without "Матч №"
    match = re.match(technical_pattern_no_num, line.strip())
    if match:
        team1, team2 = match.groups()
        team1 = team1.strip()
        team2 = team2.strip()
        return (match_counter, TEAM_NAMES.get(team1, team1), TEAM_NAMES.get(team2, team2),
                '-', '+', True)

    return None

def update_team_stats(teams, team1, team2, result1, result2, is_technical):
    # Initialize team stats if not already present
    for team in (team1, team2):
        if team not in teams:
            teams[team] = {'games': 0, 'wins': 0, 'draws': 0, 'losses': 0,
                           'goals_scored': 0, 'goals_conceded': 0, 'points': 0}

    # Update game count
    teams[team1]['games'] += 1
    teams[team2]['games'] += 1

    if is_technical:
        # Handle technical defeat
        if result1 == '-':
            teams[team1]['losses'] += 1
            teams[team2]['wins'] += 1
            teams[team2]['points'] += 2
        elif result2 == '-':
            teams[team2]['losses'] += 1
            teams[team1]['wins'] += 1
            teams[team1]['points'] += 2
    else:
        # Update goals for standard match
        teams[team1]['goals_scored'] += result1
        teams[team1]['goals_conceded'] += result2
        teams[team2]['goals_scored'] += result2
        teams[team2]['goals_conceded'] += result1

        # Update wins/draws/losses and points for standard match
        if result1 > result2:
            teams[team1]['wins'] += 1
            teams[team1]['points'] += 2
            teams[team2]['losses'] += 1
        elif result2 > result1:
            teams[team2]['wins'] += 1
            teams[team2]['points'] += 2
            teams[team1]['losses'] += 1
        else:
            teams[team1]['draws'] += 1
            teams[team2]['draws'] += 1
            teams[team1]['points'] += 1
            teams[team2]['points'] += 1

def print_table(teams):
    # Sort teams by points (descending), then by goal difference, then by goals scored
    sorted_teams = sorted(teams.items(),
                          key=lambda x: (x[1]['points'],
                                         x[1]['goals_scored'] - x[1]['goals_conceded'],
                                         x[1]['goals_scored']),
                          reverse=True)

    # Print header
    print(' М.......................И  В Н П     Ш     О')

    # Print team stats
    for i, (team, stats) in enumerate(sorted_teams, 1):
        goals = f"{stats['goals_scored']:>3}-{stats['goals_conceded']:<3}"
        print(
            f"{i:2}. {team:.<20}{stats['games']:2} {stats['wins']:2} {stats['draws']:1} {stats['losses']:2} {goals:>7} {stats['points']:2}")

def main():
    # Get input from user and add .txt extension
    filename = input("Введите название файла: ") + '.txt'
    n = int(input("Введите количество матчей: "))

    teams = defaultdict(dict)
    match_counter = 1

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                match_data = parse_match(line, match_counter)
                if match_data:
                    match_num, team1, team2, result1, result2, is_technical = match_data
                    if match_num > n:
                        break
                    update_team_stats(teams, team1, team2, result1, result2, is_technical)
                    match_counter += 1
        print_table(teams)
    except FileNotFoundError:
        print("Файл не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
