"""  """

# from .tasks.ditto_precompute_filter import DittoPrecomputedFilter

from abc import abstractmethod
import subprocess

class PipelineTaskInterface:
    def __init__(self):
        return
    
    @abstractmethod
    def run(self):
        raise NotImplementedError()

class SubprocessTask(PipelineTaskInterface):
    """  """
    
    def __init__(self, task):
        """  """
        
        self.command = task['command']

    def execute(self):
        """  """
        # subprocess.run(self.command, capture_output=True, text=True)
        subprocess.call(self.command, text=True)

# class DittoPrecomputedFilterTask(PipelineTaskInterface):
#     """  """

#     def __init__(self, task):
#         """  """

#         self.ditto_task = DittoPrecomputedFilter(task['input_path'], task['output_path'], task['batch_size'])

#         return

#     def execute(self):
#         """  """

#         self.ditto_task.run()

#         return

class PipelineTaskFactory():
    """  """
    
    tasks = {
        # "ditto_precomputed_filter": DittoPrecomputedFilterTask,
        "subprocess": SubprocessTask
    }

    @classmethod
    def create_pipeline_task(cls, pipeline_task):
        """  """
        
        pipeline_task_type = pipeline_task['type']
        
        return cls.tasks[pipeline_task_type](pipeline_task)
