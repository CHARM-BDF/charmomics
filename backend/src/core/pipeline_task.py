"""  """

# from .tasks.ditto_precompute_filter import DittoPrecomputedFilter

from abc import abstractmethod
import subprocess

class PipelineTaskInterface:
    def __init__(self):
        return

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    def aggregate_string_replacements(self, command, dependencies, attributes) -> str:
        built_commmand = command

        for dependency in dependencies:
            dependency_string = f"{{{dependency}}}"
            print(dependency_string)
            built_commmand = built_commmand.replace(
                dependency_string, str(attributes[dependency])
            )

        return built_commmand

class SubprocessTask(PipelineTaskInterface):
    """  """
    
    def __init__(self, task):
        """  """
        self.task = task

    def execute(self, attributes):
        """  """
        command = self.aggregate_string_replacements(self.task['command'], self.task['dependencies'], attributes)

        # subprocess.run(self.command, capture_output=True, text=True)
        print(command)
        subprocess.run(command, shell=True, text=True)

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
