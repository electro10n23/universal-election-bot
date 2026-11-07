from discord import Embed, Color

class MismatchError(ValueError):
    def __init__(self, msg: str, mismatch_dict: dict[str, str]) -> None:
        super().__init__(msg, mismatch_dict)
        self.msg = msg
        self.mismatch_dict = mismatch_dict

# Tests the error embed in the !sync command in main.py.
def test_sync_error_embed(produced_embed: Embed) -> None:
    test_embed = Embed(color=Color.red(),title="⚠️ Cannot sync application commands! ⚠️")
    test_embed.add_field(name="", value="You do not have permission to sync commands.")

    if produced_embed.color.value == test_embed.color.value: #type: ignore
        has_same_color = True
    else:
        has_same_color = False

    if produced_embed.title == test_embed.title: #type: ignore
        has_same_title = True
    else:
        has_same_title = False

    if produced_embed.fields[0].name == produced_embed.fields[0].name: #type: ignore
        has_same_field_name = True
    else:
        has_same_field_name = False

    if produced_embed.fields[0].value == produced_embed.fields[0].value: #type: ignore
        has_same_field_value = True
    else:
        has_same_field_value = False

    if has_same_color and has_same_title and has_same_field_name and has_same_field_value:
        return
    else:
        raise MismatchError(msg="Embed created by ErrorEmbed() does not have the expected result",
                            mismatch_dict={
                                f"Expected color: {test_embed.color.value}": #type: ignore
                                f"Actual color: {produced_embed.color.value}", #type: ignore

                                f"Expected title: {test_embed.title}": 
                                f"Actual title: {produced_embed.title}",

                                f"Expected field name: {test_embed.fields[0].name}":
                                f"Actual field name: {produced_embed.fields[0].name}",

                                f"Expected field name: {test_embed.fields[0].value}":
                                f"Actual field name: {produced_embed.fields[0].value}",
                            })