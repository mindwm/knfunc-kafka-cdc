import mindwm.model.graph as graph
from mindwm import logging
from mindwm.knfunc.decorators import Request, Response, app, event
from mindwm.model.events import (KafkaCdc, MindwmEvent, from_request,
                                 to_response)
import os

logger = logging.getLogger(__name__)

context_name = os.environ.get('CONTEXT_NAME', 'NO_CONTEXT')

@event
async def mindwm_cdc(obj: KafkaCdc, request: Request, response: Response):
    cdc_ev = await from_request(request)
    res = graph.GraphObjectChanged.from_kafka_cdc(cdc_ev.data)

    new_ev = MindwmEvent(
        source=f"org.mindwm.context.{context_name}.knfunc.kafka_cdc",
        subject=f"org.mindwm.context.{context_name}.graph.{cdc_ev.data.payload.type}",
        type=res.type,
        data=res,
        traceparent=res.obj.traceparent,
    )
    resp = to_response(new_ev)
    logger.info(f"Headers: {resp.headers}")
    logger.info(f"Body: {resp.body}")
    return resp
