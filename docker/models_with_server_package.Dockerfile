ARG ONDEWO_T2S_SERVER

FROM ${ONDEWO_T2S_SERVER}

ARG MODEL_DIR
ARG CONFIG_PATH

COPY ./${CONFIG_PATH} ./config/
COPY ./${MODEL_DIR}/ ./models/