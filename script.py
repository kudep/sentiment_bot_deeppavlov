import logging
from typing import Optional, Union

from df_engine.core.keywords import GLOBAL, LOCAL, TRANSITIONS, RESPONSE
from df_engine.core import Context, Actor
import df_engine.conditions as cnd

from sentiment_analysis import *


logger = logging.getLogger(__name__)

script = {
    GLOBAL: {
        RESPONSE: '',
        TRANSITIONS: {
            ('main_flow', 'start_node'): cnd.exact_match('/start'),
            ('sentiment_analysis_flow', 'start_node'): cnd.exact_match('/is_positive'),
            ('main_flow', 'help_node'): cnd.true(),
        }
    },
    'main_flow': {
        'start_node': {
            RESPONSE: 'Write /start to get this message again.\n'
                      'Or /is_positive to get sentiment analysis of your text',
        },
        'help_node': {
            RESPONSE: '/start or /is_positive'
        },
        'fallback_node': {
            RESPONSE: 'Ooops'
        },
    },
    'sentiment_analysis_flow': {
        LOCAL: {
            TRANSITIONS: {
                ('main_flow', 'start_node'): cnd.exact_match('/quit'),
                'positive': condition_match(positive_sentiment),
                'negative': condition_match(negative_sentiment),
                'neutral': cnd.true(),
            },
        },
        'start_node': {
            RESPONSE: 'Write down your texts one by one.\n'
                      '/quit for quit',
        },
        'positive': {
            RESPONSE: 'Positive',
        },
        'negative': {
            RESPONSE: 'Negative',
        },
        'neutral': {
            RESPONSE: 'Neutral',
        }
    }
}

actor = Actor(
    script, start_label=('main_flow', 'start_node'),
    fallback_node=('main_flow', 'fallback_node')
)


def turn_handler(in_request: str, ctx: Union[Context, dict], actor: Actor):
    ctx = Context.cast(ctx)
    ctx.add_request(in_request)
    ctx = actor(ctx)
    out_response = ctx.last_response
    return out_response, ctx


if __name__ == '__main__':
    ctx = {}
    while True:
        in_request = input('type your answer: ')
        out_response, ctx = turn_handler(in_request, ctx, actor)
        print(out_response)
