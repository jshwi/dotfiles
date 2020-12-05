# get git branch for Travis-CI
if git symbolic-ref --short HEAD >/dev/null 2>&1; then
  TRAVIS_BRANCH=$(git symbolic-ref --short HEAD)
else
  TRAVIS_BRANCH=
fi


export TRAVIS_BRANCH
