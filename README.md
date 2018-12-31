# Django Commander

Run Django `manage.py` commands from the web.

## Configuration

1. Add `commander` to your `INSTALLED_APPS`.
2. Add `COMMANDER_KEY` to your settings. This should be a reasonably secure key, which you'll use in lieu of real authentication 😱
3. `from commander import commander_urls` and add `path('commander/', commander_urls),` to your URLconf.
4. Navigate to `http://yourserver/yourapp/commander/?key={COMMANDER_KEY}`.
5. Do whatever config you need to do.
6. Change `COMMANDER_KEY` explicitly to `None` to disable management 😌

## Contributing

Contributions welcome. Be kind to one another.

To develop locally, first make a virtualenv.
Then cd into `dev/` and `pip install -e ../src`.
Then `pip install django` and off you go.

