# import os
# import subprocess
# import time
# from typing import Dict, Optional, List

# import tensorflow as tf
# from GPUtil import GPUtil
# from ondewologging.logger import logger_console as log

# from ondewo_cdls.utils.gpu_utils_constants import GPU_AVAILABLE_TIME_S, GPU_POLLING_STEP_S, NVIDIA_SMI, \
#     GPU_MEMORY_BUFFER, TF_GPU_MEMORY_MARGIN
# from ondewo_cdls.utils.gpu_utils_dataclasses import GPUProcess


# def preallocate_gpu_memory(
#     gpu_memory_limit_by_id: Dict[int, Optional[float]],
#     gpu_preallocation_time_s: float = 0.0,
# ) -> None:
#     """ Pre-allocate required GPU resources by running a dummy tensorflow command

#     Args:
#         gpu_memory_limit_by_id: mapping of GPU ids to the memory limit in MB to be set
#         gpu_preallocation_time_s: how long should the specified GPUs stay pre-allocated
#     """
#     # get all physical devices visible to the runtime
#     physical_devices = tf.config.list_physical_devices('GPU')
#     # pick the subset of physical devices
#     visible_devices = [physical_devices[gpu_id] for gpu_id in gpu_memory_limit_by_id.keys()]
#     # make visible this subset only
#     tf.config.experimental.set_visible_devices(visible_devices, 'GPU')
#     # for each visible device specify virtual device configuration (memory limit)
#     for gpu_id, gpu_memory_limit in gpu_memory_limit_by_id.items():
#         gpu_memory_limit_tf: Optional[float] = max(gpu_memory_limit - TF_GPU_MEMORY_MARGIN, 0) \
#             if gpu_memory_limit else None
#         tf.config.experimental.set_virtual_device_configuration(
#             device=physical_devices[gpu_id],
#             logical_devices=[
#                 tf.config.experimental.VirtualDeviceConfiguration(memory_limit=gpu_memory_limit_tf)
#             ]
#         )
#     with setup_strategy(num_gpus=len(gpu_memory_limit_by_id)).scope():
#         # run a dummy tf command
#         tf.Variable(1)

#     if gpu_preallocation_time_s:
#         # preallocate for specified amount of time
#         time.sleep(gpu_preallocation_time_s)


# def get_gpu_memory_limit_by_id(
#     gpus: Optional[List[GPUtil.GPU]] = None,
#     num_gpus: Optional[int] = None,
#     per_process_gpu_memory_mb: Optional[float] = None,
#     gpu_memory_buffer: float = GPU_MEMORY_BUFFER,
# ) -> Dict[int, Optional[float]]:
#     """ Choose a subset of GPUs from the pool with the corresponding memory limit in MB to set for them.

#     Args:
#         gpus: optional list of GPUs, if None, GPUtil.getGPUs() is used to detect them
#         num_gpus: number of GPUs to use, if None, use all from the pool
#         per_process_gpu_memory_mb: memory in MB to allocate on each GPU, if None, allocate all the memory
#         gpu_memory_buffer: if another process is already running on a GPU, the real available GPU memory is
#             decreased by this proportion to lower the risk of out of memory errors

#     Returns:
#         mapping of GPU ids to memory limit in MB to set for them
#     """
#     min_required_memory_mb: float = per_process_gpu_memory_mb or 0.0
#     min_required_num_gpus: int = num_gpus or 1

#     if gpus is None:
#         gpus = GPUtil.getGPUs()

#     available_gpus: List[GPUtil.GPU] = []
#     pid: int = os.getpid()
#     for gpu in gpus:
#         gpu_memory_free: float = float(gpu.memoryFree)
#         if gpu_memory_buffer > 0.0:
#             # if the buffer is applied, decrease the free memory
#             other_gpu_processes: List[GPUProcess] = [
#                 proc for proc in get_processes_for_gpu(gpu_id=gpu.id) if proc.pid != pid
#             ]
#             if len(other_gpu_processes):
#                 # if some processes already run on the gpu, decrease the available gpu memory by 10% buffer
#                 gpu_memory_free -= gpu.memoryTotal * gpu_memory_buffer
#         if gpu_memory_free >= min_required_memory_mb:
#             available_gpus.append(gpu)
#     available_num_gpus: int = len(available_gpus)
#     if available_num_gpus < min_required_num_gpus:
#         log.warning(f'Not enough GPUs currently available with free memory >= {min_required_memory_mb} MB. '
#                     f'Required {min_required_num_gpus}, found {available_num_gpus}.')
#         return {}

#     available_gpus.sort(key=lambda gpu: gpu.memoryFree, reverse=True)

#     # take only first num_gpus GPUs
#     if num_gpus is not None:
#         available_gpus = available_gpus[:num_gpus]

