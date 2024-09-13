# Description: Common regex used in the parser

import re


PARENT_LINE_REGEX = re.compile(r"^(\w+.*)")
CHILDREN_LINE_REGEX = re.compile(r"^\s(.*)$")
CHILDREN_WITH_1_SPACE_REGEX = re.compile(r"\s.*")
CHILDREN_WITH_2_SPACE_REGEX = re.compile(r"\s{2}.*")
CHILDREN_WITH_3_SPACE_REGEX = re.compile(r"\s{3}.*")
CHILDREN_WITH_4_SPACE_REGEX = re.compile(r"\s{4}.*")
CHILDREN_WITH_5_SPACE_REGEX = re.compile(r"\s{5}.*")

SPLIT_ON_BANG_MULTILINE = re.compile(r"^!", flags=re.MULTILINE)
SPLIT_ON_SECOND_BANG_MULTILINE = re.compile(r"\s!$", flags=re.MULTILINE)
SPLIT_ON_FIRST_BANG_MULTILINE = re.compile(r"^!$", flags=re.MULTILINE)
SPLIT_ON_LINE = re.compile(r"\n")
SPLIT_ON_LINE_MULTILINE = re.compile(r"\n", flags=re.MULTILINE)