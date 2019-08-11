from __future__ import annotations

import datetime
import io
from enum import Enum
from typing import List, Optional, Union, TypeVar, Any

from pydantic import BaseModel, Schema

InputFile = TypeVar('InputFile', io.BytesIO, io.FileIO, str)


class InlineKeyboardButton(BaseModel):
    """
    This object represents one button of an inline keyboard. You must use exactly one of the optional fields.
    https://core.telegram.org/bots/api#inlinekeyboardbutton
    """
    text: str = None
    url: str = None
    login_url: 'LoginUrl' = None
    callback_data: str = None
    switch_inline_query: str = None
    switch_inline_query_current_chat: str = None
    callback_game: 'CallbackGame' = None
    pay: bool = None

    def __init__(self, text: str,
                 url: str = None,
                 login_url

                 : 'LoginUrl' = None,
                 callback_data: str = None,
                 switch_inline_query: str = None,
                 switch_inline_query_current_chat: str = None,
                 callback_game: 'CallbackGame' = None,
                 pay: bool = None, **kwargs):
        super(InlineKeyboardButton, self).__init__(text=text,
                                                   url=url,
                                                   login_url=login_url,
                                                   callback_data=callback_data,
                                                   switch_inline_query=switch_inline_query,
                                                   switch_inline_query_current_chat=switch_inline_query_current_chat,
                                                   callback_game=callback_game,
                                                   pay=pay, **kwargs)


class InlineKeyboardMarkup(BaseModel):
    """
    This object represents an inline keyboard that appears right next to the message it belongs to.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will display unsupported message.
    https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """
    inline_keyboard: List[List['InlineKeyboardButton']] = []

    def __init__(self, row_width=3, inline_keyboard=None, **kwargs):
        if inline_keyboard is None:
            inline_keyboard = []

        conf = kwargs.pop('conf', {}) or {}
        conf['row_width'] = row_width

        super(InlineKeyboardMarkup, self).__init__(**kwargs,
                                                   conf=conf,
                                                   inline_keyboard=inline_keyboard)

    @property
    def row_width(self):
        return self.conf.get('row_width', 3)

    @row_width.setter
    def row_width(self, value):
        self.conf['row_width'] = value

    def add(self, *args):
        """
        Add buttons
        :param args:
        :return: 'self'
        :rtype: ':'obj:`types.InlineKeyboardMarkup`
        """
        row = []
        for index, button in enumerate(args, start=1):
            row.append(button)
            if index % self.row_width == 0:
                self.inline_keyboard.append(row)
                row = []
        if len(row) > 0:
            self.inline_keyboard.append(row)
        return self

    def row(self, *args):
        """
        Add row
        :param args:
        :return: 'self'
        :rtype: ':'obj:`types.InlineKeyboardMarkup`
        """
        btn_array = []
        for button in args:
            btn_array.append(button)
        self.inline_keyboard.append(btn_array)
        return self

    def insert(self, button):
        """
        Insert button to last row
        :param button:
        :return: 'self'
        :rtype: ':'obj:`types.InlineKeyboardMarkup`
        """
        if self.inline_keyboard and len(self.inline_keyboard[-1]) < self.row_width:
            self.inline_keyboard[-1].append(button)
        else:
            self.add(button)
        return self


class PollOption(BaseModel):
    text: str = None
    voter_count: int = None


class Poll(BaseModel):
    id: str = None
    question: str = None
    options: List['PollOption'] = []
    is_closed: bool = None


class PassportFile(BaseModel):
    """
    This object represents a file uploaded to Telegram Passport.
    Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB.
    https://core.telegram.org/bots/api#passportfile
    """

    file_id: str = None
    file_size: int = None
    file_date: int = None


class EncryptedPassportElement(BaseModel):
    """
    Contains information about documents or other Telegram Passport elements shared with the bot by the user.
    https://core.telegram.org/bots/api#encryptedpassportelement
    """

    type: str = None
    data: str = None
    phone_number: str = None
    email: str = None
    files: List['PassportFile'] = []
    front_side: 'PassportFile' = None
    reverse_side: 'PassportFile' = None
    selfie: 'PassportFile' = None


class EncryptedCredentials(BaseModel):
    """
    Contains data required for decrypting and authenticating EncryptedPassportElement.
    See the Telegram Passport Documentation for a complete description of the data decryption
    and authentication processes.
    https://core.telegram.org/bots/api#encryptedcredentials
    """

    data: str = None
    hash: str = None
    secret: str = None


class PassportData(BaseModel):
    """
    Contains information about Telegram Passport data shared with the bot by the user.
    https://core.telegram.org/bots/api#passportdata
    """

    data: List['EncryptedPassportElement'] = None
    credentials: 'EncryptedCredentials' = None


class SuccessfulPayment(BaseModel):
    """
    This object contains basic information about a successful payment.
    https://core.telegram.org/bots/api#successfulpayment
    """
    currency: str = None
    total_amount: int = None
    invoice_payload: str = None
    shipping_option_id: str = None
    order_info: 'OrderInfo' = None
    telegram_payment_charge_id: str = None
    provider_payment_charge_id: str = None


class Invoice(BaseModel):
    """
    This object contains basic information about an invoice.
    https://core.telegram.org/bots/api#invoice
    """
    title: str = None
    description: str = None
    start_parameter: str = None
    currency: str = None
    total_amount: int = None


class Location(BaseModel):
    """
    This object represents a point on the map.
    https://core.telegram.org/bots/api#location
    """
    longitude: float = None
    latitude: float = None


class Venue(BaseModel):
    """
    This object represents a venue.
    https://core.telegram.org/bots/api#venue
    """
    location: 'Location' = None
    title: str = None
    address: str = None
    foursquare_id: str = None
    foursquare_type: str = None


class Contact(BaseModel):
    """
    This object represents a phone contact.
    https://core.telegram.org/bots/api#contact
    """
    phone_number: str = None
    first_name: str = None
    last_name: str = None
    user_id: int = None
    vcard: str = None

    @property
    def full_name(self):
        name = self.first_name
        if self.last_name is not None:
            name += ' ' + self.last_name
        return name


