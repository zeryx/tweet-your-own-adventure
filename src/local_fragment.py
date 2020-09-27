


class LocalFragment:
    left = None
    right = None
    terminus = False
    body = None
    id = None

    def __init__(self, id, body, left_path=None, right_path=None, terminus=False):
        self.terminus = terminus
        self.body = body
        self.id = id
        if left_path:
            self.left = {"fragment": None, "body": left_path['body'], "id": left_path['id']}
        if right_path:
            self.right = {"fragment": None, "body": right_path['body'], "id": right_path['id']}

    def set_left_fragment(self, fragment):
        self.left_fragment = fragment

    def set_right_fragment(self, fragment):
        self.right_fragment = fragment