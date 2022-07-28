from celery import Celery


def make_celery(app_name='celery_config'):
    # backend = "redis://localhost:6379"
    # broker = "redis://localhost:6379"
    #
    #
    # print(f"APP NAME {app_name}")
    #
    # return Celery(app_name, backend=backend, broker=broker)

    celery = Celery(
        app_name,
        backend="redis://localhost:6379",
        broker="redis://localhost:6379"
    )
    # celery.conf.update(app_name.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app_name.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
celery = make_celery()
print(celery,"sdasdjajkdajsdhjkasd")