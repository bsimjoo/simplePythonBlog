# Blogger
This is a simple python blog server using cherrypy.

## variables:
You can use variables in html template like this [::variable name] and also you can change variables value in configuration

## foreach:
You can create repeatable template codes for posts and any other things like this:

``` html
[::foreach post]
<div class="post">
    <h1 class="header">
        [::header]
    </h1>
    <div class='postContent'>
        [::content]
    </div>
</div>
[::end]
```

**foreach syntax:** [::foreach source] in server codes source must return a dictionary of variables. (for more information see source code!)