class Voice(BaseModel):
    """
    This object represents a voice note.
    https://core.telegram.org/bots/api#voice
    """
    file_id: str = None
    duration: int = None
    mime_type: str = None
    file_size: int = None


class PhotoSize(BaseModel):
    """
    This object represents one size of a photo or a file / sticker thumbnail.
    https://core.telegram.org/bots/api#photosize
    """
    file_id: str = None
    width: int = None
    height: int = None
    file_size: int = None


class VideoNote(BaseModel):
    """
    This object represents a video message (available in Telegram apps as of v.4.0).
    https://core.telegram.org/bots/api#videonote
    """
    file_id: str = None
    length: int = None
    duration: int = None
    thumb: 'PhotoSize' = None
    file_size: int = None


class Video(BaseModel):
    """
    This object represents a video file.
    https://core.telegram.org/bots/api#video
    """
    file_id: str = None
    width: int = None
    height: int = None
    duration: int = None
    thumb: 'PhotoSize' = None
    mime_type: str = None
    file_size: int = None


class Sticker(BaseModel):
    """
    This object represents a sticker.
    https://core.telegram.org/bots/api#sticker
    """
    file_id: str = None
    width: int = None
    height: int = None
    thumb: 'PhotoSize' = None
    emoji: str = None
    set_name: str = None
    mask_position: 'MaskPosition' = None
    file_size: int = None


class Audio(BaseModel):
    """
    This object represents an audio file to be treated as music by the Telegram clients.
    https://core.telegram.org/bots/api#audio
    """
    file_id: str = None
    duration: int = None
    performer: str = None
    title: str = None
    mime_type: str = None
    file_size: int = None
    thumb: 'PhotoSize' = None


class Animation(BaseModel):
    """
    You can provide an animation for your game so that it looks stylish in chats
    (check out Lumberjack for an example).
    This object represents an animation file to be displayed in the message containing a game.
    https://core.telegram.org/bots/api#animation
    """

    file_id: str = None
    thumb: 'PhotoSize' = None
    file_name: str = None
    mime_type: str = None
    file_size: int = None


class Document(BaseModel):
    """
    This object represents a general file (as opposed to photos, voice messages and audio files).
    https://core.telegram.org/bots/api#document
    """
    file_id: str = None
    thumb: 'PhotoSize' = None
    file_name: str = None
    mime_type: str = None
    file_size: int = None


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str = None
    username: str = None
    language_code: str = None


User.update_forward_refs()


class ShippingAddress(BaseModel):
    """
    This object represents a shipping address.
    https://core.telegram.org/bots/api#shippingaddress
    """
    country_code: str = None
    state: str = None
    city: str = None
    street_line1: str = None
    street_line2: str = None
    post_code: str = None


class OrderInfo(BaseModel):
    """
    This object represents information about an order.
    https://core.telegram.org/bots/api#orderinfo
    """
    name: str = None
    phone_number: str = None
    email: str = None
    shipping_address: 'ShippingAddress' = None


class PreCheckoutQuery(BaseModel):
    """
    This object contains information about an incoming pre-checkout query.
    Your bot can offer users HTML5 games to play solo or to compete against
    each other in groups and one-on-one chats.
    Create games via @BotFather using the /newgame command.
    Please note that this kind of power requires responsibility:
    you will need to accept the terms for each game that your bots will be offering.
    https://core.telegram.org/bots/api#precheckoutquery
    """
    id: str = None
    from_user: 'User' = None
    currency: str = None
    total_amount: int = None
    invoice_payload: str = None
    shipping_option_id: str = None
    order_info: 'OrderInfo' = None


class ShippingQuery(BaseModel):
    """
    This object contains information about an incoming shipping query.
    https://core.telegram.org/bots/api#shippingquery
    """
    id: str = None
    from_user: 'User' = None
    invoice_payload: str = None
    shipping_address: 'ShippingAddress' = None


class ShippingOption(BaseModel):
    """
    This object represents one shipping option.
    https://core.telegram.org/bots/api#shippingoption
    """
    id: str = None
    title: str = None
    prices: List['LabeledPrice'] = []


class ChosenInlineResult(BaseModel):
    """
    Represents a result of an inline query that was chosen by the user and sent to their chat partner.
    Note: 'It' is necessary to enable inline feedback via @Botfather in order to receive these objects in updates.
    Your bot can accept payments from Telegram users.
    Please see the introduction to payments for more details on the process and how to set up payments for your bot.
    Please note that users will need Telegram v.4.0 or higher to use payments (released on May 18, 2017).
    https://core.telegram.org/bots/api#choseninlineresult
    """
    result_id: str = None
    from_user: 'User' = None
    location: 'Location' = None
    inline_message_id: str = None
    query: str = None


class InlineQuery(BaseModel):
    """
    This object represents an incoming inline query.
    When the user sends an empty query, your bot could return some default or trending results.
    https://core.telegram.org/bots/api#inlinequery
    """
    id: str = None
    from_user: 'User' = None
    location: 'Location' = None
    query: str = None
    offset: str = None

    async def answer(self,
                     results: List['InlineQueryResult'],
                     cache_time: Union[int, None] = None,
                     is_personal: Union[bool, None] = None,
                     next_offset: Union[str, None] = None,
                     switch_pm_text: Union[str, None] = None,
                     switch_pm_parameter: Union[str, None] = None):
        """
        Use this method to send answers to an inline query.
        No more than 50 results per query are allowed.
        Source: 'https'://core.telegram.org/bots/api#answerinlinequery
        :param results: 'A' JSON-serialized array of results for the inline query
        :type results: ':'obj:`List[types.InlineQueryResult]`
        :param cache_time: 'The' maximum amount of time in seconds that the result of the
            inline query may be cached on the server. Defaults to 300.
        :type cache_time: ':'obj:`Union[int, None]`
        :param is_personal: 'Pass' True, if results may be cached on the server side only
            for the user that sent the query. By default, results may be returned to any user who sends the same query
        :type is_personal: ':'obj:`Union[bool, None]`
        :param next_offset: 'Pass' the offset that a client should send in the
            next query with the same text to receive more results.
            Pass an empty string if there are no more results or if you don‘t support pagination.
            Offset length can’t exceed 64 bytes.
        :type next_offset: ':'obj:`Union[str, None]`
        :param switch_pm_text: 'If' passed, clients will display a button with specified text that
            switches the user to a private chat with the bot and sends the bot a start message
            with the parameter switch_pm_parameter
        :type switch_pm_text: ':'obj:`Union[str, None]`
        :param switch_pm_parameter: 'Deep'-linking parameter for the /start message sent to the bot when
            user presses the switch button. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.
        :type switch_pm_parameter: ':'obj:`Union[str, None]`
        :return: 'On' success, True is returned
        :rtype: ':'obj:`bool`
        """
        return await self.bot.answer_inline_query(self.id,
                                                  results=results,
                                                  cache_time=cache_time,
                                                  is_personal=is_personal,
                                                  next_offset=next_offset,
                                                  switch_pm_text=switch_pm_text,
                                                  switch_pm_parameter=switch_pm_parameter)


