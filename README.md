# Library to navigate jw org website via script

## Usage

Add to you pyproject.toml

```
dependencies = [
    "jw_page_navigation @ git+https://github.com/allofmex/jw_page_navigation@v0.1.3",
    "selenium",
    "markdown",
]
```

Use as

```
from AccountsPageNavigatior import AccountsPageNavigatior

targetNav = AccountsPageNavigatior(self.config.get(Config.BROWSER_PROFILE_DIR))
await targetNav.navigateToHub()
await targetNav.navAccounting()
await targetNav.navAccount('Account label')
await targetNav.navMonth('January')
```


## Development

To help extending this tool, you may start like this

```
apt install python3-venv
python3 -m venv ~/jw_nav_venv
# or if python was upgraded: 
#(python3 -m venv --upgrade ~/jw_nav_venv)

source ~/jw_nav_venv/bin/activate

pip3 install .
# or pip3 install --editable . (for development if this package)
python example.py
```