#     return {gpu.id: per_process_gpu_memory_mb for gpu in available_gpus}


# def get_available_gpu_memory_limit_by_id(
#     num_gpus: Optional[int] = None,
#     per_process_gpu_memory_mb: Optional[float] = None,
#     gpu_available_time_s: float = GPU_AVAILABLE_TIME_S,
#     gpu_polling_step_s: float = GPU_POLLING_STEP_S,
# ) -> Dict[int, Optional[float]]:
#     """ Choose a subset of currently available GPUs with the corresponding memory limit in MB to set for them.

#     NOTE: The GPUs must be available at least gpu_available_time_s (10) seconds.
#     NOTE: If another process is already running on a GPU, the real available GPU memory is decreased by 10%
#         buffer to lower the risk of out of memory errors

#     Args:
#         num_gpus: number of GPUs to use, if None, use all from the pool
#         per_process_gpu_memory_mb: memory in MB to allocate on each GPU, if None, allocate all the memory
#         gpu_available_time_s: GPU memory must be available at least gpu_available_time_s seconds
#         gpu_polling_step_s: how often to check if the GPU memory is still available

#     Returns:
#         mapping of GPU ids to memory limit in MB to set for them
#     """
#     gpu_memory_limit_by_id: Dict[int, Optional[float]] = {}
#     start_time: float = time.time()
#     while time.time() - start_time < gpu_available_time_s:
#         gpu_memory_limit_by_id = get_gpu_memory_limit_by_id(
#             num_gpus=num_gpus,
#             per_process_gpu_memory_mb=per_process_gpu_memory_mb,
#         )
#         if not gpu_memory_limit_by_id:
#             # if the GPU memory is not available, do not check further
#             break
#         # GPU memory is available, wait 1 s before the next check
#         time.sleep(gpu_polling_step_s)
#     return gpu_memory_limit_by_id


# def get_processes_for_gpu(gpu_id: int) -> List[GPUProcess]:
#     """ Get list of processes currently running computation on the GPU with specified id.

#     The information is retrieved by calling command

#     nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv,noheader,nounits \
#         --id=<gpu_id>

#     Args:
#         gpu_id: 0-indexed GPU id

#     Returns:
#         list of GPUProcess objects
#     """
#     command: List[str] = [NVIDIA_SMI, '--query-compute-apps=pid,process_name,used_gpu_memory',
#                           '--format=csv,noheader,nounits', f'--id={gpu_id}']
#     try:
#         p = subprocess.Popen(command, stdout=subprocess.PIPE)
#         stdout, stderr = p.communicate()
#     except FileNotFoundError as e:
#         log.warning(e)
#         return []
#     output: str = stdout.decode('utf-8')
#     if output == 'No devices were found\n':
#         log.warning(output.strip())
#         return []
#     processes: List[GPUProcess] = []
#     for line in output.splitlines():
#         pid, name, used_gpu_memory_mb = line.replace(' ', '').split(',')
#         processes.append(GPUProcess(pid=int(pid), name=name, used_gpu_memory_mb=int(used_gpu_memory_mb)))
#     log.debug(f'Processes running on GPU {gpu_id}: {processes}')
#     return processes


# def set_memory_growth() -> None:
#     """ Used in TensorFlow algorithms to avoid CUDNN_STATUS_INTERNAL_ERROR error while training/inferencing
#         without limiting/allowing growth of the memory
#     """
#     try:
#         for physical_device in tf.config.list_physical_devices('GPU'):
#             tf.config.experimental.set_memory_growth(physical_device, True)
#     except RuntimeError as e:
#         # Cannot set memory growth on device when virtual devices configured
#         log.warning(e)


# def setup_strategy(num_gpus: int = 0) -> tf.distribute.Strategy:
#     """ Set up a distribute strategy for tensorflow.

#     Typical use:
#         with strategy.scope():
#             keras_model.compile()

#     Args:
#         num_gpus: number of GPUs to use

#     Returns:
#         distribute strategy

#     Raises:
#         ValueError: if invalid number of GPUs is provided
#     """
#     if num_gpus == 0:
#         strategy: tf.distribute.Strategy = tf.distribute.OneDeviceStrategy(device='/cpu:0')
#         devices_str: str = 'CPU'
#     elif num_gpus == 1:
#         strategy = tf.distribute.OneDeviceStrategy(device='/gpu:0')
#         devices_str = 'GPU'
#     elif num_gpus > 1:
#         strategy = tf.distribute.MirroredStrategy()
#         devices_str = f'{strategy.num_replicas_in_sync} GPUs'
#     else:
#         raise ValueError(f'Invalid number of GPUs {num_gpus} for a strategy. Expected >= 0.')

#     log.info(f'Using {strategy} on {devices_str} ')
#     return strategy