class ChatActions(str, Enum):
    TYPING: str = 'typing'
    UPLOAD_PHOTO: str = 'upload_photo'
    RECORD_VIDEO: str = 'record_video'
    UPLOAD_VIDEO: str = 'upload_video'
    RECORD_AUDIO: str = 'record_audio'
    UPLOAD_AUDIO: str = 'upload_audio'
    UPLOAD_DOCUMENT: str = 'upload_document'
    FIND_LOCATION: str = 'find_location'
    RECORD_VIDEO_NOTE: str = 'record_video_note'
    UPLOAD_VIDEO_NOTE: str = 'upload_video_note'


class ChatPhoto(BaseModel):
    """
    This object represents a chat photo.
    https://core.telegram.org/bots/api#chatphoto
    """
    small_file_id: str = None
    big_file_id: str = None


ChatPhoto.update_forward_refs()


class ChatType(str, Enum):
    private: str = 'private'
    group: str = 'group'
    supergroup: str = 'supergroup'
    channel: str = 'channel'


class ChatPermissions(BaseModel):
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_views: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None


class Chat(BaseModel):  # Checked
    id: int
    type: str
    title: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    all_members_are_administrators: bool = None
    photo: 'ChatPhoto' = None
    description: str = None
    invite_link: str = None
    pinned_message: Any = None  # TODO make this type Message
    permissions: 'ChatPermissions' = None
    sticker_set_name: str = None
    can_set_sticker_set: bool = None


Chat.update_forward_refs()


class MessageEntityType(str, Enum):
    MENTION = 'mention'
    HASHTAG = 'hashtag'
    CASHTAG = 'cashtag'
    BOT_COMMAND = 'bot_command'
    URL = 'url'
    EMAIL = 'email'
    PHONE_NUMBER = 'phone_number'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    PRE = 'pre'
    TEXT_LINK = 'text_link'
    TEXT_MENTION = 'text_mention'


class MessageEntity(BaseModel):
    """
    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
    https://core.telegram.org/bots/api#messageentity
    """
    type: 'MessageEntityType' = None
    offset: int = None
    length: int = None
    url: str = None
    user: 'User' = None


MessageEntity.update_forward_refs()


class Game(BaseModel):
    """
    This object represents a game.
    Use BotFather to create and edit games, their short names will act as unique identifiers.
    https://core.telegram.org/bots/api#game
    """
    title: str = None
    description: str = None
    photo: List['PhotoSize'] = []
    text: str = None
    text_entities: List['MessageEntity'] = []
    animation: 'Animation' = None


Game.update_forward_refs()


class Message(BaseModel):  # Checked
    message_id: int
    from_user: 'User' = Schema(None, alias='from')
    date: datetime.datetime
    chat: 'Chat'
    forward_from: 'User' = None
    forward_from_chat: 'Chat' = None
    forward_from_message_id: int = None
    forward_signature: str = None
    forward_sender_name: str = None
    forward_date: datetime.datetime = None
    reply_to_message: 'Message' = None  # TODO make this Message
    edit_date: datetime.datetime = None
    media_group_id: str = None
    author_signature: str = None
    text: str = None
    entities: List['MessageEntity'] = None
    caption_entities: List['MessageEntity'] = None
    audio: 'Audio' = None
    document: 'Document' = None
    animation: 'Animation' = None
    game: 'Game' = None
    photo: List['PhotoSize'] = None
    sticker: 'Sticker' = None
    video: 'Video' = None
    voice: 'Voice' = None
    video_note: 'VideoNote' = None
    caption: str = None
    contact: 'Contact' = None
    location: 'Location' = None
    venue: 'Venue' = None
    poll: 'Poll' = None
    new_chat_members: List[User] = []
    left_chat_member: 'User' = None
    new_chat_title: str = None
    new_chat_photo: List['PhotoSize'] = []
    delete_chat_photo: bool = None
    group_chat_created: bool = None
    supergroup_chat_created: bool = None
    channel_chat_created: bool = None
    migrate_to_chat_id: int = None
    migrate_from_chat_id: int = None
    pinned_message: 'Message' = None  # TODO Make this Message
    invoice: 'Invoice' = None
    successful_payment: 'SuccessfulPayment' = None
    connected_website: str = None
    passport_data: 'PassportData' = None
    reply_markup: 'InlineKeyboardMarkup' = None


Message.update_forward_refs()


class CallbackQuery(BaseModel):
    """
    This object represents an incoming callback query from a callback button in an inline keyboard.
    If the button that originated the query was attached to a message sent by the bot,
    the field message will be present.
    If the button was attached to a message sent via the bot (in inline mode),
    the field inline_message_id will be present.
    Exactly one of the fields data or game_short_name will be present.
    https://core.telegram.org/bots/api#callbackquery
    """
    id: str = None
    from_user: 'User' = None
    message: 'Message' = None
    inline_message_id: str = None
    chat_instance: str = None
    data: str = None
    game_short_name: str = None


