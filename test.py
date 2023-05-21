"""Used for automated testing purposes.

Author: jon-chow
Created: 2023-05-19
Last Modified: 2023-05-21
"""

import json
import os
import colorama
from colorama import Fore, Back, Style

from utils.scraper import scrape

from utils.scrapers.artifacts import get_all_artifact_names
from utils.scrapers.characters import get_all_character_names
from utils.scrapers.weapons import get_all_weapon_names


colorama.init(autoreset=True)

TESTS_DIR = "tests"

# ---------------------------------------------------------------------------- #
#                                   FUNCTIONS                                  #
# ---------------------------------------------------------------------------- #
def test_get_all_names(test_function, expected):
  """Tests retrieving all names for a given test function."""
  try:
    actual = test_function()
    actual = actual[:1] + actual[-1:]
    assert (actual == expected)
    print(f"{Fore.GREEN}Test {test_function.__name__}() passed!")
    return True
  except Exception as e:
    print(f"{Fore.RED}Test {test_function.__name__}() failed!")
    return False


def test_scrape(category="characters", query="amber"):
  """Tests scraping data from category."""
  expected = json.load(open(f"{TESTS_DIR}/{category}/ex_{query}.json", "r"))
  try:
    query = query.replace("-", " ").title()
    actual = scrape(category=category, query=query)
    assert (actual == expected)
    print(f"{Fore.GREEN}Test scrape() for {Fore.YELLOW}{query.title()} {Fore.GREEN}passed!")
    return True
  except Exception as e:
    # print(f"{Fore.CYAN}{json.dumps(actual, indent=2)}")
    print(f"{Fore.RED}Test scrape() for {Fore.YELLOW}{query.capitalize()} {Fore.RED}failed!")
    return False

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def test():
  """Main function for testing."""
  progress = { "passes": 0, "fails": 0 }
  
  def passed():
    """Increments the number of passed tests."""
    progress['passes'] += 1

  def failed():
    """Increments the number of failed tests."""
    progress['fails'] += 1
  
  print(f"{Fore.CYAN}\nTesting getting all names of items...")
  FUNCTIONS_TO_TEST = [
    {
      "function": get_all_artifact_names,
      "expected": ["Adventurer", "Vourukasha's Glow"]
    },
    {
      "function": get_all_character_names,
      "expected": ["Albedo", "Zhongli"]
    },
    {
      "function": get_all_weapon_names,
      "expected": ["A Thousand Floating Dreams", "Waster Greatsword"]
    },
  ]
  for test in FUNCTIONS_TO_TEST:
    if test_get_all_names(test_function=test['function'], expected=test['expected']):
      passed()
    else:
      failed()
  
  # Testing: scrape().
  folders = os.listdir(TESTS_DIR)
  for file in folders:
    category = file
    print(f"{Fore.CYAN}\nTesting {category} scraper...")
    for file in os.listdir(f"{TESTS_DIR}/{category}"):
      if file.startswith("ex_"):
        query = file[3:-5]
        if test_scrape(category=category, query=query):
          passed()
        else:
          failed()
  
  return progress

if __name__ == "__main__":
  results = test()
  if results['fails'] == 0:
    print(f"{Fore.CYAN}\nSUMMARY: All {results['passes'] + results['fails']} tests passed!")
  else:
    print(f"{Fore.CYAN}\nSUMMARY: {results['passes']} / {results['passes'] + results['fails']} tests passed!")
