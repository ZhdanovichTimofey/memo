from src.worker.worker import Worker
from threading import Thread

class Scheduler():
    def __init__(self, model) -> None:
        self.workers = []
        self.model = model

    def add(self, task):
        '''
        Adds worker to scheduler
        '''
        worker = Worker(task, self.model)
        self.update()
        self.workers.append(worker)
        thread = Thread(target=worker.run)
        thread.start()

    def queue_count(self):
        return len(self.get_active_workers())
    
    def get_active_workers(self):
        return [worker for worker in self.workers if worker.is_running]
    
    def update(self):
        for i, worker in enumerate(self.workers):
            if not worker.is_running:
                self.workers.pop(i)
        return len(self.workers)