class Update(BaseModel):
    update_id: int
    message: 'Message'
    edited_message: 'Message' = None
    channel_post: 'Message' = None
    edited_channel_post: 'Message' = None
    inline_query: 'InlineQuery' = None
    chosen_inline_result: 'ChosenInlineResult' = None
    callback_query: 'CallbackQuery' = None
    shipping_query: 'ShippingQuery' = None
    pre_checkout_query: 'PreCheckoutQuery' = None
    poll: 'Poll' = None


Update.update_forward_refs()


class WebhookInfo(BaseModel):
    """
    Contains information about the current status of a webhook.
    https://core.telegram.org/bots/api#webhookinfo
    """
    url: str = None
    has_custom_certificate: bool = None
    pending_update_count: int = None
    last_error_date: int = None
    last_error_message: str = None
    max_connections: int = None
    allowed_updates: List[str] = []


class UserProfilePhotos(BaseModel):
    """
    This object represent a user's profile pictures.
    https://core.telegram.org/bots/api#userprofilephotos
    """
    total_count: int = None
    photos: List[List['PhotoSize']] = []


class StickerSet(BaseModel):
    """
    This object represents a sticker set.
    https://core.telegram.org/bots/api#stickerset
    """
    name: str = None
    title: str = None
    contains_masks: bool = None
    stickers: List['Sticker'] = []


class ResponseParameters(BaseModel):
    """
    Contains information about why a request was unsuccessful.
    https://core.telegram.org/bots/api#responseparameters
    """
    migrate_to_chat_id: int = None
    retry_after: int = None


class ReplyKeyboardMarkup(BaseModel):
    """
    This object represents a custom keyboard with reply options (see Introduction to bots for details and examples).
    https://core.telegram.org/bots/api#replykeyboardmarkup
    """
    keyboard: List[List['KeyboardButton']] = []
    resize_keyboard: bool = None
    one_time_keyboard: bool = None
    selective: bool = None


class KeyboardButton(BaseModel):
    """
    This object represents one button of the reply keyboard. For simple text buttons String can be used instead of this object to specify text of the button. Optional fields are mutually exclusive.
    Note: 'request_contact' and request_location options will only work in Telegram versions released after 9 April, 2016. Older clients will ignore them.
    https://core.telegram.org/bots/api#keyboardbutton
    """
    text: str = None
    request_contact: bool = None
    request_location: bool = None
    #
    # def __init__(self, text: str,
    #              request_contact: bool = None,
    #              request_location: bool = None):
    #     super(KeyboardButton, self).__init__(text=text,
    #                                          request_contact=request_contact,
    #                                          request_location=request_location)


class ReplyKeyboardRemove(BaseModel):
    """
    Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and display the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot. An exception is made for one-time keyboards that are hidden immediately after the user presses a button (see ReplyKeyboardMarkup).
    https://core.telegram.org/bots/api#replykeyboardremove
    """
    remove_keyboard: bool = None
    selective: bool = None

    def __init__(self, selective: bool = None):
        super(ReplyKeyboardRemove, self).__init__(remove_keyboard=True,
                                                  selective=selective)


class PassportElementError(BaseModel):
    """
    This object represents an error in the Telegram Passport element which was submitted that
    should be resolved by the user.
    https://core.telegram.org/bots/api#passportelementerror
    """

    source: str = None
    type: str = None
    message: str = None


class PassportElementErrorDataField(PassportElementError):
    """
    Represents an issue in one of the data fields that was provided by the user.
    The error is considered resolved when the field's value changes.
    https://core.telegram.org/bots/api#passportelementerrordatafield
    """

    field_name: str = None
    data_hash: str = None

    def __init__(self, source: str, type: str, field_name: str,
                 data_hash: str, message: str):
        super(PassportElementErrorDataField, self).__init__(source=source, type=type,
                                                            field_name=field_name,
                                                            data_hash=data_hash,
                                                            message=message)


class PassportElementErrorFile(PassportElementError):
    """
    Represents an issue with a document scan.
    The error is considered resolved when the file with the document scan changes.
    https://core.telegram.org/bots/api#passportelementerrorfile
    """

    file_hash: str = None

    def __init__(self, source: str, type: str, file_hash: str,
                 message: str):
        super(PassportElementErrorFile, self).__init__(source=source, type=type,
                                                       file_hash=file_hash,
                                                       message=message)


class PassportElementErrorFiles(PassportElementError):
    """
    Represents an issue with a list of scans.
    The error is considered resolved when the list of files containing the scans changes.
    https://core.telegram.org/bots/api#passportelementerrorfiles
    """

    file_hashes: List[str] = []

    def __init__(self, source: str, type: str,
                 file_hashes: List[str],
                 message: str):
        super(PassportElementErrorFiles, self).__init__(source=source, type=type,
                                                        file_hashes=file_hashes,
                                                        message=message)


class PassportElementErrorFrontSide(PassportElementError):
    """
    Represents an issue with the front side of a document.
    The error is considered resolved when the file with the front side of the document changes.
    https://core.telegram.org/bots/api#passportelementerrorfrontside
    """

    file_hash: str = None

    def __init__(self, source: str, type: str, file_hash: str,
                 message: str):
        super(PassportElementErrorFrontSide, self).__init__(source=source, type=type,
                                                            file_hash=file_hash,
                                                            message=message)


class PassportElementErrorReverseSide(PassportElementError):
    """
    Represents an issue with the reverse side of a document.
    The error is considered resolved when the file with reverse side of the document changes.
    https://core.telegram.org/bots/api#passportelementerrorreverseside
    """

    file_hash: str = None

    def __init__(self, source: str, type: str, file_hash: str,
                 message: str):
        super(PassportElementErrorReverseSide, self).__init__(source=source, type=type,
                                                              file_hash=file_hash,
                                                              message=message)


