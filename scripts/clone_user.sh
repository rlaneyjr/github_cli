#!/usr/bin/env bash

# Example: ./scripts/clone_user.sh rlaneyjr

_user=$1
_cap_user=${_user^}
_full_cap_user=${_user^^}
_pwd=$PWD
repos=`gh_list $_user | grep html_url | sed 's:^.*\s::'`
cd /Volumes/T5-SSD/repos/Following && mkdir -p $_cap_user && cd $_cap_user
for r in $repos; do
    git clone --recursive $r;
done
cd $_pwd
exit 0
