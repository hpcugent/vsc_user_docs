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

    function getWithExpiry(key) {
        const itemStr = localStorage.getItem(key)
        // if the item doesn't exist, return null
        if (!itemStr) {
            return null
        }
        const item = JSON.parse(itemStr)
        const now = new Date()
        // compare the expiry time of the item with the current time
        if (now.getTime() > item.expiry) {
            // If the item is expired, delete the item from storage
            // and return null
            localStorage.removeItem(key)
            return null
        }
        return item.value
    }

    function match_OS(href) {
        // absolute url
        const osmatch = href.match(/\/(Linux|macOS|Windows)\//i)
        if (osmatch !== null) {
            return osmatch[1]
        }
        return null
    }

    const store_OS = getWithExpiry("os-pick-OS");

    var buttons = Array.from(document.getElementsByClassName("md-button"))
    buttons.forEach(
        function (btn) {
            const osmatchbtn = match_OS(btn.href)
            if (osmatchbtn !== null) {
                //console.log("match button OS", osmatchbtn, "store_OS", store_OS)
                if (osmatchbtn == store_OS) {
                    //console.log("next go to ", btn.href + "#" + window.location.hash.substring(1))
                    window.location.href = btn.href + "#" + window.location.hash.substring(1)
                }
            }
            btn.addEventListener("click", function () {
                const osmatch = match_OS(this.href)
                if (osmatch !== null) {
                    //console.log("match this button OS onclick", osmatch)
                    setWithExpiry("os-pick-OS", osmatch, 12*3600*1000)  // TTL in ms
                }
                this.href = this.href + "#" + window.location.hash.substring(1)
            })
        }
    )
</script>
"""

# loop over all
#    <a class="headerlink" from text
#    <a class="md-nav__link"> from index and TOC
# strip the OS from the href of all of them if the localstorage has osneutral_links
# set to something that evaluates to true
JS_OS_NEUTRAL = """
<script>
    if (!! localStorage.getItem('osneutral_links')) {
        const classes = ["md-button", "md-nav__link"]
        for (i in classes) {
            var anchors = Array.from(document.getElementsByClassName(classes[i]))
            anchors.forEach(
                function (anch) {
                    if (!!anch.href) {
                        anch.href = anch.href.replace(/\/(Linux|macOS|Windows)\//i, "/")
                    }
                })
        }
    }
</script>
"""
