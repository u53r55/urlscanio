import argparse
import itertools
import uuid
from typing import Dict, List, Tuple

import pytest

from ..context import utils

TEST_WEBSITE: str = "https://www.google.com"
TEST_UUID: uuid.UUID = uuid.uuid4()

TEST_FLAGS: Dict[str, str] = {
    "investigate": "-i {website}".format(website=TEST_WEBSITE),
    "submit": "-s {website}".format(website=TEST_WEBSITE),
    "retrieve": "-r {uuid}".format(uuid=TEST_UUID)
}

ALL_FLAG_COMBOS: List[Tuple[str, ...]] = \
    [combo for i in range(len(TEST_FLAGS) + 1)
     for combo in itertools.combinations(TEST_FLAGS.values(), i)]

ALL_SPLIT_FLAG_COMBOS: List[List[str]] = []
for combo in ALL_FLAG_COMBOS:
    split_flags: List[str] = []
    for flag in combo:
        split_flags += flag.split(" ")
    ALL_SPLIT_FLAG_COMBOS.append(split_flags)


@pytest.mark.parametrize("mock_flags", ALL_SPLIT_FLAG_COMBOS)
def test_create_arg_parser(mock_flags: List[str]) -> None:
    parser = utils.create_arg_parser()

    if " ".join(mock_flags) in TEST_FLAGS.values():
        args: Dict[str, str] = vars(parser.parse_args(mock_flags))
        for name, value in args.items():
            if args[name] is not None:
                assert TEST_FLAGS[name].split(" ")[1].strip() == \
                       value.strip()
    else:
        with pytest.raises(SystemExit):
            parser.parse_args(mock_flags)


MOCK_INVALID_URLS: Tuple[str, ...] = (
    "google.com",
    "www.google.com",
    "google",
    "https://google",
    "https://google.",
    "https://.google",
    "https://....google...."
)


@pytest.mark.parametrize("mock_invalid_url", MOCK_INVALID_URLS)
def test_is_url_valid_for_invalid_urls(mock_invalid_url: str) -> None:          # pylint: disable=C0103
    assert not utils.is_url_valid(mock_invalid_url)


@pytest.mark.parametrize("mock_flag", TEST_FLAGS.values())
def test_validate_arguments_with_valid_arguments(mock_flag: str) -> None:       # pylint: disable=C0103
    parser: argparse.ArgumentParser = utils.create_arg_parser()
    args: argparse.Namespace = parser.parse_args(mock_flag.split(" "))
    utils.validate_arguments(args)
