# import requests
# from config.settings import settings
# from config.celery import celery_app
#
# @celery_app.task(
#     name='delete_task_scheduled',
#     bind=True,
#     max_retries=3,
#     default_retry_delay=5
# )
# def delete_task_scheduled(self, task_id, dell_key):
#     try:
#         response = requests.delete(f"{settings.celery_config.BROKER_URL}/delete/{task_id}/{dell_key}")
#         response.raise_for_status()
#         return response.status_code
#     except requests.RequestException as exc:
#         self.retry(exc=exc)
#     except Exception as e:
#         print(e)
