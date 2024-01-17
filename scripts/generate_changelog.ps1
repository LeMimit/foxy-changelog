
$version = $args[0]

if ($version.Length -eq 0) {
    Write-Host -ForegroundColor Red "You need to specify the version of the new release"
    exit
}

hatch run foxy-changelog --unreleased --latest-version "$version" --title "Foxy changelog" --description "A small program that will generate a changelog from git repos using ""conventional style"" commit messages "

Write-Host -ForegroundColor Green "Changelog generated"
