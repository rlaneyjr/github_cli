#!/usr/bin/env bash

# Example: ./scripts/github_user_clone.sh rlaneyjr
# Save our location before we start moving around
_pwd=$PWD
# Only variable we want is the username
_user=$1
# Capitalize the username first letter (directory name repos are stored)
_cap_user=${_user^}
# Capitalize the username completely
#_full_cap_user=${_user^^}
# Grab a list of the user's public repos (100 max)
repos=`gh_list $_user | grep html_url | sed 's:^.*\s::'`
# My personal directory for github users I am following (CHANGE IT!)
_gitfollowdir="/Volumes/T5-SSD/repos/Following"
_gituserdir="/Volumes/T5-SSD/repos/Following/$_cap_user"
if ! [[ -d $_gituserdir ]]
    then mkdir -p $_gituserdir && cd $_gituserdir
    else cd $_gituserdir
fi
# Iterate and clone each repo
for r in $repos; do
    git clone --recursive $r;
done
# Get us back where we started
cd $_pwd
exit 0
