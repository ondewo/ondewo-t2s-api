from tritonclient.grpc import InferenceServerClient

from pylog.logger import logger_console as logger


def check_triton_online(triton_client: InferenceServerClient, triton_model_name: str) -> None:
    """Check if Triton server is active and the specified model is loaded.
    """
    if triton_client.is_server_ready() and triton_client.is_model_ready(triton_model_name):
        logger.info(f"Model {triton_model_name} is ready on Triton inference server.")
    else:
        error_text: str = f"Triton server is not ready for the inference of model {triton_model_name}."
        logger.error(error_text)
        raise RuntimeError(error_text)
