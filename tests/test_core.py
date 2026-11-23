import pytest

from members_reader import (
    Member,
    MissingColumnsError,
    read_members,
    sort_members,
)

CSV = (
    "id,first_name,last_name,email,gender,ip_address\n"
    "1,Zed,adams,z@x.com,Male,1.1.1.1\n"
    "2,Amy,Baker,a@x.com,Female,2.2.2.2\n"
    "3,Al,Adams,al@x.com,Male,3.3.3.3\n"
)


@pytest.fixture
def csv_file(tmp_path):
    p = tmp_path / "members.csv"
    p.write_text(CSV, encoding="utf-8")
    return p


def test_read_members_parses_all_columns(csv_file):
    members = read_members(csv_file)
    assert len(members) == 3
    assert members[0] == Member(
        first_name="Zed",
        last_name="adams",
        id="1",
        email="z@x.com",
        gender="Male",
        ip_address="1.1.1.1",
    )


def test_read_members_accepts_str_path(csv_file):
    assert len(read_members(str(csv_file))) == 3


def test_optional_columns_default_to_none(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text("first_name,last_name\nA,B\n")
    assert read_members(p) == [Member(first_name="A", last_name="B")]


def test_full_name():
    assert Member("Ada", "Lovelace").full_name == "Ada Lovelace"


def test_sort_is_case_insensitive_and_breaks_ties_by_first_name(csv_file):
    names = [m.full_name for m in sort_members(read_members(csv_file))]
    assert names == ["Al Adams", "Zed adams", "Amy Baker"]


def test_sort_does_not_mutate_input(csv_file):
    members = read_members(csv_file)
    before = list(members)
    sort_members(members)
    assert members == before


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_members(tmp_path / "nope.csv")


def test_missing_column_raises(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("first_name,email\nA,a@x.com\n")
    with pytest.raises(MissingColumnsError) as exc:
        read_members(p)
    assert exc.value.missing == ("last_name",)


def test_empty_file_raises(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("")
    with pytest.raises(MissingColumnsError):
        read_members(p)
