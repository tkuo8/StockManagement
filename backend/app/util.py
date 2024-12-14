from enum import Enum


# キャメルケース変換関数を定義
def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_keys_to_camel_case(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = snake_to_camel(key)
            new_dict[new_key] = convert_keys_to_camel_case(value)
        return new_dict
    elif isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    else:
        return data


# モデルを値を辞書にする。ただし、プロパティやメソッドを除く。
def model_to_dict(obj):
    return {
        col.name: (
            getattr(obj, col.name).value
            if isinstance(getattr(obj, col.name), Enum)
            else getattr(obj, col.name)
        )
        for col in obj.__table__.columns
    }