class PassportElementErrorSelfie(PassportElementError):
    """
    Represents an issue with the selfie with a document.
    The error is considered resolved when the file with the selfie changes.
    https://core.telegram.org/bots/api#passportelementerrorselfie
    """

    file_hash: str = None

    def __init__(self, source: str, type: str, file_hash: str,
                 message: str):
        super(PassportElementErrorSelfie, self).__init__(source=source, type=type,
                                                         file_hash=file_hash,
                                                         message=message)


class MaskPosition(BaseModel):
    """
    This object describes the position on faces where a mask should be placed by default.
    https://core.telegram.org/bots/api#maskposition
    """
    point: str = None
    x_shift: float = None
    y_shift: float = None
    scale: float = None


class LoginUrl(BaseModel):
    """
    This object represents a parameter of the inline keyboard button used to automatically authorize a user.
    Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram.
    All the user needs to do is tap/click a button and confirm that they want to log in.
    https://core.telegram.org/bots/api#loginurl
    """
    url: str = None
    forward_text: str = None
    bot_username: str = None
    request_write_access: bool = None


class LabeledPrice(BaseModel):
    """
    This object represents a portion of the price for goods or services.
    https://core.telegram.org/bots/api#labeledprice
    """
    label: str = None
    amount: int = None


class InputMessageContent(BaseModel):
    """
    This object represents the content of a message to be sent as a result of an inline query.
    Telegram clients currently support the following 4 types
    https://core.telegram.org/bots/api#inputmessagecontent
    """
    pass


class InputContactMessageContent(InputMessageContent):
    """
    Represents the content of a contact message to be sent as the result of an inline query.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inputcontactmessagecontent
    """
    phone_number: str = None
    first_name: str = None
    last_name: str = None
    vcard: str = None

    def __init__(self, phone_number: str,
                 first_name: Optional[str] = None,
                 last_name: Optional[str] = None):
        super(InputContactMessageContent, self).__init__(phone_number=phone_number,
                                                         first_name=first_name,
                                                         last_name=last_name)


class InputLocationMessageContent(InputMessageContent):
    """
    Represents the content of a location message to be sent as the result of an inline query.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inputlocationmessagecontent
    """
    latitude: float = None
    longitude: float = None

    def __init__(self, latitude: float, longitude: float):
        super(InputLocationMessageContent, self).__init__(latitude=latitude,
                                                          longitude=longitude)


class InputTextMessageContent(InputMessageContent):
    """
    Represents the content of a text message to be sent as the result of an inline query.
    https://core.telegram.org/bots/api#inputtextmessagecontent
    """
    message_text: str = None
    parse_mode: str = None
    disable_web_page_preview: bool = None

    def safe_get_parse_mode(self):
        try:
            return self.bot.parse_mode
        except RuntimeError:
            pass

    def __init__(self, message_text: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 disable_web_page_preview: Optional[bool] = None):
        if parse_mode is None:
            parse_mode = self.safe_get_parse_mode()

        super(InputTextMessageContent, self).__init__(message_text=message_text,
                                                      parse_mode=parse_mode,
                                                      disable_web_page_preview=disable_web_page_preview)


class InputVenueMessageContent(InputMessageContent):
    """
    Represents the content of a venue message to be sent as the result of an inline query.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inputvenuemessagecontent
    """
    latitude: float = None
    longitude: float = None
    title: str = None
    address: str = None
    foursquare_id: str = None

    def __init__(self, latitude: Optional[float] = None,
                 longitude: Optional[float] = None,
                 title: Optional[str] = None,
                 address: Optional[str] = None,
                 foursquare_id: Optional[str] = None):
        super(InputVenueMessageContent, self).__init__(latitude=latitude,
                                                       longitude=longitude, title=title,
                                                       address=address,
                                                       foursquare_id=foursquare_id)


class InputMedia(BaseModel):
    """
    This object represents the content of a media message to be sent. It should be one of
     - InputMediaAnimation
     - InputMediaDocument
     - InputMediaAudio
     - InputMediaPhoto
     - InputMediaVideo
    That is only base class.
    https://core.telegram.org/bots/api#inputmedia
    """
    type: str = None
    media: str = None
    thumb: Union[InputFile, str] = Schema(None, alias='thumb')
    caption: str = None
    parse_mode: bool = None


class InputMediaAnimation(InputMedia):
    """
    Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.
    https://core.telegram.org/bots/api#inputmediaanimation
    """

    width: int = None
    height: int = None
    duration: int = None

    def __init__(self, media: InputFile, thumb: Union[InputFile, str] = None,
                 caption: str = None,
                 width: int = None, height: int = None, duration: int = None,
                 parse_mode: bool = None, **kwargs):
        super(InputMediaAnimation, self).__init__(type='animation', media=media,
                                                  thumb=thumb, caption=caption,
                                                  width=width, height=height,
                                                  duration=duration,
                                                  parse_mode=parse_mode, conf=kwargs)


class InputMediaDocument(InputMedia):
    """
    Represents a photo to be sent.
    https://core.telegram.org/bots/api#inputmediadocument
    """

    def __init__(self, media: InputFile,
                 thumb: Union[InputFile, str] = None,
                 caption: str = None, parse_mode: bool = None, **kwargs):
        super(InputMediaDocument, self).__init__(type='document', media=media,
                                                 thumb=thumb,
                                                 caption=caption, parse_mode=parse_mode,
                                                 conf=kwargs)


class InputMediaAudio(InputMedia):
    """
    Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.
    https://core.telegram.org/bots/api#inputmediaanimation
    """

    width: int = None
    height: int = None
    duration: int = None
    performer: str = None
    title: str = None

    def __init__(self, media: InputFile,
                 thumb: Union[InputFile, str] = None,
                 caption: str = None,
                 width: int = None, height: int = None,
                 duration: int = None,
                 performer: str = None,
                 title: str = None,
                 parse_mode: bool = None, **kwargs):
        super(InputMediaAudio, self).__init__(type='audio', media=media, thumb=thumb,
                                              caption=caption,
                                              width=width, height=height,
                                              duration=duration,
                                              performer=performer, title=title,
                                              parse_mode=parse_mode, conf=kwargs)


