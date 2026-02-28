import json
import logging
from nba_game_predictor.statistics import Statistics

_LOGGER = logging.getLogger(__name__)
def test_get_team_ids_returns_list_of_dicts():
    statistics = Statistics()
    """ Use file w/ test json and loop through test cases and compare to expected results """

    with open ("tests/test_data/nba_teams.json", mode="r") as file:
        contents = file.read()

    data = json.loads(contents)
    if data is None:
        _LOGGER.warning("test_event(): Error with test file '%s'", "tests/test_data/nba_teams.json")
        assert False
    
    result = statistics.get_team_ids(data)
    
        # Assert
    assert isinstance(result, list)
    assert len(result) == 30
    assert {"Los Angeles Lakers": "13"} in result
    assert {"Boston Celtics": "2"} in result
    assert {"Golden State Warriors": "9"} in result
