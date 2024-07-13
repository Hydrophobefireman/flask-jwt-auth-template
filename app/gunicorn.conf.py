def when_ready(server):
    # touch app-initialized when ready
    try:
        open("/tmp/app-initialized", "w").close()
    except:
        pass


bind = "0.0.0.0:8080"
workers = 4
threads = 4
max_requests = 1200
max_requests_jitter = 10
timeout = 500