class InputMediaPhoto(InputMedia):
    """
    Represents a photo to be sent.
    https://core.telegram.org/bots/api#inputmediaphoto
    """

    def __init__(self, media: InputFile,
                 thumb: Union[InputFile, str] = None,
                 caption

                 : str = None, parse_mode: bool = None, **kwargs):
        super(InputMediaPhoto, self).__init__(type='photo', media=media, thumb=thumb,
                                              caption=caption, parse_mode=parse_mode,
                                              conf=kwargs)


class InputMediaVideo(InputMedia):
    """
    Represents a video to be sent.
    https://core.telegram.org/bots/api#inputmediavideo
    """
    width: int = None
    height: int = None
    duration: int = None
    supports_streaming: bool = None

    def __init__(self, media: InputFile,
                 thumb: Union[InputFile, str] = None,
                 caption: str = None,
                 width: int = None, height: int = None,
                 duration: int = None,
                 parse_mode: bool = None,
                 supports_streaming: bool = None, **kwargs):
        super(InputMediaVideo, self).__init__(type='video', media=media, thumb=thumb,
                                              caption=caption,
                                              width=width, height=height,
                                              duration=duration,
                                              parse_mode=parse_mode,
                                              supports_streaming=supports_streaming,
                                              conf=kwargs)


class InlineQueryResult(BaseModel):
    """
    This object represents one result of an inline query.
    Telegram clients currently support results of the following 20 types
    https://core.telegram.org/bots/api#inlinequeryresult
    """
    id: str = None
    reply_markup: 'InlineKeyboardMarkup' = None


class InlineQueryResultArticle(InlineQueryResult):
    """
    Represents a link to an article or web page.
    https://core.telegram.org/bots/api#inlinequeryresultarticle
    """
    type: str = None
    title: str = None
    input_message_content: 'InputMessageContent' = None
    url: str = None
    hide_url: bool = None
    description: str = None
    thumb_url: str = None
    thumb_width: int = None
    thumb_height: int = None


class InlineQueryResultPhoto(InlineQueryResult):
    """
    Represents a link to a photo.
    By default, this photo will be sent by the user with optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the photo.
    https://core.telegram.org/bots/api#inlinequeryresultphoto
    """
    type: str = None
    photo_url: str = None
    thumb_url: str = None
    photo_width: int = None
    photo_height: int = None
    title: str = None
    description: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None


class InlineQueryResultGif(InlineQueryResult):
    """
    Represents a link to an animated GIF file.
    By default, this animated GIF file will be sent by the user with optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the animation.
    https://core.telegram.org/bots/api#inlinequeryresultgif
    """
    type: str = None
    gif_url: str = None
    gif_width: int = None
    gif_height: int = None
    gif_duration: int = None
    thumb_url: str = None
    title: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    """
    Represents a link to a video animation (H.264/MPEG-4 AVC video without sound).
    By default, this animated MPEG-4 file will be sent by the user with optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the animation.
    https://core.telegram.org/bots/api#inlinequeryresultmpeg4gif
    """
    type: str = None
    mpeg4_url: str = None
    mpeg4_width: int = None
    mpeg4_height: int = None
    mpeg4_duration: int = None
    thumb_url: str = None
    title: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None


class InlineQueryResultVideo(InlineQueryResult):
    """
    Represents a link to a page containing an embedded video player or a video file.
    By default, this video file will be sent by the user with an optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the video.
    If an InlineQueryResultVideo message contains an embedded video (e.g., YouTube),
    you must replace its content using input_message_content.
    https://core.telegram.org/bots/api#inlinequeryresultvideo
    """
    type: str = None
    video_url: str = None
    mime_type: str = None
    thumb_url: str = None
    title: str = None
    caption: str = None
    video_width: int = None
    video_height: int = None
    video_duration: int = None
    description: str = None
    input_message_content: 'InputMessageContent' = None


class InlineQueryResultAudio(InlineQueryResult):
    """
    Represents a link to an mp3 audio file. By default, this audio file will be sent by the user.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the audio.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultaudio
    """
    type: str = None
    audio_url: str = None
    title: str = None
    caption: str = None
    performer: str = None
    audio_duration: int = None
    input_message_content: 'InputMessageContent' = None


class InlineQueryResultVoice(InlineQueryResult):
    """
    Represents a link to a voice recording in an .ogg container encoded with OPUS.
    By default, this voice recording will be sent by the user.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the the voice message.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultvoice
    """
    type: str = None
    voice_url: str = None
    title: str = None
    caption: str = None
    voice_duration: int = None
    input_message_content: 'InputMessageContent' = None


class InlineQueryResultDocument(InlineQueryResult):
    """
    Represents a link to a file.
    By default, this file will be sent by the user with an optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the file. Currently, only .PDF and .ZIP files can be sent using this method.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016. Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultdocument
    """
    type: str = None
    title: str = None
    caption: str = None
    document_url: str = None
    mime_type: str = None
    description: str = None
    input_message_content: 'InputMessageContent' = None
    thumb_url: str = None
    thumb_width: int = None
    thumb_height: int = None


class InlineQueryResultLocation(InlineQueryResult):
    """
    Represents a location on a map.
    By default, the location will be sent by the user.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the location.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultlocation
    """
    type: str = None
    latitude: float = None
    longitude: float = None
    title: str = None
    live_period: int = None
    input_message_content: 'InputMessageContent' = None
    thumb_url: str = None
    thumb_width: int = None
    thumb_height: int = None


