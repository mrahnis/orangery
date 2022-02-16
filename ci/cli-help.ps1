<#
    Generate CLI help files from Click online help.
    These will get picked up by Sphinx.
 #>

$main = "orangery"
$commands = @(
    "adjust",
    "cutfill",
    "geodetic",
    "info",
    "section",
    "segment"
)

$dst = "$($PSScriptRoot)\..\docs\source\cli"
ForEach ($command in $commands)
{
    Write-Host "Writing help for $command"
    $path = Join-Path $dst cli.${command}.txt
    & $main ${command} --help | Out-File $path
}
