from mindwm import logging
from mindwm.knfunc.decorators import kafka_cdc, app

logger = logging.getLogger(__name__)

@kafka_cdc
async def func(event):
    logger.info(f"event: {event}")
    return event.data