class InlineQueryResultVenue(InlineQueryResult):
    """
    Represents a venue. By default, the venue will be sent by the user.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the venue.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultvenue
    """
    type: str = None
    latitude: float = None
    longitude: float = None
    title: str = None
    address: str = None
    foursquare_id: str = None
    input_message_content: 'InputMessageContent' = None
    thumb_url: str = None
    thumb_width: int = None
    thumb_height: int = None
    foursquare_type: str = None

    def __init__(self, *,
                 id: str,
                 latitude: float,
                 longitude: float,

                 title: str,
                 address: str,
                 foursquare_id: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[
                     InputMessageContent] = None,
                 thumb_url: Optional[str] = None,
                 thumb_width: Optional[
                     int] = None,
                 thumb_height: Optional[int] = None,
                 foursquare_type: Optional[str] = None):
        super(InlineQueryResultVenue, self).__init__(id=id, latitude=latitude,
                                                     longitude=longitude,
                                                     title=title, address=address,
                                                     foursquare_id=foursquare_id,
                                                     reply_markup=reply_markup,
                                                     input_message_content=input_message_content,
                                                     thumb_url=thumb_url,
                                                     thumb_width=thumb_width,
                                                     thumb_height=thumb_height,
                                                     foursquare_type=foursquare_type)


class InlineQueryResultContact(InlineQueryResult):
    """
    Represents a contact with a phone number.
    By default, this contact will be sent by the user.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the contact.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016. Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultcontact
    """
    type: str = None
    phone_number: str = None
    first_name: str = None
    last_name: str = None
    vcard: str = None
    input_message_content: 'InputMessageContent' = None
    thumb_url: str = None
    thumb_width: int = None
    thumb_height: int = None
    foursquare_type: str = None

    def __init__(self, *,
                 id: str,
                 phone_number: str,
                 first_name: str,
                 last_name: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None,
                 thumb_url: Optional[str] = None,
                 thumb_width: Optional[int] = None,
                 thumb_height: Optional[int] = None,
                 foursquare_type: Optional[str] = None):
        super(InlineQueryResultContact, self).__init__(id=id, phone_number=phone_number,
                                                       first_name=first_name,
                                                       last_name=last_name,
                                                       reply_markup=reply_markup,
                                                       input_message_content=input_message_content,
                                                       thumb_url=thumb_url,
                                                       thumb_width=thumb_width,
                                                       thumb_height=thumb_height,
                                                       foursquare_type=foursquare_type)


class InlineQueryResultGame(InlineQueryResult):
    """
    Represents a Game.
    Note: 'This' will only work in Telegram versions released after October 1, 2016.
    Older clients will not display any inline results if a game result is among them.
    https://core.telegram.org/bots/api#inlinequeryresultgame
    """
    type: str = None
    game_short_name: str = None

    def __init__(self, *,
                 id: str,
                 game_short_name: str,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None):
        super(InlineQueryResultGame, self).__init__(id=id,
                                                    game_short_name=game_short_name,
                                                    reply_markup=reply_markup)


class InlineQueryResultCachedPhoto(InlineQueryResult):
    """
    Represents a link to a photo stored on the Telegram servers.
    By default, this photo will be sent by the user with an optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the photo.
    https://core.telegram.org/bots/api#inlinequeryresultcachedphoto
    """
    type: str = None
    photo_file_id: str = None
    title: str = None
    description: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None

    def __init__(self, *,
                 id: str,
                 photo_file_id: str,
                 title: Optional[str] = None,
                 description: Optional[str] = None,
                 caption: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None):
        super(InlineQueryResultCachedPhoto, self).__init__(id=id,
                                                           photo_file_id=photo_file_id,
                                                           title=title,
                                                           description=description,
                                                           caption=caption,
                                                           parse_mode=parse_mode,
                                                           reply_markup=reply_markup,
                                                           input_message_content=input_message_content)


class InlineQueryResultCachedGif(InlineQueryResult):
    """
    Represents a link to an animated GIF file stored on the Telegram servers.
    By default, this animated GIF file will be sent by the user with an optional caption.
    Alternatively, you can use input_message_content to send a message with specified content
    instead of the animation.
    https://core.telegram.org/bots/api#inlinequeryresultcachedgif
    """
    type: str = None
    gif_file_id: str = None
    title: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None

    def __init__(self, *,
                 id: str,
                 gif_file_id: str,
                 title: Optional[str] = None,
                 caption: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None):
        super(InlineQueryResultCachedGif, self).__init__(id=id, gif_file_id=gif_file_id,
                                                         title=title, caption=caption,
                                                         parse_mode=parse_mode,
                                                         reply_markup=reply_markup,
                                                         input_message_content=input_message_content)


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):
    """
    Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers.
    By default, this animated MPEG-4 file will be sent by the user with an optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the animation.
    https://core.telegram.org/bots/api#inlinequeryresultcachedmpeg4gif
    """
    type: str = None
    mpeg4_file_id: str = None
    title: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None

    def __init__(self, *,
                 id: str,
                 mpeg4_file_id: str,
                 title: Optional[str] = None,
                 caption: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None):
        super(InlineQueryResultCachedMpeg4Gif, self).__init__(id=id,
                                                              mpeg4_file_id=mpeg4_file_id,
                                                              title=title,
                                                              caption=caption,
                                                              parse_mode=parse_mode,
                                                              reply_markup=reply_markup,
                                                              input_message_content=input_message_content)


class InlineQueryResultCachedSticker(InlineQueryResult):
    """
    Represents a link to a sticker stored on the Telegram servers.
    By default, this sticker will be sent by the user.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the sticker.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultcachedsticker
    """
    type: str = None
    sticker_file_id: str = None
    input_message_content: 'InputMessageContent' = None

    def __init__(self, *,
                 id: str,
                 sticker_file_id: str,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None):
        super(InlineQueryResultCachedSticker, self).__init__(id=id,
                                                             sticker_file_id=sticker_file_id,
                                                             reply_markup=reply_markup,
                                                             input_message_content=input_message_content)


class InlineQueryResultCachedDocument(InlineQueryResult):
    """
    Represents a link to a file stored on the Telegram servers.
    By default, this file will be sent by the user with an optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the file.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultcacheddocument
    """
    type: str = None
    title: str = None
    document_file_id: str = None
    description: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None

    def __init__(self, *,
                 id: str,
                 title: str,
                 document_file_id: str,
                 description: Optional[str] = None,
                 caption: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None):
        super(InlineQueryResultCachedDocument, self).__init__(id=id, title=title,
                                                              document_file_id=document_file_id,
                                                              description=description,
                                                              caption=caption,
                                                              parse_mode=parse_mode,
                                                              reply_markup=reply_markup,
                                                              input_message_content=input_message_content)


