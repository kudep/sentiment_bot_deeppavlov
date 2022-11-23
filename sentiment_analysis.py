from typing import Callable, Optional
from functools import partial

from df_engine.core import Context, Actor
from pydantic import validate_arguments

from transformers import AutoTokenizer, AutoModelForSequenceClassification

import numpy as np


MODEL = 'cardiffnlp/twitter-roberta-base-sentiment'

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

labels = {
    0: 'negative',
    1: 'neutral',
    2: 'positive',
}


def define_sentiment(text: str, sentiment: Optional[str]=None):
    input = tokenizer(text, return_tensors="pt")
    output = model(**input)
    scores = output[0][0].detach().numpy()
    pred = np.argmax(scores)

    if sentiment is None:
        return pred

    return labels[pred] == sentiment


positive_sentiment = partial(define_sentiment, sentiment='positive')
negative_sentiment = partial(define_sentiment, sentiment='negative')


@validate_arguments
def condition_match(condition: Callable, *args, **kwargs) -> Callable:
    """
    Returns function handler.
    This handler returns True if :py:func:`~condition` returns True
    Parameters
    ----------
    condition: Callable
        any :py:func:`~condition`
    """

    def condition_match_condition_handler(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
        request = ctx.last_request
        return condition(request)

    return condition_match_condition_handler


if __name__ == "__main__":
    pass
