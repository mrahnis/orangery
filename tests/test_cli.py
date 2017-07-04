from click.testing import CliRunner

import orangery
from orangery.cli.orangery import cli

def test_orangery():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
