#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# vim: noai:et:tw=80:ts=2:ss=2:sts=2:sw=2:ft=bash

# Example: ./scripts/github_user_clone.sh rlaneyjr
# Save our location before we start moving around
_pwd="$PWD"

if [[ "$#" == 2 ]]
then
  if [[ "$2" =~ \/+ ]]
  then
    # First variable must be the username
    _user="$1"
    _gitfollowdir="$2"
  elif [[ "$1" =~ \/+ ]]
  then
    # First variable must be the dir
    _user="$2"
    _gitfollowdir="$1"
  fi
else
  _user="$@"
  # My personal directory for github users I am following (CHANGE IT!)
  _gitfollowdir="/Volumes/T5-SSD/repos/Following"
fi
# Capitalize the username first letter (directory name repos are stored)
_cap_user=${_user^}
# Capitalize the username completely
_full_cap_user=${_user^^}
# Grab a list of the user's public repos (100 max)
repos=$(gh_list $_user | grep html_url | sed 's:^.*\s::')
_gituserdir="$_gitfollowdir/$_cap_user"

if [[ ${#repos} > 0 ]]
then
  if ! [[ -d $_gituserdir ]]
  then
    mkdir -p $_gituserdir && cd $_gituserdir
  else
    cd $_gituserdir
  fi
  echo "GitUserDir: $_gituserdir"
  # Iterate and clone each repo
  _count=0
  for r in $repos
  do
    echo "Cloning: $r"
    git clone --recursive $r;
    ((_count++))
  done
  echo "Cloned $_count repos"
  # Get us back where we started
  cd $_pwd && echo "Done!"
  exit 0
else
  echo "ERROR: Repos = $repos\nUser = $_user\nGitUserDir = $_gituserdir"
  exit 1
fi

