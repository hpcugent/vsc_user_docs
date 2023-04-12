# This string is used to generate OS picking files dynamically.
OS_PICK_STR = """---
hide:
  - navigation
  - toc
  - footer
---

# Please select your operating system:
"""

OS_PICK_BTN = """
{{%- if {} %}}
[{}]({}){{ .md-button }}
{{%- endif %}}
"""

# This string enables automatic scrolling to section on some page while using OS picking feature.
JS_SCROLL_STR = """
<script>
  var buttons = Array.from(document.getElementsByClassName("md-button"))
  buttons.forEach(
          function (btn) {
            btn.addEventListener("click", function () {
                var hash = window.location.hash.substring(1);
                this.href = this.href + "#" + hash
            })
          }
  )
</script>
"""
