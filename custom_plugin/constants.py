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
# localStorage with expiration is from https://www.sohamkamani.com/javascript/localstorage-with-ttl-expiry/
JS_SCROLL_STR = """
<script>

    function setWithExpiry(key, value, ttl) {
        const now = new Date()

        // `item` is an object which contains the original value
        // as well as the time when it's supposed to expire
        const item = {
            value: value,
            expiry: now.getTime() + ttl,
        }
        localStorage.setItem(key, JSON.stringify(item))
    }

    function match_OS(href) {
        // absolute url
        const osmatch = href.match(/\/(Linux|macOS|Windows)\//i)
        if (osmatch !== null) {
            return osmatch[1]
        }
        return null
    }

    var buttons = Array.from(document.getElementsByClassName("md-button"))
    buttons.forEach(
        function (btn) {
            btn.addEventListener("click", function () {
                const osmatch = this.href.match(/^(.*?)\/(Linux|macOS|Windows)\//i)
                if (osmatch !== null) {
                    console.log("match this button OS onclick", osmatch)
                    setWithExpiry("select_OS", [osmatch[1], osmatch[2]], 12*3600*1000)  // TTL in ms
                }
                const hash = window.location.hash.substring(1)
                if (hash != 'force_select_OS') {
                    this.href = this.href + "#" + hash
                }
            })
        }
    )
</script>
"""

# loop over all
#    <a class="headerlink" from text
#    <a class="md-nav__link"> from index and TOC
# strip the OS from the href of all of them if the localstorage has select_OS defined
JS_OS_NEUTRAL = """
<script>
    if (!! localStorage.getItem('select_OS')) {
        const classes = ["headerlink", "md-nav__link"]
        for (i in classes) {
            var anchors = Array.from(document.getElementsByClassName(classes[i]))
            anchors.forEach(
                function (anch) {
                    console.log("i", i, "class", classes[i], "anch.href", anch.href)
                    if (!!anch.href) {
                        anch.href = anch.href.replace(/\/(Linux|macOS|Windows)\//i, "/")
                    }
                })
        }
    }
</script>
"""
