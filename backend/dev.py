import subprocess

GUNICORN_COMMANDS = (
    [
        "gunicorn",
        "-c",
        "app/gunicorn.conf.py",
        "runner:core_app",
        "-b",
        "localhost:3000",
    ],
)
FLASK_COMMANDS = (["uv", "run", "python3", "-u", "runner.py", "coreserver"],)


def get_argv(argv, i):
    try:
        return argv[i]
    except IndexError:
        return None


if __name__ == "__main__":
    import sys

    argv = sys.argv
    gunicorn = get_argv(argv, 1) == "gunicorn"
    proc1 = subprocess.Popen(GUNICORN_COMMANDS[0] if gunicorn else FLASK_COMMANDS[0])
    proc1.wait()
