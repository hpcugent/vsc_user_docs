#!/bin/bash

set -u

if [ -z ${1:-} ]; then
    echo "ERROR: Usage: $0 <directory>" >&2
    exit 1
fi
dir=${1:-}

if [ ! -d $dir ]; then
    echo "ERROR: Non-existing directory '$dir' specified" >&2
    exit 2
fi

# determine current version & checksum for specified directory
curr_version_line=$(grep '^\\LARGE Version' $dir/*.tex)
curr_version_file=$(echo $curr_version_line | cut -f1 -d:)
curr_version=$(echo $curr_version_line | cut -f2 -d: | cut -f3 -d' ')
if [ -z $curr_version ]; then
    echo "ERROR: Failed to determine current version for '$dir'" >&2
    exit 3
else
    echo "Current version for $dir: $curr_version (found in $curr_version_file)"
fi

travis_label=$(echo $dir | tr '[[:lower:]]' '[[:upper:]]' | tr '-' '_')
curr_checksum=$(grep "${travis_label}_EXPECTED=" .travis.yml | sed 's/.* \(.*\)"$/\1/g')
if [ -z $curr_checksum ]; then
    echo "ERROR: Failed to determine current checksum for '$dir'" >&2
    exit 4
else
    echo "Current checksum for $dir: $curr_checksum"
fi

# compute new checksum, to check whether current version/checksum is up-to-date
for checksum_tool_cand in sha256sum shasum;
do
    which $checksum_tool_cand > /dev/null
    if [ $? -eq 0 ]; then
        checksum_tool=$checksum_tool_cand
        break
    fi
done
if [ "x$checksum_tool" == "xshasum" ]; then
    checksum_tool="shasum -a 256"
fi

if [ -z $checksum_tool ]; then
    echo "ERROR: No checksum tool found!" >&2
    exit 4
fi

function compute_checksum() {
    tmpfile=$(mktemp /tmp/${USER}_XXXXX)
    find $1 -name '*.tex' | sort -u | xargs $checksum_tool > $tmpfile
    $checksum_tool $tmpfile | cut -f1 -d' '
    rm $tmpfile
}

new_checksum=$(compute_checksum $dir)
echo "Computed checksum for $dir: $new_checksum"

# check current and computed checksums
if [ "x$curr_checksum" == "x$new_checksum" ]; then
    echo "Checksum for $dir is still valid, no changes detected, version does not need to be bumped"
else
    echo "Mismatch between current and computed checksums for $dir, version need to be bumped..."
    datestamp=$(date +%Y%m%d)
    echo $curr_version | grep $datestamp > /dev/null
    if [ $? -eq 0 ]; then
        # if current datestamp matches in current version, we need to bump the 2-digit 'minor' version number...
        curr_minor_ver=$(echo $curr_version | cut -f2 -d.)
        if [ $curr_minor_ver -eq 99 ]; then
            echo "ERROR: Ran out of minor version numbers, found .99" >&2
            exit 5
        fi
        new_minor_ver=$(expr $curr_minor_ver + 1)
        new_version=${datestamp}.$(printf "%02d" ${new_minor_ver})
    else
        new_version="${datestamp}.01"
    fi

    echo "New version: $new_version"

    # inject new version
    sed -i.bak "s/Version ${curr_version}/Version ${new_version}/" $curr_version_file

    # need to recompute checksum after injecting new version...
    new_checksum=$(compute_checksum $dir)

    sed -i.bak "s/${travis_label}_EXPECTED=\".*\"/${travis_label}_EXPECTED=\"$new_version $new_checksum\"/g" .travis.yml

    rm ${curr_version_file}.bak .travis.yml.bak
fi
