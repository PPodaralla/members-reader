from members_reader.cli import main


def _write(tmp_path, text):
    p = tmp_path / "m.csv"
    p.write_text(text)
    return str(p)


def test_prints_sorted_names(tmp_path, capsys):
    path = _write(tmp_path, "first_name,last_name\nB,Zed\nA,Yan\n")
    assert main([path]) == 0
    assert capsys.readouterr().out.splitlines() == ["A Yan", "B Zed"]


def test_unsorted_keeps_file_order(tmp_path, capsys):
    path = _write(tmp_path, "first_name,last_name\nB,Zed\nA,Yan\n")
    assert main([path, "--unsorted"]) == 0
    assert capsys.readouterr().out.splitlines() == ["B Zed", "A Yan"]


def test_missing_file_returns_1(tmp_path, capsys):
    assert main([str(tmp_path / "nope.csv")]) == 1
    assert "file not found" in capsys.readouterr().err


def test_bad_header_returns_1(tmp_path, capsys):
    path = _write(tmp_path, "name\nA\n")
    assert main([path]) == 1
    assert "missing required column" in capsys.readouterr().err
