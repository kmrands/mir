# Creating Request Hooks

To add hooks to your API, you can use the `hook` command:

```
mir hook
```

## Default Hook Definition

This will prompt you for a `name`, for if the hook should be `pre-request` or `post-request`, for a method (i.e. `GET`, `PUT` etc), and optionally for a specific resource for which the hook should be run.

The code generated in `./hooks/<name>.py` should look something like the following, with `<name>` and `<resource>` replaced with your provided values:

```
from mir.lib.common import register_hook


@register_hook('on_pre_GET_<resource>')
def <name>(resource, request, lookup):
    pass
```

## Reusing Hooks Across Projects

As with resources, hooks can be installed from raw git URLs:

```
mir hook --url https://raw.githubusercontent.com/path/to/your/hook.py
```

## References

* [Eve Event Hooks](http://python-eve.org/features.html#eventhooks) _(note that all event hooks added in the `hooks` folder are automatically registered by Mir)_
