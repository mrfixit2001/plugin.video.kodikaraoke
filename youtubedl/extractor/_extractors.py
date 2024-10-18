# flake8: noqa: F401
# isort: off

from .youtube import (  # Youtube is moved to the top to improve performance
    YoutubeIE,
    YoutubeClipIE,
    YoutubeFavouritesIE,
    YoutubeNotificationsIE,
    YoutubeHistoryIE,
    YoutubeTabIE,
    YoutubeLivestreamEmbedIE,
    YoutubePlaylistIE,
    YoutubeRecommendedIE,
    YoutubeSearchDateIE,
    YoutubeSearchIE,
    YoutubeSearchURLIE,
    YoutubeMusicSearchURLIE,
    YoutubeSubscriptionsIE,
    YoutubeTruncatedIDIE,
    YoutubeTruncatedURLIE,
    YoutubeYtBeIE,
    YoutubeYtUserIE,
    YoutubeWatchLaterIE,
    YoutubeShortsAudioPivotIE,
    YoutubeConsentRedirectIE,
)

# isort: on
from .commonmistakes import (
    BlobIE,
    CommonMistakesIE,
    UnicodeBOMIE,
)
from .commonprotocols import (
    MmsIE,
    RtmpIE,
    ViewSourceIE,
)
from .generic import GenericIE
