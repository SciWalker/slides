# slides
### This is my repo for slides, done mainly using reveal.js framework

Create a feature branch from the develop branch and work on your feature. For example:
```
git checkout develop
git branch feature_branch
git checkout feature_branch
#...develop some code...
git add .
git commit -m "Some commit message"
```
When the feature is done, finish the feature branch and merge it back to develop. For example:
```
git checkout develop
git merge feature_branch
git branch -d feature_branch
```
## git flow release
Use the git flow release start command to create the release branch from develop. For example:
```
git flow release start 1.0.0
```
This will create a new branch named release/1.0.0 and switch to it. You can make any final changes or fixes on this branch before releasing it.

Use the git flow release finish command to merge the release branch to master and develop, and tag the release with its name. For example:
```
git flow release finish 1.0.0
```
This will merge release/1.0.0 to both master and develop, delete the release branch, and create a tag named 1.0.0.
## Finalizing a release
Push the master, develop, and tag to the remote repository. For example:
```
git push origin main
git push origin develop
git push origin 1.0.x
```
Now you have successfully merged your feature branch to release-1.0 and then to master using the Gitflow Workflow.
