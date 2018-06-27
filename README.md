# Popper Badge Server

This is a RESTful API server built with Flask used for serving badges,
specific to popper.


### Endpoints:

1. `/:org/:repo`:
    1. **GET**: Get the badge image for the org/repo (can be used to obtain
    the badge image used in the README of the popperized repository)
    2. **POST**: Create a record on the server for the org/repo with the
    commit_id, timestamp and the status of `popper run` command
    (will be triggered by a CI service)
2. `/:org/:repo/list`: List all the status records of the org/repo,
sorted by timestamp. Provides the `commit_id` and the `status`.


### For development:

1. Clone the repository with `git clone
https://github.com/popperized/popper-badge-server.git`.
2. Create and activate a virtual environment (recommended, but not necessary).
3. Run `pip install -r requirements.txt` to install all the dependencies.
4. Run `python main.py` to run the development server.