# git quick
new repo: `git init -b main && git add . && git commit -m "init"` · publish: `gh repo create <name> --public --source . --push`
branch: `git switch -c feat/x` · undo last commit keep changes: `git reset --soft HEAD~1`
find who/when: `git log -S "symbol" --oneline` · `git blame -L 10,30 file`
clean history view: `git log --oneline --graph -20` · tag: `git tag v1.0.0 && git push --tags`
