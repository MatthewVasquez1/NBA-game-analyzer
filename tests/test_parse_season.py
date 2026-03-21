import json
import logging
from nba_game_predictor.statistics import Statistics

_LOGGER = logging.getLogger(__name__)
def test_parse_season_returns_list_of_dicts():
    statistics = Statistics()
    """ Use file w/ test json and loop through test cases and compare to expected results """

    with open ("tests/test_data/nba_schedule.json", mode="r") as file:
        contents = file.read()

    data = json.loads(contents)
    if data is None:
        _LOGGER.warning("test_event(): Error with test file '%s'", "tests/test_data/nba_schedule.json")
        assert False
    
    result = statistics.parse_season(data)
    
        # Assert list with 82 games with first, last, and middle game ids
    assert isinstance(result, list)
    assert len(result) == 82
    assert "2025-26" == result[0]
    assert "2025-26" == result[41]
    assert "2025-26" == result[81]