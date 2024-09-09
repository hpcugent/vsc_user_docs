main() {
  local build_dir=$1

  local a_tag_regex='<a\s+[^>]*href="http[^"]*'

  # Generate links from build:
  # 1. Find all <a> tags in build, H option to print filename (/path/to/file:<a href="url)
  # 2. convert middle part to space (/path/to/file url)                     ^^^^^^^^^^ -> ' '
  # 3. sort by url
  # 4. remove duplicates (only based on url)
  grep -rHoP "$a_tag_regex" "$build_dir" \
      | sed 's/:<a.*href="/ /' \
      | sort -k2,2 \
      | uniq -f1

  # Output is in format: /path/to/file url with no duplicate urls
}

main "$1"