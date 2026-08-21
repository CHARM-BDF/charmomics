import concurrent.futures

from .pipeline_unit import PipelineUnit
from .pipeline_task import PipelineTaskFactory

class PipelineService():
    def __init__(self, pipeline_queue):
        """  """
        self.queue = pipeline_queue
        
        return
    
    def queue_pipeline_tasks(self, json):
        """  """
        pipeline_unit = PipelineUnit()

        for task in json:
            new_task = PipelineTaskFactory.create_pipeline_task(task)
            pipeline_unit.tasks.append(new_task)
        
        self.queue.put(pipeline_unit)

    def process_tasks(self):
        try:
            while not self.queue.empty():
                pipeline_unit = self.queue.get()
                pipeline_unit.execute_current_task()
                
                if pipeline_unit.tasks_left():
                    self.queue.put(pipeline_unit)
        except Exception as e:
            logger.info(f"MAIN :: EXCEPTION :: {e}")