import bleach

dirty_html = '<script>alert("XSS")</script><p>This is a paragraph.</p><font>ddd</font>'
clean_html = bleach.clean(dirty_html, tags = {'font'})

print(clean_html)
