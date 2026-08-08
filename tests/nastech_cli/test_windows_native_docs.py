from pathlib import Path


def test_windows_native_install_path_docs_match_installer() -> None:
    doc = Path("website/docs/user-guide/windows-native.md").read_text()
    install = Path("scripts/install.ps1").read_text()

    assert "%LOCALAPPDATA%\\nastech\\nastech-agent\\venv\\Scripts" in doc
    assert "Get-Command nastech        # should print C:\\Users\\<you>\\AppData\\Local\\nastech\\nastech-agent\\venv\\Scripts\\nastech.exe" in doc
    assert '$nastechBin = "$InstallDir\\venv\\Scripts"' in install
