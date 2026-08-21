class PipelineUnit:
    def __init__(self):
        self.tasks = []
    
    def execute_current_task(self):
        task = self.tasks.pop(0)
        try:
            task.execute()
            print()
        except Exception as e:
            print(e)

    def tasks_left(self):
        return False if len(self.tasks) == 0 else True