class InlineQueryResultCachedVideo(InlineQueryResult):
    """
    Represents a link to a video file stored on the Telegram servers.
    By default, this video file will be sent by the user with an optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the video.
    https://core.telegram.org/bots/api#inlinequeryresultcachedvideo
    """
    type: str = None
    video_file_id: str = None
    title: str = None
    description: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None

    def __init__(self, *,
                 id: str,
                 video_file_id: str,
                 title: str,
                 description: Optional[str] = None,
                 caption: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None):
        super(InlineQueryResultCachedVideo, self).__init__(id=id,
                                                           video_file_id=video_file_id,
                                                           title=title,
                                                           description=description,
                                                           caption=caption,
                                                           parse_mode=parse_mode,
                                                           reply_markup=reply_markup,
                                                           input_message_content=input_message_content)


class InlineQueryResultCachedVoice(InlineQueryResult):
    """
    Represents a link to a voice message stored on the Telegram servers.
    By default, this voice message will be sent by the user.
    Alternatively, you can use input_message_content to send a message with the specified content
    instead of the voice message.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016. Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultcachedvoice
    """
    type: str = None
    voice_file_id: str = None
    title: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None

    def __init__(self, *,
                 id: str,
                 voice_file_id: str,
                 title: str,
                 caption: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None):
        super(InlineQueryResultCachedVoice, self).__init__(id=id,
                                                           voice_file_id=voice_file_id,
                                                           title=title, caption=caption,
                                                           parse_mode=parse_mode,
                                                           reply_markup=reply_markup,
                                                           input_message_content=input_message_content)


class InlineQueryResultCachedAudio(InlineQueryResult):
    """
    Represents a link to an mp3 audio file stored on the Telegram servers.
    By default, this audio file will be sent by the user.
    Alternatively, you can use input_message_content to send a message with
    the specified content instead of the audio.
    Note: 'This' will only work in Telegram versions released after 9 April, 2016.
    Older clients will ignore them.
    https://core.telegram.org/bots/api#inlinequeryresultcachedaudio
    """
    type: str = None
    audio_file_id: str = None
    caption: str = None
    input_message_content: 'InputMessageContent' = None

    def __init__(self, *,
                 id: str,
                 audio_file_id: str,
                 caption: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 reply_markup: Optional['InlineKeyboardMarkup'] = None,
                 input_message_content: Optional[InputMessageContent] = None):
        super(InlineQueryResultCachedAudio, self).__init__(id=id,
                                                           audio_file_id=audio_file_id,
                                                           caption=caption,
                                                           parse_mode=parse_mode,
                                                           reply_markup=reply_markup,
                                                           input_message_content=input_message_content)


class GameHighScore(BaseModel):
    """
    This object represents one row of the high scores table for a game.
    And that‘s about all we’ve got for now.
    If you've got any questions, please check out our Bot FAQ
    https://core.telegram.org/bots/api#gamehighscore
    """
    position: int = None
    user: 'User' = None
    score: int = None


class ForceReply(BaseModel):
    """
    Upon receiving a message with this object,
    Telegram clients will display a reply interface to the user
    (act as if the user has selected the bot‘s message and tapped ’Reply').
    This can be extremely useful if you want to create user-friendly step-by-step
    interfaces without having to sacrifice privacy mode.
    Example: 'A' poll bot for groups runs in privacy mode
    (only receives commands, replies to its messages and mentions).
    There could be two ways to create a new poll
    The last option is definitely more attractive.
    And if you use ForceReply in your bot‘s questions, it will receive the user’s answers even
    if it only receives replies, commands and mentions — without any extra work for the user.
    https://core.telegram.org/bots/api#forcereply
    """
    force_reply: bool = None
    selective: bool = None


class File(BaseModel):
    """
    This object represents a file ready to be downloaded.
    The file can be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>.
    It is guaranteed that the link will be valid for at least 1 hour.
    When the link expires, a new one can be requested by calling getFile.
    Maximum file size to download is 20 MB
    https://core.telegram.org/bots/api#file
    """
    file_id: str = None
    file_size: int = None
    file_path: str = None


class ChatMember(BaseModel):
    """
    This object contains information about one member of a chat.
    https://core.telegram.org/bots/api#chatmember
    """
    user: 'User' = None
    status: str = None
    until_date: datetime.datetime = None
    can_be_edited: bool = None
    can_change_info: bool = None
    can_post_messages: bool = None
    can_edit_messages: bool = None
    can_delete_messages: bool = None
    can_invite_users: bool = None
    can_restrict_members: bool = None
    can_pin_messages: bool = None
    can_promote_members: bool = None
    is_member: bool = None
    can_send_messages: bool = None
    can_send_media_messages: bool = None
    can_send_other_messages: bool = None
    can_add_web_page_previews: bool = None

    def is_chat_admin(self):
        return ChatMemberStatus.is_admin(self.status)

    def is_chat_member(self):
        return ChatMemberStatus.is_member(self.status)

    def __int__(self):
        return self.user.id


class ChatMemberStatus(str, Enum):
    CREATOR = 'creator'
    ADMINISTRATOR = 'administrator'
    MEMBER = 'member'
    LEFT = 'left'
    KICKED = 'kicked'

    @classmethod
    def is_chat_admin(cls, role):
        return role in [cls.ADMINISTRATOR, cls.CREATOR]

    @classmethod
    def is_chat_member(cls, role):
        return role in [cls.MEMBER, cls.ADMINISTRATOR, cls.CREATOR]


class CallbackGame(BaseModel):
    """
    A placeholder, currently holds no information. Use BotFather to set up your game.
    https://core.telegram.org/bots/api#callbackgame
    """
    pass


class AuthWidgetData(BaseModel):
    id: int = None
    first_name: str = None
    last_name: str = None
    username: str = None
    photo_url: str = None
    auth_date: str = None
    hash: str = None
