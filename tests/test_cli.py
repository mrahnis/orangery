from click.testing import CliRunner

import orangery
from orangery.cli.cutfill import cutfill

def test_cutfill():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
