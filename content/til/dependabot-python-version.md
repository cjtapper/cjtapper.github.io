Title: How to configure dependabot python version
Date: 2022-11-10

I've recently configured dependabot for some of my personal projects to get automated pull requests opened for updates to my dependencies.
This is nice because it means I can review these PRs one-by-one and confirm that my tests are still passing for each individual dependency upgrade.

I ran into some issues though with dependabot misidentifying some dependencies and excluding them from the new version of my requirements.txt file that it was generating.
In my case, all of the automated PRs had removed `tomli` from my requirements file.


It turns out that by default, dependabot uses the latest version of Python defined in [this file](https://www.b-list.org/weblog/2022/may/13/boring-python-dependencies)--in this case, the newly released Python 3.11.0.
In case you are unaware, Python 3.11 added support for parsing TOML files to the standard library (see: `[tomlib](https://docs.python.org/3/library/tomllib.html)`).
Because of this, some packages (in my case, `black`, `pytest`, and `coverage`) have removed their dependency on `tomli` when installed into a Python 3.11 environment.


At this point in time my projects are still running on Python 3.10.x--I don't like upgrading to the latest version until the first point release (at the very minimum) as there are often bugs or incompatibilities with third party packages.
So dependabot was opening PRs with the `tomli` dependency removed, then attempting to run the CI pipeline in a Python 3.10 environment, which would quickly fail because of the lack of TOML support.


The fix for this is to specify the version of Python that dependabot should use when resolving dependencies.
I struggled to find this any of the dependabot documentation, but stumbled upon a couple of Github issues that were very helpful:
- https://github.com/dependabot/dependabot-core/issues/4062
- https://github.com/dependabot/dependabot-core/issues/1455


It turns out that there are multiple ways to configure the Python version for dependabot, most of which I believe are not suitable:
- Specifying it in a `Pipfile`. I don't use `pipenv`, so I don't want to have to add a `Pipfile` to my repositories.
- `python_requires = "x.x.x"` in `setup.py`. I don't have a `setup.py` either, and have no desire to add one because most of my projects are Django projects, not publishable packages.
- Specifying it in `pyproject.toml`. I think this is the least offensive of the above. I already have a `pyproject.toml` in my repositories for configuration purposes. However, it seems that they chose to rely on `poetry` specific configuration for this, and it seems silly to add it just for this. 
- Specifying it in `.python-version`. Unfortunately this interferes with `pyenv`s usage of this file, so it's a no-go for me.

The least offensive option in my opinion is to use `runtime.txt`.
This file was originally used by Heroku for specifying which Python runtime to use on their PaaS.
I'm not using Heroku at this point in time, so there's no chance of this interfering with anything else.


So for now, I've added a `runtime.txt` to my repositories with the following:

    python-3.10.7

This gets picked up by dependabot, and has no unintended side-effects.


I do wish there was a better way to do this - currently I have to independently specify the Python version in my Dockerfiles, Github actions, pre-commit config, etc.
Maybe I should just write a script to do this!

https://github.com/dependabot/dependabot-core/blob/00f0e52b630af6d55318951e8cb21a9a32eabbb7/python%2Flib%2Fdependabot%2Fpython%2Ffile_parser%2Fpython_requirement_parser.rb
